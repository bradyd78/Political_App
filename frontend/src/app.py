import os
import requests
from flask import Flask, render_template, request, jsonify, redirect, url_for, session, Response
from flask_cors import CORS
from collections import defaultdict

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

app = Flask(__name__, template_folder=os.path.join(BASE_DIR, 'templates'), static_folder=os.path.join(BASE_DIR, 'static'))
CORS(app)
app.secret_key = os.environ.get('FLASK_SECRET', 'dev-secret-key')

# In-memory comments: {bill_id: [ {"text": ..., "user": ...}, ... ]}
COMMENTS = defaultdict(list)

JAVA_BACKEND = os.environ.get('JAVA_BACKEND_URL', 'http://localhost:8080')

@app.route('/api/bills/<bill_id>/comments', methods=['GET'])
def get_comments(bill_id):
    return jsonify(COMMENTS[bill_id])

@app.route('/api/bills/<bill_id>/comments', methods=['POST'])
def post_comment(bill_id):
    data = request.get_json() or {}
    text = data.get('text', '').strip()
    user = session.get('user', 'anonymous')
    if not text:
        return jsonify({'error': 'Comment text required'}), 400
    COMMENTS[bill_id].append({'text': text, 'user': user})
    return jsonify({'success': True})
import os
import requests
from flask import Flask, render_template, request, jsonify, redirect, url_for, session, Response
from flask_cors import CORS

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

app = Flask(__name__, template_folder=os.path.join(BASE_DIR, 'templates'), static_folder=os.path.join(BASE_DIR, 'static'))
CORS(app)
app.secret_key = os.environ.get('FLASK_SECRET', 'dev-secret-key')

JAVA_BACKEND = os.environ.get('JAVA_BACKEND_URL', 'http://localhost:8080')

@app.route('/')
def home():
    user = session.get('user')
    return render_template('index.html', user=user)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    data = request.get_json() or request.form or {}
    username = data.get('username')
    password = data.get('password')
    if username == 'admin' and password == '1234':
        session['user'] = username
        return jsonify({"success": True, "message": "Login successful"})
    return jsonify({"success": False, "message": "Invalid credentials"}), 401

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('home'))

@app.route('/map')
def map_page():
    return render_template('map.html')

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
                import re
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
            return Response(r.content, status=r.status_code, content_type=r.headers.get('Content-Type', 'application/json'))
        except Exception as e2:
            return jsonify({'error': 'Could not load bills', 'details': str(e), 'proxy_error': str(e2)}), 502

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)), debug=True)
