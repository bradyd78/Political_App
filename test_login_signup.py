#!/usr/bin/env python3
"""
Test script to verify login and signup functionality
"""
import requests
import json

BASE_URL = "http://localhost:5000"

def test_signup():
    """Test user signup"""
    print("\n=== Testing Signup ===")
    
    # Test new user signup
    response = requests.post(
        f"{BASE_URL}/signup",
        json={"username": "testuser123", "password": "testpass123"}
    )
    
    print(f"Signup Response: {response.status_code}")
    print(f"Message: {response.text}")
    
    # Verify user was saved to users.json
    with open('database/users.json', 'r') as f:
        users = json.load(f)
        if 'testuser123' in users:
            print("✓ User successfully saved to users.json")
            print(f"  User data: {users['testuser123']}")
        else:
            print("✗ User NOT found in users.json")
    
    return response.status_code == 200

def test_login():
    """Test user login"""
    print("\n=== Testing Regular User Login ===")
    
    # Test login with the user we just created
    response = requests.post(
        f"{BASE_URL}/login",
        json={"username": "testuser123", "password": "testpass123"}
    )
    
    print(f"Login Response: {response.status_code}")
    data = response.json()
    print(f"Message: {data}")
    
    if data.get('success'):
        print("✓ Login successful")
        print(f"  Is Admin: {data.get('is_admin', False)}")
    else:
        print("✗ Login failed")
    
    return response.status_code == 200 and data.get('success')

def test_admin_login():
    """Test admin login"""
    print("\n=== Testing Admin Login ===")
    
    # Test admin login
    response = requests.post(
        f"{BASE_URL}/login",
        json={"username": "admin", "password": "1234"}
    )
    
    print(f"Login Response: {response.status_code}")
    data = response.json()
    print(f"Message: {data}")
    
    if data.get('success') and data.get('is_admin'):
        print("✓ Admin login successful")
        print(f"  Is Admin: {data.get('is_admin')}")
    else:
        print("✗ Admin login failed or no admin privileges")
    
    return response.status_code == 200 and data.get('success') and data.get('is_admin')

def test_duplicate_signup():
    """Test that duplicate usernames are rejected"""
    print("\n=== Testing Duplicate Username ===")
    
    response = requests.post(
        f"{BASE_URL}/signup",
        json={"username": "testuser123", "password": "different"}
    )
    
    print(f"Duplicate Signup Response: {response.status_code}")
    print(f"Message: {response.text}")
    
    if response.status_code == 400:
        print("✓ Duplicate username correctly rejected")
    else:
        print("✗ Duplicate username was not rejected")
    
    return response.status_code == 400

def test_invalid_login():
    """Test that invalid credentials are rejected"""
    print("\n=== Testing Invalid Login ===")
    
    response = requests.post(
        f"{BASE_URL}/login",
        json={"username": "testuser123", "password": "wrongpassword"}
    )
    
    print(f"Invalid Login Response: {response.status_code}")
    data = response.json()
    print(f"Message: {data}")
    
    if response.status_code == 401 and not data.get('success'):
        print("✓ Invalid credentials correctly rejected")
    else:
        print("✗ Invalid credentials were not rejected")
    
    return response.status_code == 401

if __name__ == "__main__":
    print("=" * 60)
    print("Login and Signup Functionality Tests")
    print("=" * 60)
    
    try:
        # Run all tests
        results = {
            "Signup": test_signup(),
            "Login": test_login(),
            "Admin Login": test_admin_login(),
            "Duplicate Signup": test_duplicate_signup(),
            "Invalid Login": test_invalid_login()
        }
        
        # Print summary
        print("\n" + "=" * 60)
        print("Test Summary")
        print("=" * 60)
        for test_name, passed in results.items():
            status = "✓ PASS" if passed else "✗ FAIL"
            print(f"{test_name}: {status}")
        
        all_passed = all(results.values())
        print("\n" + ("=" * 60))
        if all_passed:
            print("✓ All tests passed!")
        else:
            print("✗ Some tests failed")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n✗ Error running tests: {e}")
        print("Make sure the Flask server is running on http://localhost:5000")
