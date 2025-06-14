#!/usr/bin/env python3
"""
Focused test script for failing scenarios in Miora Backend
"""

import requests
import json
import tempfile
import os

# Configuration
API_BASE_URL = "http://localhost:8080"
ML_SERVICE_URL = "http://localhost:8000"

def test_authentication_issues():
    """Test authentication problems"""
    print("🔐 Testing Authentication Issues...")
    
    # Test 1: Registration
    user_data = {
        "email": "test@miora.com",
        "password": "TestPassword123!",
        "firstName": "Test",
        "lastName": "User"
    }
    
    print("\n1. Testing Registration:")
    try:
        response = requests.post(f"{API_BASE_URL}/api/v1/auth/register", 
                               json=user_data, timeout=10)
        print(f"   Registration Status: {response.status_code}")
        print(f"   Response: {response.text[:200]}")
    except Exception as e:
        print(f"   Registration Error: {e}")
    
    # Test 2: Login
    login_data = {
        "email": user_data["email"],
        "password": user_data["password"]
    }
    
    print("\n2. Testing Login:")
    try:
        response = requests.post(f"{API_BASE_URL}/api/v1/auth/login", 
                               json=login_data, timeout=10)
        print(f"   Login Status: {response.status_code}")
        print(f"   Response: {response.text[:200]}")
        
        if response.status_code == 200:
            data = response.json()
            token = data.get("accessToken") or data.get("token")  # Handle both field names
            print(f"   Token extracted: {token[:20] if token else 'None'}...")
            return token
    except Exception as e:
        print(f"   Login Error: {e}")
    
    return None

def test_file_upload_endpoints(token):
    """Test file upload failing scenarios"""
    print("\n📁 Testing File Upload Issues...")
    
    if not token:
        print("   No token available - skipping file upload tests")
        return
        
    headers = {"Authorization": f"Bearer {token}"}
    
    # Test 1: File validation without file
    print("\n1. Testing File Validation:")
    try:
        response = requests.post(f"{API_BASE_URL}/api/v1/upload/validate", 
                               headers=headers, timeout=10)
        print(f"   Validation Status: {response.status_code}")
        print(f"   Response: {response.text[:200]}")
    except Exception as e:
        print(f"   Validation Error: {e}")
    
    # Test 2: Garment image upload without proper multipart
    print("\n2. Testing Garment Image Upload:")
    try:
        # This should fail with 415 - testing incorrect content type
        response = requests.post(f"{API_BASE_URL}/api/v1/upload/garment", 
                               headers=headers, 
                               json={"test": "data"}, 
                               timeout=10)
        print(f"   Garment Upload Status: {response.status_code}")
        print(f"   Response: {response.text[:200]}")
    except Exception as e:
        print(f"   Garment Upload Error: {e}")
    
    # Test 3: Avatar image upload without proper multipart
    print("\n3. Testing Avatar Image Upload:")
    try:
        # This should fail with 415 - testing incorrect content type
        response = requests.post(f"{API_BASE_URL}/api/v1/upload/avatar", 
                               headers=headers, 
                               json={"test": "data"}, 
                               timeout=10)
        print(f"   Avatar Upload Status: {response.status_code}")
        print(f"   Response: {response.text[:200]}")
    except Exception as e:
        print(f"   Avatar Upload Error: {e}")

def test_garment_workflow(token):
    """Test category->garment workflow"""
    print("\n👗 Testing Category->Garment Workflow...")
    
    if not token:
        print("   No token available - skipping workflow tests")
        return
        
    headers = {"Authorization": f"Bearer {token}"}
    
    # Test 1: Get categories
    print("\n1. Testing Get Categories:")
    try:
        response = requests.get(f"{API_BASE_URL}/api/v1/categories", 
                              headers=headers, timeout=10)
        print(f"   Categories Status: {response.status_code}")
        if response.status_code == 200:
            categories = response.json()
            print(f"   Categories Count: {len(categories)}")
            if categories:
                first_category = categories[0]
                print(f"   First Category: {first_category.get('name')} (ID: {first_category.get('id')})")
                
                # Test 2: Get garments for category
                print("\n2. Testing Get Garments by Category:")
                category_id = first_category.get('id')
                response = requests.get(f"{API_BASE_URL}/api/v1/garments/category/{category_id}", 
                                      headers=headers, timeout=10)
                print(f"   Garments by Category Status: {response.status_code}")
                if response.status_code == 200:
                    garments = response.json()
                    print(f"   Garments Count: {len(garments)}")
                    if not garments:
                        print("   ⚠️  No garments found in category - this explains the workflow failure")
                else:
                    print(f"   Response: {response.text[:200]}")
        else:
            print(f"   Response: {response.text[:200]}")
    except Exception as e:
        print(f"   Categories Error: {e}")

def test_unauthorized_access():
    """Test unauthorized access scenarios"""
    print("\n🚫 Testing Unauthorized Access...")
    
    # Test 1: Access protected endpoint without token
    print("\n1. Testing No Token:")
    try:
        response = requests.get(f"{API_BASE_URL}/api/v1/garments/my", timeout=10)
        print(f"   No Token Status: {response.status_code}")
        print(f"   Response: {response.text[:200]}")
    except Exception as e:
        print(f"   No Token Error: {e}")
    
    # Test 2: Access with invalid token
    print("\n2. Testing Invalid Token:")
    try:
        headers = {"Authorization": "Bearer invalid_token_here"}
        response = requests.get(f"{API_BASE_URL}/api/v1/garments/my", 
                              headers=headers, timeout=10)
        print(f"   Invalid Token Status: {response.status_code}")
        print(f"   Response: {response.text[:200]}")
    except Exception as e:
        print(f"   Invalid Token Error: {e}")
    
    # Test 3: Access with expired token (simulate)
    print("\n3. Testing Expired Token:")
    try:
        # Using a malformed JWT that should cause authentication failure
        expired_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c"
        headers = {"Authorization": f"Bearer {expired_token}"}
        response = requests.get(f"{API_BASE_URL}/api/v1/garments/my", 
                              headers=headers, timeout=10)
        print(f"   Expired Token Status: {response.status_code}")
        print(f"   Response: {response.text[:200]}")
    except Exception as e:
        print(f"   Expired Token Error: {e}")

def main():
    """Main test runner for failing scenarios"""
    print("🚨 Focused Testing: Failing Scenarios")
    print("="*50)
    
    # Test authentication issues
    token = test_authentication_issues()
    
    # Test file upload issues
    test_file_upload_endpoints(token)
    
    # Test garment workflow
    test_garment_workflow(token)
    
    # Test unauthorized access
    test_unauthorized_access()
    
    print("\n" + "="*50)
    print("🏁 Focused Testing Complete")

if __name__ == "__main__":
    main() 