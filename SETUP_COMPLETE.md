# Setup Complete! 🎉

## Changes Made

### 1. File Structure
- ✅ **Removed** duplicate `frontend/src/index.html`
- ✅ **Kept** `frontend/src/templates/index.html` (the correct one)

### 2. Backend Setup (Flask)
The Flask backend (`frontend/src/app.py`) now includes:

#### Comment System
- **GET** `/api/bills/<bill_id>/comments` - Retrieve comments for a specific bill
- **POST** `/api/bills/<bill_id>/comments` - Add a new comment to a bill
  - Request body: `{ "text": "Your comment here" }`
  - Comments are saved to `database/comments.json`
  - Comments include the username from the session

#### Authentication System
- **POST** `/signup` - Create a new user account
  - Request body: `{ "username": "user", "password": "pass" }`
  - User data is saved to `database/users.json`
  
- **POST** `/login` - Authenticate a user
  - Request body: `{ "username": "user", "password": "pass" }`
  - Returns: `{ "success": true/false, "message": "..." }`
  - Sets session cookie on success

- **GET** `/logout` - Log out current user

### 3. Data Persistence

#### `database/users.json`
Stores user accounts with structure:
```json
{
  "username": {
    "password": "plaintext_password",
    "is_admin": false
  }
}
```
- Default admin account: `admin` / `1234`

#### `database/comments.json`
Stores bill comments with structure:
```json
{
  "bill_id": [
    {
      "text": "Comment text",
      "user": "username"
    }
  ]
}
```

### 4. Frontend Integration

#### Login Page (`templates/login.html`)
- ✅ Signup form POST to `/signup`
- ✅ Login form POST to `/login`
- ✅ Handles JSON responses properly
- ✅ Redirects to home page on success
- ✅ Shows error messages via alerts

#### Home Page (`templates/index.html`)
- ✅ Displays list of bills
- ✅ Each bill has collapsible details section
- ✅ Shows comments for each bill
- ✅ Comment form to add new comments
- ✅ Real-time comment loading via AJAX
- ✅ Uses session username when posting comments

## How to Use

### Start the Application
```bash
cd /workspaces/Political_App
python3 frontend/src/app.py
```

The app will run on `http://localhost:5000`

### Test the Setup
```bash
python3 test_setup.py
```

### User Flow

1. **Sign Up / Log In**
   - Navigate to `http://localhost:5000/login`
   - Create a new account or log in with existing credentials
   - Default admin: username `admin`, password `1234`

2. **View Bills**
   - Go to home page `http://localhost:5000/`
   - Click "Details" on any bill to expand it

3. **Comment on Bills**
   - Expand a bill's details
   - Type your comment in the input field
   - Click "Post" to submit
   - Your comment appears immediately with your username

4. **Persistence**
   - All user accounts are saved to `database/users.json`
   - All comments are saved to `database/comments.json`
   - Data persists across server restarts

## API Endpoints Summary

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | `/` | Home page | No |
| GET | `/login` | Login page | No |
| POST | `/signup` | Create account | No |
| POST | `/login` | Authenticate | No |
| GET | `/logout` | Sign out | Yes |
| GET | `/api/bills` | List all bills | No |
| GET | `/api/bills/<id>/comments` | Get bill comments | No |
| POST | `/api/bills/<id>/comments` | Add comment | Session* |
| GET | `/admin` | Admin console | Admin only |

*Session recommended (will show as "anonymous" if not logged in)

## Technical Details

### Session Management
- Flask sessions are used for authentication
- Session data stored in encrypted cookie
- Session key: `FLASK_SECRET` environment variable (defaults to `dev-secret-key`)

### Data Loading
On app startup, the following functions are called:
- `load_users_from_file()` - Loads user data from JSON
- `load_comments_from_file()` - Loads comments from JSON
- `load_publishes_from_file()` - Loads published articles/blogs from JSON

### Error Handling
- Invalid credentials return 401 with error message
- Missing data returns 400 with error message
- Admin-only endpoints return 403 if not admin

## Security Notes

⚠️ **Important**: This is a development setup. For production:
1. Hash passwords (use bcrypt or similar)
2. Use HTTPS
3. Set strong `FLASK_SECRET` environment variable
4. Add CSRF protection
5. Implement rate limiting
6. Validate and sanitize all inputs
7. Add proper error logging
