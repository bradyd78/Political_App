"""
JSON-backed data storage layer for bill comments and user accounts.

Provides atomic file writes and cross-platform file locking for thread safety.
Uses passlib with bcrypt for secure password hashing.

Note: If file locking is unavailable (e.g., on some file systems), the code
falls back to in-process threading locks. Full concurrent access protection
across multiple processes requires proper file locking support.
"""

import json
import os
import tempfile
import threading
from datetime import datetime, timezone
from typing import Any, Optional

try:
    from passlib.hash import bcrypt
except ImportError:
    bcrypt = None


# Data directory and file paths
DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'data')
COMMENTS_FILE = os.path.join(DATA_DIR, 'comments.json')
USERS_FILE = os.path.join(DATA_DIR, 'users.json')

# In-process locks for fallback when file locking fails
_comments_lock = threading.Lock()
_users_lock = threading.Lock()


def _ensure_data_dir() -> None:
    """Ensure the data directory exists."""
    os.makedirs(DATA_DIR, exist_ok=True)


def _acquire_file_lock(file_handle, exclusive: bool = True) -> bool:
    """
    Acquire a file lock. Returns True if successful, False otherwise.
    Falls back gracefully if file locking is not supported.
    """
    try:
        import fcntl
        lock_type = fcntl.LOCK_EX if exclusive else fcntl.LOCK_SH
        fcntl.flock(file_handle.fileno(), lock_type)
        return True
    except (ImportError, OSError):
        pass

    try:
        import msvcrt
        # msvcrt only supports exclusive locks; use LK_LOCK for blocking exclusive lock
        # For non-exclusive reads, we still use exclusive lock on Windows for simplicity
        msvcrt.locking(file_handle.fileno(), msvcrt.LK_LOCK, 1)
        return True
    except (ImportError, OSError):
        pass

    return False


def _release_file_lock(file_handle) -> None:
    """Release a file lock if held."""
    try:
        import fcntl
        fcntl.flock(file_handle.fileno(), fcntl.LOCK_UN)
        return
    except (ImportError, OSError):
        pass

    try:
        import msvcrt
        msvcrt.locking(file_handle.fileno(), msvcrt.LK_UNLCK, 1)
    except (ImportError, OSError):
        pass


def _atomic_write(filepath: str, data: Any) -> None:
    """
    Write data to file atomically using temp file + os.replace.
    """
    _ensure_data_dir()
    dir_name = os.path.dirname(filepath)

    # Write to temp file first
    fd, temp_path = tempfile.mkstemp(dir=dir_name, suffix='.tmp')
    try:
        with os.fdopen(fd, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        # Atomic replace
        os.replace(temp_path, filepath)
    except Exception:
        # Clean up temp file on failure
        if os.path.exists(temp_path):
            os.unlink(temp_path)
        raise


def _read_json_file(filepath: str, default: Any) -> Any:
    """Read JSON file with optional default value."""
    _ensure_data_dir()
    if not os.path.exists(filepath):
        return default
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            _acquire_file_lock(f, exclusive=False)
            try:
                return json.load(f)
            finally:
                _release_file_lock(f)
    except (json.JSONDecodeError, OSError):
        return default


# =============================================================================
# Comments API
# =============================================================================

def load_comments() -> dict:
    """
    Load all comments from the JSON file.

    Returns:
        dict: A dictionary mapping bill_id to list of comments.
    """
    with _comments_lock:
        return _read_json_file(COMMENTS_FILE, {})


def save_comments(comments: dict) -> None:
    """
    Save all comments to the JSON file atomically.

    Args:
        comments: Dictionary mapping bill_id to list of comments.
    """
    with _comments_lock:
        _atomic_write(COMMENTS_FILE, comments)


def add_comment(bill_id: str, author: str, text: str) -> dict:
    """
    Add a comment to a bill.

    Args:
        bill_id: The ID of the bill.
        author: The username of the comment author.
        text: The comment text.

    Returns:
        dict: The newly created comment.
    """
    with _comments_lock:
        comments = _read_json_file(COMMENTS_FILE, {})
        if bill_id not in comments:
            comments[bill_id] = []

        comment = {
            'text': text,
            'user': author,
            'timestamp': datetime.now(timezone.utc).isoformat().replace('+00:00', 'Z')
        }
        comments[bill_id].append(comment)
        _atomic_write(COMMENTS_FILE, comments)
        return comment


def get_comments_for_bill(bill_id: str) -> list:
    """
    Get all comments for a specific bill.

    Args:
        bill_id: The ID of the bill.

    Returns:
        list: List of comments for the bill.
    """
    comments = load_comments()
    return comments.get(bill_id, [])


# =============================================================================
# Users API
# =============================================================================

def _hash_password(password: str) -> str:
    """Hash a password using bcrypt."""
    if bcrypt is None:
        raise RuntimeError("passlib[bcrypt] is required for password hashing")
    return bcrypt.hash(password)


def _verify_password(password: str, hashed: str) -> bool:
    """Verify a password against its hash."""
    if bcrypt is None:
        raise RuntimeError("passlib[bcrypt] is required for password verification")
    try:
        return bcrypt.verify(password, hashed)
    except Exception:
        return False


def load_users() -> dict:
    """
    Load all users from the JSON file.

    Returns:
        dict: A dictionary mapping username to user data.
    """
    with _users_lock:
        return _read_json_file(USERS_FILE, {})


def save_users(users: dict) -> None:
    """
    Save all users to the JSON file atomically.

    Args:
        users: Dictionary mapping username to user data.
    """
    with _users_lock:
        _atomic_write(USERS_FILE, users)


def create_user(username: str, password: str, display_name: Optional[str] = None) -> dict:
    """
    Create a new user with hashed password.

    Args:
        username: The username for the new user.
        password: The plaintext password (will be hashed).
        display_name: Optional display name.

    Returns:
        dict: The newly created user data (without password hash).

    Raises:
        ValueError: If username already exists.
    """
    with _users_lock:
        users = _read_json_file(USERS_FILE, {})

        if username in users:
            raise ValueError(f"User '{username}' already exists")

        user = {
            'password_hash': _hash_password(password),
            'display_name': display_name or username,
            'is_admin': False,
            'created_at': datetime.now(timezone.utc).isoformat().replace('+00:00', 'Z')
        }
        users[username] = user
        _atomic_write(USERS_FILE, users)

        # Return user data without password hash
        return {
            'username': username,
            'display_name': user['display_name'],
            'is_admin': user['is_admin'],
            'created_at': user['created_at']
        }


def authenticate_user(username: str, password: str) -> dict | None:
    """
    Authenticate a user by username and password.

    Args:
        username: The username to authenticate.
        password: The plaintext password to verify.

    Returns:
        dict: User data if authentication succeeds, None otherwise.
    """
    users = load_users()
    user = users.get(username)

    if not user:
        return None

    # Support both legacy plaintext passwords and bcrypt hashes
    password_hash = user.get('password_hash') or user.get('password')
    if password_hash is None or password_hash == '':
        return None

    # Check if this is a legacy plaintext password (bcrypt hashes start with $2)
    if not str(password_hash).startswith('$2'):
        # Legacy plaintext comparison
        if password_hash == password:
            return {
                'username': username,
                'display_name': user.get('display_name', username),
                'is_admin': user.get('is_admin', False)
            }
        return None

    # Bcrypt hash verification
    if _verify_password(password, password_hash):
        return {
            'username': username,
            'display_name': user.get('display_name', username),
            'is_admin': user.get('is_admin', False)
        }
    return None


def update_password(username: str, new_password: str) -> bool:
    """
    Update a user's password.

    Args:
        username: The username of the user.
        new_password: The new plaintext password (will be hashed).

    Returns:
        bool: True if password was updated, False if user not found.
    """
    with _users_lock:
        users = _read_json_file(USERS_FILE, {})

        if username not in users:
            return False

        users[username]['password_hash'] = _hash_password(new_password)
        # Remove legacy plaintext password if present
        users[username].pop('password', None)
        _atomic_write(USERS_FILE, users)
        return True
