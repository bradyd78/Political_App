"""
Thread-safe JSON-based storage backend for comments on bills and user authentication.

This module provides a clean, well-tested API for managing comments and users
with file-based JSON persistence and thread-safe operations.
"""

import json
import os
import threading
from collections import defaultdict
from typing import Any


# File paths for data storage
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.abspath(os.path.join(BASE_DIR, '..', '..', 'database'))
COMMENTS_FILE = os.path.join(DATA_DIR, 'comments.json')
USERS_FILE = os.path.join(DATA_DIR, 'users.json')

# Thread locks for safe concurrent access
_comments_lock = threading.Lock()
_users_lock = threading.Lock()


def _ensure_data_dir() -> None:
    """Ensure the data directory exists."""
    os.makedirs(DATA_DIR, exist_ok=True)


# -----------------------------------------------------------------
# Comments API
# -----------------------------------------------------------------

def load_comments() -> dict[str, list[dict[str, Any]]]:
    """
    Load all comments from the JSON file.

    Returns:
        A dict mapping bill_id -> list of comment dicts.
        Each comment dict has at least 'text' and 'user' keys.
    """
    with _comments_lock:
        try:
            if os.path.exists(COMMENTS_FILE):
                with open(COMMENTS_FILE, 'r', encoding='utf-8') as fh:
                    data = json.load(fh)
                    return defaultdict(list, data)
        except (json.JSONDecodeError, OSError):
            pass
        return defaultdict(list)


def save_comments(comments: dict[str, list[dict[str, Any]]]) -> bool:
    """
    Save all comments to the JSON file.

    Args:
        comments: A dict mapping bill_id -> list of comment dicts.

    Returns:
        True if save was successful, False otherwise.
    """
    with _comments_lock:
        try:
            _ensure_data_dir()
            with open(COMMENTS_FILE, 'w', encoding='utf-8') as fh:
                json.dump(dict(comments), fh, ensure_ascii=False, indent=2)
            return True
        except OSError:
            return False


def get_comments(bill_id: str) -> list[dict[str, Any]]:
    """
    Get comments for a specific bill.

    Args:
        bill_id: The ID of the bill.

    Returns:
        A list of comment dicts for the bill.
    """
    comments = load_comments()
    return comments.get(bill_id, [])


def add_comment(bill_id: str, text: str, user: str) -> bool:
    """
    Add a comment to a specific bill.

    Args:
        bill_id: The ID of the bill.
        text: The comment text.
        user: The username of the commenter.

    Returns:
        True if the comment was added successfully, False otherwise.
    """
    with _comments_lock:
        try:
            # Load current comments
            comments: dict[str, list[dict[str, Any]]] = {}
            if os.path.exists(COMMENTS_FILE):
                with open(COMMENTS_FILE, 'r', encoding='utf-8') as fh:
                    comments = json.load(fh)

            # Add the new comment
            if bill_id not in comments:
                comments[bill_id] = []
            comments[bill_id].append({'text': text, 'user': user})

            # Save back
            _ensure_data_dir()
            with open(COMMENTS_FILE, 'w', encoding='utf-8') as fh:
                json.dump(comments, fh, ensure_ascii=False, indent=2)
            return True
        except (json.JSONDecodeError, OSError):
            return False


# -----------------------------------------------------------------
# Users API
# -----------------------------------------------------------------

def load_users() -> dict[str, dict[str, Any]]:
    """
    Load all users from the JSON file.

    Returns:
        A dict mapping username -> user info dict.
        Each user dict has 'password' and 'is_admin' keys.
    """
    with _users_lock:
        try:
            if os.path.exists(USERS_FILE):
                with open(USERS_FILE, 'r', encoding='utf-8') as fh:
                    return json.load(fh)
        except (json.JSONDecodeError, OSError):
            pass

        # Return default admin user if file doesn't exist or is invalid
        default_users = {'admin': {'password': '1234', 'is_admin': True}}
        # Try to save the default users
        try:
            _ensure_data_dir()
            with open(USERS_FILE, 'w', encoding='utf-8') as fh:
                json.dump(default_users, fh, ensure_ascii=False, indent=2)
        except OSError:
            pass
        return default_users


def save_users(users: dict[str, dict[str, Any]]) -> bool:
    """
    Save all users to the JSON file.

    Args:
        users: A dict mapping username -> user info dict.

    Returns:
        True if save was successful, False otherwise.
    """
    with _users_lock:
        try:
            _ensure_data_dir()
            with open(USERS_FILE, 'w', encoding='utf-8') as fh:
                json.dump(users, fh, ensure_ascii=False, indent=2)
            return True
        except OSError:
            return False


def get_user(username: str) -> dict[str, Any] | None:
    """
    Get a specific user by username.

    Args:
        username: The username to look up.

    Returns:
        The user info dict if found, None otherwise.
    """
    users = load_users()
    return users.get(username)


def add_user(username: str, password: str, is_admin: bool = False) -> bool:
    """
    Add a new user.

    Args:
        username: The username for the new user.
        password: The password for the new user.
        is_admin: Whether the user should have admin privileges.

    Returns:
        True if the user was added successfully, False if the username
        already exists or if there was an error.
    """
    with _users_lock:
        try:
            # Load current users
            users: dict[str, dict[str, Any]] = {}
            if os.path.exists(USERS_FILE):
                with open(USERS_FILE, 'r', encoding='utf-8') as fh:
                    users = json.load(fh)
            else:
                # Start with default admin user
                users = {'admin': {'password': '1234', 'is_admin': True}}

            # Check if username already exists
            if username in users:
                return False

            # Add the new user
            users[username] = {'password': password, 'is_admin': is_admin}

            # Save back
            _ensure_data_dir()
            with open(USERS_FILE, 'w', encoding='utf-8') as fh:
                json.dump(users, fh, ensure_ascii=False, indent=2)
            return True
        except (json.JSONDecodeError, OSError):
            return False


def authenticate_user(username: str, password: str) -> dict[str, Any] | None:
    """
    Authenticate a user by username and password.

    Args:
        username: The username.
        password: The password.

    Returns:
        The user info dict if authentication is successful, None otherwise.
    """
    user = get_user(username)
    if user is not None and user.get('password') == password:
        return user
    return None


def user_exists(username: str) -> bool:
    """
    Check if a user exists.

    Args:
        username: The username to check.

    Returns:
        True if the user exists, False otherwise.
    """
    return get_user(username) is not None
