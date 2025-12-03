"""
Tests for the Flask app routes.
"""

import json
import os
import sys
import tempfile

import pytest


@pytest.fixture
def temp_data_dir():
    """Create a temporary directory for test data files."""
    with tempfile.TemporaryDirectory() as tmpdir:
        yield tmpdir


@pytest.fixture
def app_client(temp_data_dir):
    """Create a Flask test client with temporary file paths."""
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

    import app

    app.app.config['TESTING'] = True
    app.app.config['SECRET_KEY'] = 'test-secret-key'

    with app.app.test_client() as client:
        yield client

    # Restore original paths
    data_store.DATA_DIR = original_data_dir
    data_store.COMMENTS_FILE = original_comments_file
    data_store.USERS_FILE = original_users_file


class TestAuthRoutes:
    """Tests for authentication routes."""

    def test_login_page_get(self, app_client):
        """Test GET /login returns login page."""
        response = app_client.get('/login')
        assert response.status_code == 200

    def test_login_success(self, app_client):
        """Test POST /login with valid credentials."""
        response = app_client.post('/login', json={
            'username': 'admin',
            'password': '1234'
        })
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['success'] is True

    def test_login_invalid_credentials(self, app_client):
        """Test POST /login with invalid credentials."""
        response = app_client.post('/login', json={
            'username': 'admin',
            'password': 'wrongpassword'
        })
        assert response.status_code == 401
        data = json.loads(response.data)
        assert data['success'] is False

    def test_login_missing_credentials(self, app_client):
        """Test POST /login with missing credentials."""
        response = app_client.post('/login', json={})
        assert response.status_code == 400
        data = json.loads(response.data)
        assert data['success'] is False

    def test_signup_success(self, app_client):
        """Test POST /signup with new user."""
        response = app_client.post('/signup', json={
            'username': 'newuser',
            'password': 'newpassword'
        })
        assert response.status_code == 200
        assert b'Signup successful' in response.data

    def test_signup_duplicate_user(self, app_client):
        """Test POST /signup with existing username."""
        # First signup
        app_client.post('/signup', json={
            'username': 'testuser',
            'password': 'pass1'
        })
        # Try duplicate
        response = app_client.post('/signup', json={
            'username': 'testuser',
            'password': 'pass2'
        })
        assert response.status_code == 400

    def test_signup_missing_fields(self, app_client):
        """Test POST /signup with missing fields."""
        response = app_client.post('/signup', json={})
        assert response.status_code == 400


class TestCommentRoutes:
    """Tests for comment routes."""

    def test_get_comments_empty(self, app_client):
        """Test GET /api/bills/<bill_id>/comments returns empty list."""
        response = app_client.get('/api/bills/B001/comments')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data == []

    def test_post_comment(self, app_client):
        """Test POST /api/bills/<bill_id>/comments adds comment."""
        response = app_client.post('/api/bills/B001/comments', json={
            'text': 'Test comment'
        })
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['success'] is True

        # Verify comment was saved
        response = app_client.get('/api/bills/B001/comments')
        data = json.loads(response.data)
        assert len(data) == 1
        assert data[0]['text'] == 'Test comment'

    def test_post_comment_empty_text(self, app_client):
        """Test POST /api/bills/<bill_id>/comments with empty text."""
        response = app_client.post('/api/bills/B001/comments', json={
            'text': ''
        })
        assert response.status_code == 400


class TestBillsRoutes:
    """Tests for bills routes."""

    def test_get_bills(self, app_client):
        """Test GET /api/bills returns bills list."""
        response = app_client.get('/api/bills')
        assert response.status_code == 200
        data = json.loads(response.data)
        # Should return a list (might be empty or have bills depending on billsList.txt)
        assert isinstance(data, list)


class TestHomeRoute:
    """Tests for home route."""

    def test_home_page(self, app_client):
        """Test GET / returns home page."""
        response = app_client.get('/')
        assert response.status_code == 200
