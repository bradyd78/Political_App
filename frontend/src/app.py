import json
import os
import re
from datetime import datetime

import requests
from flask import (
    Flask, Response, jsonify, redirect, render_template, request, session, url_for
)
from flask_cors import CORS

import data_store

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

app = Flask(
    __name__,
    template_folder=os.path.join(BASE_DIR, 'templates'),
    static_folder=os.path.join(BASE_DIR, 'static')
)
CORS(app)
app.secret_key = os.environ.get('FLASK_SECRET', 'dev-secret-key')

JAVA_BACKEND = os.environ.get('JAVA_BACKEND_URL', 'http://localhost:8080')

# File-backed publishes store (persisted to database/publishes.json)
PUBLISHES = []
PUBLISHES_FILE = os.path.abspath(os.path.join(BASE_DIR, '..', '..', 'database', 'publishes.json'))

def load_publishes_from_file():
    global PUBLISHES
    try:
        if os.path.exists(PUBLISHES_FILE):
            with open(PUBLISHES_FILE, 'r', encoding='utf-8') as fh:
                PUBLISHES = json.load(fh)
                return
    except Exception:
        # If reading fails, fall back to an empty list and overwrite on save
        PUBLISHES = []

    # If file missing or failed to load, seed default publishes and persist
    now = datetime.utcnow().isoformat() + 'Z'
    PUBLISHES = [
        {'id': 1, 'title': 'New Tax Policy Announced', 'content': 'The government revealed a new tax policy aimed at supporting small businesses.', 'type': 'Article', 'timestamp': now},
        {'id': 2, 'title': 'Understanding the New Voting Bill', 'content': 'A detailed look into the implications of the latest voting rights bill.', 'type': 'Article', 'timestamp': now},
        {'id': 3, 'title': 'Behind the Scenes: Policy Reform Journey', 'content': 'A first-hand blog on what it’s like to navigate the policy reform process.', 'type': 'Blog', 'timestamp': now},
        {'id': 4, 'title': 'My Experience at the National Debate', 'content': 'An inside story from a young journalist attending the annual national debate.', 'type': 'Blog', 'timestamp': now},
    ]
    save_publishes_to_file()


def save_publishes_to_file():
    try:
        os.makedirs(os.path.dirname(PUBLISHES_FILE), exist_ok=True)
        with open(PUBLISHES_FILE, 'w', encoding='utf-8') as fh:
            json.dump(PUBLISHES, fh, ensure_ascii=False, indent=2)
    except Exception:
        # Fail silently; the app will continue to serve in-memory data
        pass


def seed_publishes():
    if PUBLISHES:
        return
    load_publishes_from_file()

@app.route('/')
def home():
    user = session.get('user')
    return render_template('index.html', user=user)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    req_data = request.get_json() or request.form or {}
    username = req_data.get('username')
    password = req_data.get('password')
    if not username or not password:
        return jsonify({"success": False, "message": "Missing credentials"}), 400
    user_info = data_store.authenticate_user(username, password)
    if not user_info:
        return jsonify({"success": False, "message": "Invalid credentials"}), 401
    session['user'] = username
    session['is_admin'] = bool(user_info.get('is_admin'))
    return jsonify({"success": True, "message": "Login successful"})


@app.route('/logout')
def logout():
    session.pop('user', None)
    session.pop('is_admin', None)
    return redirect(url_for('home'))


@app.route('/signup', methods=['POST'])
def signup():
    req_data = request.get_json() or request.form or {}
    username = (req_data.get('username') or '').strip()
    password = (req_data.get('password') or '').strip()
    if not username or not password:
        return 'Username and password required', 400
    if data_store.user_exists(username):
        return 'Username already exists', 400
    if not data_store.add_user(username, password, is_admin=False):
        return 'Failed to create user', 500
    session['user'] = username
    session['is_admin'] = False
    return 'Signup successful'


@app.route('/map')
def map_page():
    return render_template('map.html')


@app.route('/api/bills/<bill_id>/comments', methods=['GET'])
def get_bill_comments(bill_id):
    comments = data_store.get_comments(bill_id)
    return jsonify(comments)


@app.route('/api/bills/<bill_id>/comments', methods=['POST'])
def post_comment(bill_id):
    req_data = request.get_json() or {}
    text = req_data.get('text', '').strip()
    user = session.get('user', 'anonymous')
    if not text:
        return jsonify({'error': 'Comment text required'}), 400
    if not data_store.add_comment(bill_id, text, user):
        return jsonify({'error': 'Failed to save comment'}), 500
    return jsonify({'success': True})


@app.route('/publishes')
def publishes_page():
    seed_publishes()
    user = session.get('user')
    return render_template('publishes.html', user=user)


@app.route('/api/publishes')
def api_publishes():
    seed_publishes()
    q = (request.args.get('q') or '').strip().lower()
    ptype = (request.args.get('type') or '').strip().lower()
    results = []
    for p in PUBLISHES:
        if ptype and p['type'].lower() != ptype:
            continue
        if q and q not in p['title'].lower() and q not in p['content'].lower():
            continue
        results.append(p)
    # sort newest first by timestamp
    try:
        results.sort(key=lambda x: x.get('timestamp', ''), reverse=True)
    except Exception:
        pass
    return jsonify(results)


@app.route('/api/publishes', methods=['POST'])
def api_publishes_post():
    # admin-only: create a publish
    if not session.get('is_admin'):
        return jsonify({'error': 'admin required'}), 403
    req_data = request.get_json() or {}
    title = (req_data.get('title') or '').strip()
    content = (req_data.get('content') or '').strip()
    ptype = (req_data.get('type') or 'Article').strip()
    if not title or not content:
        return jsonify({'error': 'title and content required'}), 400
    load_publishes_from_file()
    next_id = max([p.get('id', 0) for p in PUBLISHES] or [0]) + 1
    new = {
        'id': next_id,
        'title': title,
        'content': content,
        'type': ptype,
        'timestamp': datetime.utcnow().isoformat() + 'Z'
    }
    PUBLISHES.append(new)
    save_publishes_to_file()
    return jsonify({'success': True, 'publish': new})


@app.route('/api/publishes/<int:pid>')
def api_publish_get(pid):
    seed_publishes()
    for p in PUBLISHES:
        if p['id'] == pid:
            return jsonify(p)
    return jsonify({'error': 'not found'}), 404


@app.route('/admin')
def admin_page():
    # render admin UI; ensure user is signed in as admin
    user = session.get('user')
    if not session.get('is_admin'):
        return redirect(url_for('login'))
    load_publishes_from_file()
    return render_template('admin.html', user=user, publishes=PUBLISHES)


@app.route('/quiz')
def quiz_page():
    return render_template('quiz.html')


@app.route('/api/bills')
def api_bills():
    # Try to read bills from billsList.txt first
    bills_file = os.path.join(os.path.dirname(__file__), '../../database/billsList.txt')
    bills = []
    try:
        with open(bills_file, encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith('#'):
                    continue
                # Format: B001: Title — Description. [Category]
                m = re.match(r'^(B\d+):\s*(.+?)\s+—\s+(.+?)\.\s*\[(.+)\]$', line)
                if m:
                    bills.append({
                        'id': m.group(1),
                        'title': m.group(2),
                        'description': m.group(3),
                        'category': m.group(4)
                    })
        return jsonify(bills)
    except Exception as e:
        # If file read fails, fallback to Java backend proxy
        try:
            r = requests.get(f'{JAVA_BACKEND}/api/bills', timeout=5)
            return Response(
                r.content,
                status=r.status_code,
                content_type=r.headers.get('Content-Type', 'application/json')
            )
        except Exception as e2:
            return jsonify({
                'error': 'Could not load bills',
                'details': str(e),
                'proxy_error': str(e2)
            }), 502


@app.route('/api/bills', methods=['POST'])
def api_bills_post():
    # admin-only: add a bill (format: id auto-generated, title, description, category)
    if not session.get('is_admin'):
        return jsonify({'error': 'admin required'}), 403
    req_data = request.get_json() or {}
    title = (req_data.get('title') or '').strip()
    description = (req_data.get('description') or '').strip()
    category = (req_data.get('category') or '').strip() or 'General'
    if not title or not description:
        return jsonify({'error': 'title and description required'}), 400
    bills_file = os.path.join(os.path.dirname(__file__), '../../database/billsList.txt')
    # determine next id
    next_id = 1
    try:
        if os.path.exists(bills_file):
            with open(bills_file, encoding='utf-8') as f:
                for line in f:
                    m = line.strip().split(':', 1)
                    if m and m[0].startswith('B'):
                        try:
                            n = int(m[0][1:])
                            if n >= next_id:
                                next_id = n + 1
                        except Exception:
                            pass
    except Exception:
        pass
    bill_id = f'B{next_id:03d}'
    line = f"{bill_id}: {title} — {description}. [{category}]\n"
    try:
        os.makedirs(os.path.dirname(bills_file), exist_ok=True)
        with open(bills_file, 'a', encoding='utf-8') as f:
            f.write(line)
    except Exception as e:
        return jsonify({'error': 'failed to save', 'details': str(e)}), 500
    return jsonify({'success': True, 'id': bill_id})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)), debug=True)
