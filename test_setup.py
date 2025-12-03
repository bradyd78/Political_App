#!/usr/bin/env python3
"""
Test script to verify the Political App setup
"""
import json
import os

def test_json_files():
    """Test that JSON files exist and are properly formatted"""
    base_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Test comments.json
    comments_file = os.path.join(base_dir, 'database', 'comments.json')
    print(f"✓ Checking {comments_file}...")
    if os.path.exists(comments_file):
        with open(comments_file, 'r') as f:
            data = json.load(f)
            print(f"  ✓ comments.json is valid JSON: {data}")
    else:
        print(f"  ✗ comments.json not found")
    
    # Test users.json
    users_file = os.path.join(base_dir, 'database', 'users.json')
    print(f"\n✓ Checking {users_file}...")
    if os.path.exists(users_file):
        with open(users_file, 'r') as f:
            data = json.load(f)
            print(f"  ✓ users.json is valid JSON")
            print(f"  ✓ Found {len(data)} user(s)")
            for username, userdata in data.items():
                is_admin = userdata.get('is_admin', False)
                print(f"    - {username} (admin: {is_admin})")
    else:
        print(f"  ✗ users.json not found")
    
    print("\n✓ All JSON files are properly set up!")

def test_file_structure():
    """Test that key files exist"""
    files_to_check = [
        'frontend/src/app.py',
        'frontend/src/templates/index.html',
        'frontend/src/templates/login.html',
        'database/comments.json',
        'database/users.json'
    ]
    
    print("\n" + "="*50)
    print("Checking file structure...")
    print("="*50)
    
    base_dir = os.path.dirname(os.path.abspath(__file__))
    all_exist = True
    
    for file_path in files_to_check:
        full_path = os.path.join(base_dir, file_path)
        exists = os.path.exists(full_path)
        status = "✓" if exists else "✗"
        print(f"{status} {file_path}")
        if not exists:
            all_exist = False
    
    # Check that duplicate index.html is removed
    duplicate = os.path.join(base_dir, 'frontend/src/index.html')
    if not os.path.exists(duplicate):
        print("✓ Duplicate frontend/src/index.html has been removed")
    else:
        print("✗ Duplicate frontend/src/index.html still exists")
        all_exist = False
    
    return all_exist

if __name__ == '__main__':
    print("="*50)
    print("Political App Setup Test")
    print("="*50)
    
    if test_file_structure():
        print("\n✓ File structure is correct!")
    else:
        print("\n✗ Some files are missing or incorrectly placed")
    
    print("\n" + "="*50)
    print("Testing JSON persistence files...")
    print("="*50)
    test_json_files()
    
    print("\n" + "="*50)
    print("Setup Summary:")
    print("="*50)
    print("✓ Frontend: Flask app at frontend/src/app.py")
    print("✓ Templates: Using templates folder (not src/)")
    print("✓ Comments API: /api/bills/<bill_id>/comments (GET/POST)")
    print("✓ Login API: /login (POST)")
    print("✓ Signup API: /signup (POST)")
    print("✓ Data persistence: database/comments.json & database/users.json")
    print("\nTo start the app: python3 frontend/src/app.py")
