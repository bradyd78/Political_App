# 🚀 How to Run the Political App - Complete Instructions

## Quick Start (3 Steps)

```bash
# 1. Install dependencies
pip install flask flask-cors requests

# 2. Start the server
python3 frontend/src/app.py

# 3. Open browser to http://localhost:5000
```

Default login: **admin** / **1234**

---

## Detailed Instructions

### Step 1: Prerequisites

Make sure you have Python installed:
```bash
python3 --version
```

You should see Python 3.8 or higher.

### Step 2: Install Dependencies

Install required Python packages:
```bash
pip install -r requirements.txt
```

Or install manually:
```bash
pip install flask flask-cors requests
```

### Step 3: Start the Application

From the project root directory:
```bash
python3 frontend/src/app.py
```

You should see output like:
```
 * Serving Flask app 'app'
 * Debug mode: on
 * Running on http://0.0.0.0:5000
```

### Step 4: Access the Application

Open your web browser and go to:
```
http://localhost:5000
```

---

## Using the Application

### 1. **Login or Create Account**
   - Navigate to: `http://localhost:5000/login`
   - **Signup:** Enter a new username and password, click "Signup"
   - **Login:** Use existing credentials, click "Login"
   - **Admin Account:** username `admin`, password `1234`

### 2. **View Bills (Home Page)**
   - Go to: `http://localhost:5000/`
   - Browse all available bills
   - Use the search box to filter by keyword, category, or bill ID
   - Click **"Reload Bills Feed"** to refresh the list

### 3. **Comment on Bills**
   - Click **"Details"** on any bill to expand it
   - View existing comments
   - Type your comment in the input field
   - Click **"Post"** to submit
   - Your username will appear with your comment

### 4. **View Publishes (Articles/Blogs)**
   - Navigate to: `http://localhost:5000/publishes`
   - Browse published articles and blog posts
   - Filter by type (Article/Blog) or search by keyword

### 5. **Admin Features** (Admin users only)
   - Go to: `http://localhost:5000/admin`
   - **Create Bills:** Add new bills with title, description, and category
   - **Publish Content:** Create articles and blog posts
   - Only accessible if logged in as an admin user

### 6. **Other Pages**
   - **Map:** `http://localhost:5000/map` - Interactive map view
   - **Quiz:** `http://localhost:5000/quiz` - Political quiz

---

## API Reference

### Authentication Endpoints

#### Signup
```http
POST /signup
Content-Type: application/json

{
  "username": "newuser",
  "password": "password123"
}
```

**Example:**
```bash
curl -X POST http://localhost:5000/signup \
  -H "Content-Type: application/json" \
  -d '{"username": "john", "password": "pass123"}'
```

#### Login
```http
POST /login
Content-Type: application/json

{
  "username": "admin",
  "password": "1234"
}
```

**Response:**
```json
{
  "success": true,
  "message": "Login successful"
}
```

**Example:**
```bash
curl -X POST http://localhost:5000/login \
  -H "Content-Type: application/json" \
  -d '{"username": "admin", "password": "1234"}'
```

#### Logout
```http
GET /logout
```

### Bill Endpoints

#### Get All Bills
```http
GET /api/bills
```

**Example:**
```bash
curl http://localhost:5000/api/bills
```

**Response:**
```json
[
  {
    "id": "B001",
    "title": "Tax Reform Act",
    "description": "Reduces taxes for small businesses",
    "category": "Economy"
  }
]
```

#### Create Bill (Admin Only)
```http
POST /api/bills
Content-Type: application/json

{
  "title": "New Bill Title",
  "description": "Bill description here",
  "category": "Healthcare"
}
```

### Comment Endpoints

#### Get Comments for a Bill
```http
GET /api/bills/<bill_id>/comments
```

**Example:**
```bash
curl http://localhost:5000/api/bills/B001/comments
```

**Response:**
```json
[
  {
    "user": "admin",
    "text": "Great bill!"
  },
  {
    "user": "john",
    "text": "I support this."
  }
]
```

#### Post Comment
```http
POST /api/bills/<bill_id>/comments
Content-Type: application/json

{
  "text": "Your comment here"
}
```

**Example:**
```bash
curl -X POST http://localhost:5000/api/bills/B001/comments \
  -H "Content-Type: application/json" \
  -d '{"text": "This is a great bill!"}'
```

**Note:** Must be logged in (have session cookie) or comment will show as "anonymous"

### Publishes Endpoints

#### Get All Publishes
```http
GET /api/publishes
```

Optional query parameters:
- `type` - Filter by "Article" or "Blog"
- `q` - Search by keyword

**Example:**
```bash
curl http://localhost:5000/api/publishes?type=Article
```

#### Create Publish (Admin Only)
```http
POST /api/publishes
Content-Type: application/json

{
  "title": "Article Title",
  "content": "Article content here...",
  "type": "Article"
}
```

---

## Data Storage

All application data is stored in JSON files in the `database/` directory:

### `database/users.json`
Stores user accounts and authentication data:
```json
{
  "admin": {
    "password": "1234",
    "is_admin": true
  },
  "john": {
    "password": "pass123",
    "is_admin": false
  }
}
```

### `database/comments.json`
Stores comments organized by bill ID:
```json
{
  "B001": [
    {
      "user": "admin",
      "text": "Great bill!"
    },
    {
      "user": "john",
      "text": "I support this"
    }
  ],
  "B002": [
    {
      "user": "jane",
      "text": "Needs improvement"
    }
  ]
}
```

### `database/publishes.json`
Stores published articles and blogs:
```json
[
  {
    "id": 1,
    "title": "New Tax Policy Announced",
    "content": "The government revealed...",
    "type": "Article",
    "timestamp": "2025-12-03T10:30:00Z"
  }
]
```

### `database/billsList.txt`
Stores bill information (one per line):
```
B001: Tax Reform Act — Reduces taxes for small businesses. [Economy]
B002: Healthcare Expansion — Provides universal coverage. [Healthcare]
B003: Education Bill — Increases funding for schools. [Education]
```

**All data persists automatically** across server restarts!

---

## Testing

### Run the Test Script

Verify your setup is correct:
```bash
python3 test_setup.py
```

This checks:
- ✅ All required files exist in correct locations
- ✅ JSON files are valid and readable
- ✅ Database structure is correct
- ✅ Duplicate files have been removed

### Manual Testing

1. **Test Signup:**
   - Go to `/login`
   - Create account with username "test" and password "test123"
   - Verify you're redirected to home page

2. **Test Login:**
   - Log out if needed
   - Login with username "admin" and password "1234"
   - Verify successful login

3. **Test Comments:**
   - Go to home page
   - Expand any bill
   - Post a comment
   - Verify comment appears with your username

4. **Test Persistence:**
   - Stop the server (Ctrl+C)
   - Restart: `python3 frontend/src/app.py`
   - Log in again
   - Verify your comments are still there

---

## Troubleshooting

### Problem: Port 5000 Already in Use

**Solution:**
```bash
# Find and kill the process using port 5000
lsof -ti:5000 | xargs kill -9

# Then restart the app
python3 frontend/src/app.py
```

### Problem: Import Errors (Module not found)

**Solution:**
```bash
# Upgrade pip
python3 -m pip install --upgrade pip

# Install dependencies
pip install flask flask-cors requests

# Or use requirements file
pip install -r requirements.txt
```

### Problem: Can't Find Python3

**Solution:**
```bash
# Try with python instead
python frontend/src/app.py

# Or check Python version
python --version
python3 --version
```

### Problem: Permission Denied

**Solution:**
```bash
# Make the script executable
chmod +x frontend/src/app.py

# Run it
python3 frontend/src/app.py
```

### Problem: Database Files Missing

**Solution:**
The app automatically creates database files on first run. If you deleted them:
```bash
# Ensure database directory exists
mkdir -p database

# Restart the app (it will recreate files)
python3 frontend/src/app.py
```

### Problem: Comments Not Saving

**Check:**
1. Make sure you're logged in (check /login)
2. Verify `database/comments.json` has write permissions
3. Check the browser console for errors (F12)
4. Check the Flask console output for error messages

### Problem: Can't Access Admin Page

**Solution:**
Only admin users can access `/admin`. To make a user admin:
1. Stop the server
2. Edit `database/users.json`
3. Set `"is_admin": true` for your user
4. Restart the server

Example:
```json
{
  "myusername": {
    "password": "mypassword",
    "is_admin": true
  }
}
```

---

## Advanced Configuration

### Change Server Port

Set the `PORT` environment variable:
```bash
export PORT=8080
python3 frontend/src/app.py
```

The app will now run on `http://localhost:8080`

### Set Secret Key

For production, set a strong secret key:
```bash
export FLASK_SECRET="your-super-secret-key-here"
python3 frontend/src/app.py
```

### Run in Production Mode

```bash
export FLASK_ENV=production
python3 frontend/src/app.py
```

### Reset All Data

To start fresh with empty data:
```bash
# Remove all data files
rm database/users.json
rm database/comments.json  
rm database/publishes.json

# Restart app (will recreate with defaults)
python3 frontend/src/app.py
```

---

## File Structure

```
Political_App/
├── frontend/
│   └── src/
│       ├── app.py                 # Main Flask application
│       ├── templates/             # HTML templates
│       │   ├── index.html         # Home page with bills
│       │   ├── login.html         # Login/Signup page
│       │   ├── admin.html         # Admin console
│       │   └── ...
│       └── static/                # CSS/JS files
│           ├── css/
│           └── js/
├── database/
│   ├── users.json                 # User accounts
│   ├── comments.json              # Bill comments
│   ├── publishes.json             # Articles/blogs
│   └── billsList.txt              # Bill data
├── test_setup.py                  # Setup verification script
├── requirements.txt               # Python dependencies
├── START.md                       # This file
└── README.md                      # Project documentation
```

---

## Security Notes

⚠️ **Important:** This is a development/demo setup. For production:

1. **Hash Passwords:** Use bcrypt instead of plain text
2. **HTTPS:** Use SSL/TLS encryption
3. **Strong Secret:** Set `FLASK_SECRET` to a random string
4. **CSRF Protection:** Add CSRF tokens to forms
5. **Input Validation:** Sanitize all user inputs
6. **Rate Limiting:** Prevent brute force attacks
7. **Error Logging:** Log errors securely
8. **Session Timeout:** Implement session expiration

---

## Next Steps

Once you have the app running:

1. ✅ Create a personal account
2. ✅ Browse and comment on bills
3. ✅ Try the admin features (with admin account)
4. ✅ Explore the publishes page
5. ✅ Check out the map and quiz pages

---

## Support

If you run into issues:

1. Check this troubleshooting guide
2. Run `python3 test_setup.py` for diagnostics
3. Check the Flask console for error messages
4. Verify all files are in the correct locations
5. Make sure you're in the project root directory

---

## Summary

**To run the app:**
```bash
python3 frontend/src/app.py
```

**To access:**
```
http://localhost:5000
```

**To login:**
- Username: `admin`
- Password: `1234`

That's it! Enjoy using the Political App! 🎉
