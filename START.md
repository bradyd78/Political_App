# Quick Start — Political_App

This file explains how to run the Flask server and use the application.

## Requirements
- Python 3.8 or higher
- pip (Python package manager)

## Installation

Install dependencies:
```bash
pip install -r requirements.txt
```

Or install manually:
```bash
pip install flask flask-cors requests
```

## Run the Application

From the repository root:
```bash
python3 frontend/src/app.py
```

The Flask server will start on **http://localhost:5000**

## What This Starts
- A Flask web server at `http://localhost:5000`
- Serves HTML templates from `frontend/src/templates/`
- Provides REST API endpoints for authentication, bills, and comments
- Persists data to JSON files in `database/` directory

## Test the Application

### 1. Open the Login Page
Navigate to: `http://localhost:5000/login`

### 2. Default Admin Credentials
- **Username:** `admin`
- **Password:** `1234`

### 3. Try the Features
- **Home Page:** View and search bills at `http://localhost:5000/`
- **Comments:** Click "Details" on any bill to expand and add comments
- **Signup:** Create a new account on the login page
- **Admin:** Access admin console at `http://localhost:5000/admin` (admin users only)

## API Endpoints

### Authentication
- `POST /signup` - Create new user account
- `POST /login` - Authenticate user (returns JSON with success/message)
- `GET /logout` - Sign out current user

### Bills & Comments
- `GET /api/bills` - Get all bills
- `GET /api/bills/<bill_id>/comments` - Get comments for a bill
- `POST /api/bills/<bill_id>/comments` - Add a comment (JSON: {"text": "..."})
- `POST /api/bills` - Create new bill (admin only)

### Publishes
- `GET /api/publishes` - Get all articles/blogs
- `POST /api/publishes` - Create new publish (admin only)

## Test the Setup

Run the test script:
```bash
python3 test_setup.py
```

This verifies:
- All required files exist
- JSON files are valid
- Database structure is correct

## Data Persistence

All data is saved to JSON files in `database/`:
- `users.json` - User accounts and credentials
- `comments.json` - Bill comments by bill ID
- `publishes.json` - Published articles and blogs
- `billsList.txt` - Bill information

Data persists across server restarts!

## Troubleshooting

**Port 5000 already in use:**
```bash
lsof -ti:5000 | xargs kill -9
```

**Missing dependencies:**
```bash
pip install --upgrade flask flask-cors requests
```

## Quick Test with curl

**Login:**
```bash
curl -X POST http://localhost:5000/login \
  -H "Content-Type: application/json" \
  -d '{"username": "admin", "password": "1234"}'
```

**Get Bills:**
```bash
curl http://localhost:5000/api/bills
```

**Post Comment:**
```bash
curl -X POST http://localhost:5000/api/bills/B001/comments \
  -H "Content-Type: application/json" \
  -d '{"text": "Great bill!"}'
```

1. Open `http://localhost:3000/login.html` in your browser.
2. Enter username `admin` and password `1234` and press Login.
3. On success you'll be redirected to `/` (home page). If credentials are invalid you'll see an error message.

Notes
- The login page uses `fetch` to POST JSON to `/login` and handle the response in the browser.
- To expand functionality integrate the Java backend controllers or add persistent storage as needed.
