"""
Tests for the data_store module.
"""

import json
import os
import tempfile
import threading
from unittest import mock

import pytest


# Set up test environment before importing data_store
@pytest.fixture
def temp_data_dir():
    """Create a temporary directory for test data files."""
    with tempfile.TemporaryDirectory() as tmpdir:
        yield tmpdir


@pytest.fixture
def data_store_module(temp_data_dir):
    """Create a data_store module with temporary file paths."""
    import sys
    # Add frontend/src to path
    src_path = os.path.join(os.path.dirname(__file__), '..', 'frontend', 'src')
    if src_path not in sys.path:
        sys.path.insert(0, src_path)

    import data_store

    # Patch the file paths to use temp directory
    original_comments_file = data_store.COMMENTS_FILE
    original_users_file = data_store.USERS_FILE
    original_data_dir = data_store.DATA_DIR

    data_store.DATA_DIR = temp_data_dir
    data_store.COMMENTS_FILE = os.path.join(temp_data_dir, 'comments.json')
    data_store.USERS_FILE = os.path.join(temp_data_dir, 'users.json')

    yield data_store

    # Restore original paths
    data_store.DATA_DIR = original_data_dir
    data_store.COMMENTS_FILE = original_comments_file
    data_store.USERS_FILE = original_users_file


class TestComments:
    """Tests for comment-related functions."""

    def test_load_comments_empty_file(self, data_store_module):
        """Test loading comments when no file exists."""
        comments = data_store_module.load_comments()
        assert dict(comments) == {}

    def test_save_and_load_comments(self, data_store_module):
        """Test saving and loading comments."""
        test_comments = {
            'B001': [{'text': 'Test comment', 'user': 'testuser'}],
            'B002': [{'text': 'Another comment', 'user': 'admin'}]
        }
        result = data_store_module.save_comments(test_comments)
        assert result is True

        loaded = data_store_module.load_comments()
        assert loaded['B001'] == test_comments['B001']
        assert loaded['B002'] == test_comments['B002']

    def test_get_comments_for_bill(self, data_store_module):
        """Test getting comments for a specific bill."""
        # First add some comments
        data_store_module.add_comment('B001', 'Comment 1', 'user1')
        data_store_module.add_comment('B001', 'Comment 2', 'user2')
        data_store_module.add_comment('B002', 'Comment 3', 'user1')

        comments = data_store_module.get_comments('B001')
        assert len(comments) == 2
        assert comments[0]['text'] == 'Comment 1'
        assert comments[1]['text'] == 'Comment 2'

    def test_get_comments_nonexistent_bill(self, data_store_module):
        """Test getting comments for a bill that doesn't exist."""
        comments = data_store_module.get_comments('NONEXISTENT')
        assert comments == []

    def test_add_comment(self, data_store_module):
        """Test adding a comment to a bill."""
        result = data_store_module.add_comment('B001', 'Test comment', 'testuser')
        assert result is True

        comments = data_store_module.get_comments('B001')
        assert len(comments) == 1
        assert comments[0]['text'] == 'Test comment'
        assert comments[0]['user'] == 'testuser'


class TestUsers:
    """Tests for user-related functions."""

    def test_load_users_creates_default_admin(self, data_store_module):
        """Test that loading users creates a default admin user."""
        users = data_store_module.load_users()
        assert 'admin' in users
        assert users['admin']['password'] == '1234'
        assert users['admin']['is_admin'] is True

    def test_save_and_load_users(self, data_store_module):
        """Test saving and loading users."""
        test_users = {
            'admin': {'password': '1234', 'is_admin': True},
            'user1': {'password': 'pass1', 'is_admin': False}
        }
        result = data_store_module.save_users(test_users)
        assert result is True

        loaded = data_store_module.load_users()
        assert loaded == test_users

    def test_get_user_exists(self, data_store_module):
        """Test getting an existing user."""
        # Load default users first (creates admin)
        data_store_module.load_users()

        user = data_store_module.get_user('admin')
        assert user is not None
        assert user['password'] == '1234'
        assert user['is_admin'] is True

    def test_get_user_not_exists(self, data_store_module):
        """Test getting a non-existent user."""
        user = data_store_module.get_user('nonexistent')
        assert user is None

    def test_add_user(self, data_store_module):
        """Test adding a new user."""
        result = data_store_module.add_user('newuser', 'newpass', is_admin=False)
        assert result is True

        user = data_store_module.get_user('newuser')
        assert user is not None
        assert user['password'] == 'newpass'
        assert user['is_admin'] is False

    def test_add_user_duplicate(self, data_store_module):
        """Test adding a duplicate user fails."""
        data_store_module.add_user('testuser', 'pass1')
        result = data_store_module.add_user('testuser', 'pass2')
        assert result is False

    def test_authenticate_user_success(self, data_store_module):
        """Test successful user authentication."""
        # Load default users (creates admin)
        data_store_module.load_users()

        result = data_store_module.authenticate_user('admin', '1234')
        assert result is not None
        assert result['is_admin'] is True

    def test_authenticate_user_wrong_password(self, data_store_module):
        """Test authentication with wrong password."""
        data_store_module.load_users()

        result = data_store_module.authenticate_user('admin', 'wrongpass')
        assert result is None

    def test_authenticate_user_nonexistent(self, data_store_module):
        """Test authentication of non-existent user."""
        result = data_store_module.authenticate_user('nobody', 'anypass')
        assert result is None

    def test_user_exists(self, data_store_module):
        """Test checking if user exists."""
        data_store_module.add_user('testuser', 'pass')

        assert data_store_module.user_exists('testuser') is True
        assert data_store_module.user_exists('nonexistent') is False


class TestThreadSafety:
    """Tests for thread safety."""

    def test_concurrent_comment_writes(self, data_store_module):
        """Test concurrent writes to comments don't corrupt data."""
        num_threads = 10
        comments_per_thread = 10
        errors = []

        def add_comments(thread_id):
            try:
                for i in range(comments_per_thread):
                    data_store_module.add_comment(
                        'B001',
                        f'Thread {thread_id} comment {i}',
                        f'user{thread_id}'
                    )
            except Exception as e:
                errors.append(e)

        threads = [
            threading.Thread(target=add_comments, args=(i,))
            for i in range(num_threads)
        ]

        for t in threads:
            t.start()
        for t in threads:
            t.join()

        assert len(errors) == 0, f"Errors occurred: {errors}"

        # Verify all comments were saved
        comments = data_store_module.get_comments('B001')
        assert len(comments) == num_threads * comments_per_thread

    def test_concurrent_user_writes(self, data_store_module):
        """Test concurrent writes to users don't corrupt data."""
        num_threads = 10
        errors = []
        results = []

        def add_user(thread_id):
            try:
                result = data_store_module.add_user(
                    f'user{thread_id}',
                    f'pass{thread_id}',
                    is_admin=False
                )
                results.append((thread_id, result))
            except Exception as e:
                errors.append(e)

        threads = [
            threading.Thread(target=add_user, args=(i,))
            for i in range(num_threads)
        ]

        for t in threads:
            t.start()
        for t in threads:
            t.join()

        assert len(errors) == 0, f"Errors occurred: {errors}"

        # Verify users were created
        users = data_store_module.load_users()
        # Count non-admin users (excluding default admin)
        non_admin_users = sum(1 for k in users if k != 'admin')
        assert non_admin_users == num_threads


class TestDataIntegrity:
    """Tests for data integrity."""

    def test_comments_persist_across_loads(self, data_store_module):
        """Test that comments persist across multiple load calls."""
        data_store_module.add_comment('B001', 'Persistent comment', 'user1')

        # Load multiple times
        comments1 = data_store_module.get_comments('B001')
        comments2 = data_store_module.get_comments('B001')
        comments3 = data_store_module.get_comments('B001')

        assert len(comments1) == 1
        assert comments1 == comments2 == comments3

    def test_users_persist_across_loads(self, data_store_module):
        """Test that users persist across multiple load calls."""
        data_store_module.add_user('persistuser', 'pass', is_admin=False)

        # Load multiple times
        users1 = data_store_module.load_users()
        users2 = data_store_module.load_users()
        users3 = data_store_module.load_users()

        assert 'persistuser' in users1
        assert users1 == users2 == users3

    def test_invalid_json_comments_file(self, data_store_module, temp_data_dir):
        """Test handling of corrupted comments file."""
        # Write invalid JSON
        with open(data_store_module.COMMENTS_FILE, 'w') as f:
            f.write('not valid json {{{')

        # Should return empty dict without crashing
        comments = data_store_module.load_comments()
        assert dict(comments) == {}

    def test_invalid_json_users_file(self, data_store_module, temp_data_dir):
        """Test handling of corrupted users file."""
        # Write invalid JSON
        with open(data_store_module.USERS_FILE, 'w') as f:
            f.write('not valid json {{{')

        # Should return default admin user without crashing
        users = data_store_module.load_users()
        assert 'admin' in users
