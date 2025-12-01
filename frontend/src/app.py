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
