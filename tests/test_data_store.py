"""
Tests for the data_store module.
"""

import json
import os
import shutil
import sys
import tempfile
import unittest

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

import data_store


class TestDataStore(unittest.TestCase):
    """Test cases for the data_store module."""

    def setUp(self):
        """Set up test fixtures with a temporary data directory."""
        self.test_dir = tempfile.mkdtemp()
        self.original_data_dir = data_store.DATA_DIR
        self.original_comments_file = data_store.COMMENTS_FILE
        self.original_users_file = data_store.USERS_FILE

        # Override data paths to use temp directory
        data_store.DATA_DIR = self.test_dir
        data_store.COMMENTS_FILE = os.path.join(self.test_dir, 'comments.json')
        data_store.USERS_FILE = os.path.join(self.test_dir, 'users.json')

    def tearDown(self):
        """Clean up test fixtures."""
        # Restore original paths
        data_store.DATA_DIR = self.original_data_dir
        data_store.COMMENTS_FILE = self.original_comments_file
        data_store.USERS_FILE = self.original_users_file

        # Remove temp directory
        shutil.rmtree(self.test_dir, ignore_errors=True)

    # =========================================================================
    # Comments Tests
    # =========================================================================

    def test_load_comments_empty(self):
        """Test loading comments when no file exists."""
        comments = data_store.load_comments()
        self.assertEqual(comments, {})

    def test_save_and_load_comments(self):
        """Test saving and loading comments."""
        test_comments = {
            'B001': [
                {'text': 'Test comment', 'user': 'testuser', 'timestamp': '2024-01-01T00:00:00Z'}
            ]
        }
        data_store.save_comments(test_comments)
        loaded = data_store.load_comments()
        self.assertEqual(loaded, test_comments)

    def test_add_comment(self):
        """Test adding a comment to a bill."""
        comment = data_store.add_comment('B001', 'testuser', 'This is a test comment')

        self.assertEqual(comment['text'], 'This is a test comment')
        self.assertEqual(comment['user'], 'testuser')
        self.assertIn('timestamp', comment)

        # Verify comment was persisted
        comments = data_store.load_comments()
        self.assertEqual(len(comments['B001']), 1)
        self.assertEqual(comments['B001'][0]['text'], 'This is a test comment')

    def test_add_multiple_comments_same_bill(self):
        """Test adding multiple comments to the same bill."""
        data_store.add_comment('B001', 'user1', 'First comment')
        data_store.add_comment('B001', 'user2', 'Second comment')

        comments = data_store.get_comments_for_bill('B001')
        self.assertEqual(len(comments), 2)

    def test_get_comments_for_bill(self):
        """Test getting comments for a specific bill."""
        data_store.add_comment('B001', 'user1', 'Comment on B001')
        data_store.add_comment('B002', 'user2', 'Comment on B002')

        comments_b001 = data_store.get_comments_for_bill('B001')
        self.assertEqual(len(comments_b001), 1)
        self.assertEqual(comments_b001[0]['text'], 'Comment on B001')

        comments_b002 = data_store.get_comments_for_bill('B002')
        self.assertEqual(len(comments_b002), 1)
        self.assertEqual(comments_b002[0]['text'], 'Comment on B002')

    def test_get_comments_for_nonexistent_bill(self):
        """Test getting comments for a bill with no comments."""
        comments = data_store.get_comments_for_bill('NONEXISTENT')
        self.assertEqual(comments, [])

    # =========================================================================
    # Users Tests
    # =========================================================================

    def test_load_users_empty(self):
        """Test loading users when no file exists."""
        users = data_store.load_users()
        self.assertEqual(users, {})

    def test_create_user(self):
        """Test creating a new user."""
        user = data_store.create_user('testuser', 'testpass123')

        self.assertEqual(user['username'], 'testuser')
        self.assertEqual(user['display_name'], 'testuser')
        self.assertFalse(user['is_admin'])
        self.assertIn('created_at', user)

        # Verify user was persisted with hashed password
        users = data_store.load_users()
        self.assertIn('testuser', users)
        self.assertTrue(users['testuser']['password_hash'].startswith('$2'))

    def test_create_user_with_display_name(self):
        """Test creating a user with a custom display name."""
        user = data_store.create_user('testuser', 'testpass', display_name='Test User')
        self.assertEqual(user['display_name'], 'Test User')

    def test_create_duplicate_user(self):
        """Test that creating a duplicate user raises an error."""
        data_store.create_user('testuser', 'pass1')

        with self.assertRaises(ValueError) as context:
            data_store.create_user('testuser', 'pass2')

        self.assertIn('already exists', str(context.exception))

    def test_authenticate_user_success(self):
        """Test successful user authentication."""
        data_store.create_user('testuser', 'correctpass')
        result = data_store.authenticate_user('testuser', 'correctpass')

        self.assertIsNotNone(result)
        self.assertEqual(result['username'], 'testuser')

    def test_authenticate_user_wrong_password(self):
        """Test authentication with wrong password."""
        data_store.create_user('testuser', 'correctpass')
        result = data_store.authenticate_user('testuser', 'wrongpass')

        self.assertIsNone(result)

    def test_authenticate_nonexistent_user(self):
        """Test authentication for a user that doesn't exist."""
        result = data_store.authenticate_user('nonexistent', 'anypass')
        self.assertIsNone(result)

    def test_authenticate_legacy_plaintext_password(self):
        """Test authentication with legacy plaintext password."""
        # Manually create a user with plaintext password (legacy format)
        users = {'legacyuser': {'password': 'plainpass', 'is_admin': False}}
        data_store.save_users(users)

        result = data_store.authenticate_user('legacyuser', 'plainpass')
        self.assertIsNotNone(result)
        self.assertEqual(result['username'], 'legacyuser')

    def test_update_password(self):
        """Test updating a user's password."""
        data_store.create_user('testuser', 'oldpass')

        # Update password
        result = data_store.update_password('testuser', 'newpass')
        self.assertTrue(result)

        # Verify old password no longer works
        self.assertIsNone(data_store.authenticate_user('testuser', 'oldpass'))

        # Verify new password works
        self.assertIsNotNone(data_store.authenticate_user('testuser', 'newpass'))

    def test_update_password_nonexistent_user(self):
        """Test updating password for nonexistent user."""
        result = data_store.update_password('nonexistent', 'newpass')
        self.assertFalse(result)

    def test_save_and_load_users(self):
        """Test saving and loading users directly."""
        test_users = {
            'user1': {
                'password_hash': '$2b$12$somehash',
                'display_name': 'User One',
                'is_admin': False,
                'created_at': '2024-01-01T00:00:00Z'
            }
        }
        data_store.save_users(test_users)
        loaded = data_store.load_users()
        self.assertEqual(loaded, test_users)


if __name__ == '__main__':
    unittest.main()
