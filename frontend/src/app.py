from flask import Flask, render_template, request, jsonify, redirect, url_for, session
from flask_cors import CORS
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

app = Flask(__name__, template_folder=os.path.join(BASE_DIR, 'templates'), static_folder=os.path.join(BASE_DIR, 'static'))
CORS(app)
app.secret_key = os.environ.get('FLASK_SECRET', 'dev-secret-key')


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

    # Demo authentication - replace with real logic later
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


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)), debug=True)
from flask import Flask, request, jsonify, send_from_directory, redirect, url_for
from flask_cors import CORS
import os

# Serve files from the frontend/src directory
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_DIR = BASE_DIR  # file sits in frontend/src

app = Flask(__name__, static_folder=STATIC_DIR, static_url_path='')
CORS(app)

@app.route('/')
def index():
    # serve index.html
    return send_from_directory(STATIC_DIR, 'index.html')

@app.route('/<path:filename>')
def static_files(filename):
    # serve any other frontend files (login.html, map.html, quiz.html, css, js)
    return send_from_directory(STATIC_DIR, filename)

@app.route('/login', methods=['POST'])
def login():
    # Expect JSON with username and password
    data = request.get_json() or {}
    username = data.get('username') or request.form.get('username')
    password = data.get('password') or request.form.get('password')

    # Demo authentication logic (replace with real auth)
    if username == 'admin' and password == '1234':
        return jsonify({"success": True, "message": "Login successful"})
    return jsonify({"success": False, "message": "Invalid credentials"}), 401

if __name__ == '__main__':
    # dev server, accessible on port 5000 by default
    app.run(host='0.0.0.0', port=5000, debug=True)
