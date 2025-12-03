# Civic Engagement Platform

## Project Overview
This project is a civic engagement platform designed to help users interact with political content, track bills, follow political figures, and comment on legislation. It integrates a mix of **MVC** and **N-tier layered architecture** to ensure scalability, maintainability, and clear separation of concerns.

---

## Software Architecture

### Architectural Diagram

---

### Presentation Layer (MVC Controllers)

This is the topmost layer and consists of the controllers and user interface code.

**Components:**
- AppManager
- UserController
- BillController
- PoliticalFigureController

**Responsibilities:**
- Receives user actions (menu selections, input commands)
- Translates UI requests into service-layer calls
- Formats data before displaying back to the user
- Does not implement business logic

**Communication:**
- Controllers → call → Service Layer Managers
- Controllers → display output → User

---

### Business / Service Layer

This layer contains the core logic of the system.

**Components:**
- UserManager
- BillManager
- PoliticalFigureManager

**Responsibilities:**
- Validate inputs received from controllers
- Apply political app business rules
- Coordinate interactions between controllers and models
- Prepare data for display or further processing

**Communication:**
- Service Layer → reads/writes → Data Layer
- Service Layer → returns results → Controller Layer

---

### Data / Model Layer

This layer stores the application's domain data.

**Components:**
- User
- Bill
- Political_Figure
- JSON Data Storage Handler

**Responsibilities:**
- Represent core data structures
- Store attributes of domain entities
- Support serialization and persistence
- Provide structured data to service layer

**Communication:**
- Models → accessed by → Managers
- Models → return entity data → Managers

---

## Technology Stack

| Layer             | Technologies                     |
|------------------|----------------------------------|
| Presentation      | React, HTML/CSS, JavaScript      |
| Service           | Node.js, Express, Python/Flask   |
| Data Access       | JSON Storage, Supabase, Firebase |

---

## JSON Data Storage Layer

The platform includes a JSON-backed data storage layer (`src/data_store.py`) for managing bill comments and user accounts.

### Features

- **Secure Password Hashing**: Uses `passlib[bcrypt]` for industry-standard password hashing
- **Atomic Writes**: Uses temp file + `os.replace()` for safe concurrent access
- **File Locking**: Cross-platform file locking (fcntl/msvcrt) with in-process lock fallback
- **Legacy Support**: Supports migration from plaintext passwords to bcrypt hashes

### API Reference

#### Comments API
```python
from src.data_store import load_comments, save_comments, add_comment, get_comments_for_bill

# Load all comments
comments = load_comments()

# Save all comments
save_comments({"B001": [{"text": "...", "user": "admin"}]})

# Add a comment to a bill
comment = add_comment("B001", "username", "Comment text")

# Get comments for a specific bill
bill_comments = get_comments_for_bill("B001")
```

#### Users API
```python
from src.data_store import load_users, save_users, create_user, authenticate_user, update_password

# Create a new user (password is automatically hashed)
user = create_user("username", "password", display_name="Display Name")

# Authenticate a user
user = authenticate_user("username", "password")

# Update a user's password
success = update_password("username", "new_password")
```

### Data Files

Data files are stored in the `data/` directory:
- `data/comments.json` - Bill comments
- `data/users.json` - User accounts

Example files are provided:
- `data/comments.json.example`
- `data/users.json.example`

### Migration Notes

If migrating from the existing `database/users.json` with plaintext passwords:

1. The data store automatically supports both legacy plaintext passwords and bcrypt hashes
2. Users can log in with existing plaintext passwords
3. Use `update_password()` to upgrade a user's password to bcrypt
4. New users created via `create_user()` will automatically use bcrypt

---

## Running Tests

```bash
# Run data store tests
python -m unittest tests.test_data_store -v
```

---

## Setup Instructions

```bash
# Clone the repo
git clone https://github.com/yourusername/civic-engagement-platform.git

# Install Python dependencies
pip install -r requirements.txt

# Install Node dependencies
npm install

# Run the app
npm start
```
