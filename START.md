# Quick Start — Political_App

This file explains how to run the demo server and test the frontend/login quickly.

Requirements
- Node.js (16+ recommended)

Run locally
```bash
# from the repository root
npm install
npm start
```

What this starts
- An Express server located at `database/server.js` listening on port `3000`.
- The server serves static files from `frontend/src` (so `http://localhost:3000/` opens the home page).
- A demo login endpoint `POST /login` that accepts JSON and returns { success: true } for credentials `admin` / `1234`.

Test the login page
1. Open `http://localhost:3000/login.html` in your browser.
2. Enter username `admin` and password `1234` and press Login.
3. On success you'll be redirected to `/` (home page). If credentials are invalid you'll see an error message.

Notes
- The login page uses `fetch` to POST JSON to `/login` and handle the response in the browser.
- To expand functionality integrate the Java backend controllers or add persistent storage as needed.
