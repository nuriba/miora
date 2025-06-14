#!/usr/bin/env python3
"""
Comprehensive Backend Testing Script for Miora Platform
Tests all controllers, services, and API endpoints
"""

import requests
import json
import time
import sys
import os
from typing import Dict, Any, Optional

# Configuration
SPRING_BOOT_URL = "http://localhost:8080"
ML_SERVICE_URL = "http://localhost:8000"
AUTH_HEADERS = {}

class MioraBackendTester:
    def __init__(self):
        self.test_results = []
        self.jwt_token = None
        self.test_user_id = None
        self.created_resources = {
            'garments': [],
            'categories': [],
            'sessions': []
        }

    def log_test(self, test_name: str, success: bool, details: str = ""):
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status} | {test_name} | {details}")
        self.test_results.append({
            'test': test_name,
            'success': success,
            'details': details
        })

    def make_request(self, method: str, endpoint: str, data: Dict = None, 
                    files: Dict = None, headers: Dict = None) -> tuple:
        """Make HTTP request and return (success, response_data, status_code)"""
        url = f"{SPRING_BOOT_URL}{endpoint}"
        
        request_headers = {}
        if headers:
            request_headers.update(headers)
        if self.jwt_token:
            request_headers['Authorization'] = f"Bearer {self.jwt_token}"
        
        try:
            if method == 'GET':
                response = requests.get(url, headers=request_headers)
            elif method == 'POST':
                if files:
                    response = requests.post(url, data=data, files=files, headers=request_headers)
                else:
                    request_headers['Content-Type'] = 'application/json'
                    response = requests.post(url, json=data, headers=request_headers)
            elif method == 'PUT':
                request_headers['Content-Type'] = 'application/json'
                response = requests.put(url, json=data, headers=request_headers)
            elif method == 'DELETE':
                response = requests.delete(url, headers=request_headers)
            else:
                return False, None, 0
            
            try:
                return response.status_code < 400, response.json(), response.status_code
            except:
                return response.status_code < 400, response.text, response.status_code
                
        except Exception as e:
            return False, str(e), 0

    def test_service_health(self):
        """Test if both services are running"""
        print("🏥 Testing Service Health...")
        
        # Test Spring Boot service
        success, data, status = self.make_request('GET', '/api/v1/auth/health')
        self.log_test("Spring Boot Health Check", success, f"Status: {status}")
        
        # Test ML service
        try:
            response = requests.get(f"{ML_SERVICE_URL}/health")
            ml_success = response.status_code == 200
            self.log_test("ML Service Health Check", ml_success, f"Status: {response.status_code}")
        except:
            self.log_test("ML Service Health Check", False, "Service not reachable")

    def test_authentication(self):
        """Test user registration and login"""
        print("\n🔐 Testing Authentication...")
        
        # Test user registration
        test_user = {
            "email": f"test_{int(time.time())}@miora.com",
            "password": "TestPassword123!",
            "displayName": "Test User",
            "firstName": "Test",
            "lastName": "User"
        }
        
        success, data, status = self.make_request('POST', '/api/v1/auth/register', test_user)
        self.log_test("User Registration", success, f"Status: {status}")
        
        if success:
            # Test user login
            login_data = {
                "email": test_user["email"],
                "password": test_user["password"]
            }
            
            success, data, status = self.make_request('POST', '/api/v1/auth/login', login_data)
            self.log_test("User Login", success, f"Status: {status}")
            
            if success and 'accessToken' in data:
                self.jwt_token = data['accessToken']
                # Extract user ID from response if available
                if 'user' in data and 'id' in data['user']:
                    self.test_user_id = data['user']['id']
                self.log_test("JWT Token Retrieved", True, "Token stored for subsequent tests")
            else:
                self.log_test("JWT Token Retrieved", False, "No token in response")

    def test_categories(self):
        """Test category management endpoints"""
        print("\n📂 Testing Category Management...")
        
        # Test get all categories
        success, data, status = self.make_request('GET', '/api/v1/categories')
        self.log_test("Get All Categories", success, f"Status: {status}, Count: {len(data) if isinstance(data, list) else 0}")
        
        # Test get top-level categories
        success, data, status = self.make_request('GET', '/api/v1/categories/top-level')
        self.log_test("Get Top-Level Categories", success, f"Status: {status}")
        
        if success and isinstance(data, list) and len(data) > 0:
            category_id = data[0]['id']
            category_slug = data[0]['slug']
            
            # Test get category by ID
            success, data, status = self.make_request('GET', f'/api/v1/categories/{category_id}')
            self.log_test("Get Category by ID", success, f"Status: {status}")
            
            # Test get category by slug
            success, data, status = self.make_request('GET', f'/api/v1/categories/slug/{category_slug}')
            self.log_test("Get Category by Slug", success, f"Status: {status}")
            
            # Test get subcategories
            success, data, status = self.make_request('GET', f'/api/v1/categories/{category_id}/subcategories')
            self.log_test("Get Subcategories", success, f"Status: {status}")
            
            # Test get category hierarchy
            success, data, status = self.make_request('GET', f'/api/v1/categories/{category_id}/hierarchy')
            self.log_test("Get Category Hierarchy", success, f"Status: {status}")
        
        # Test category search
        success, data, status = self.make_request('GET', '/api/v1/categories/search?q=clothing')
        self.log_test("Search Categories", success, f"Status: {status}")
        
        # Test categories with counts
        success, data, status = self.make_request('GET', '/api/v1/categories/with-counts')
        self.log_test("Get Categories with Counts", success, f"Status: {status}")

    def test_file_upload(self):
        """Test file upload functionality"""
        print("\n📁 Testing File Upload...")
        
        if not self.jwt_token:
            self.log_test("File Upload Tests", False, "No JWT token available")
            return
        
        # Test upload limits
        success, data, status = self.make_request('GET', '/api/v1/upload/limits')
        self.log_test("Get Upload Limits", success, f"Status: {status}")
        
        # Create a simple test image file
        test_image_content = b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x02\x00\x00\x00\x90wS\xde\x00\x00\x00\tpHYs\x00\x00\x0b\x13\x00\x00\x0b\x13\x01\x00\x9a\x9c\x18\x00\x00\x00\nIDATx\x9cc\xf8\x00\x00\x00\x01\x00\x01\x00\x00\x00\x00IEND\xaeB`\x82'
        
        # Test file validation
        try:
            files = {'file': ('test.png', test_image_content, 'image/png')}
            headers = {'Authorization': f'Bearer {self.jwt_token}'}
            
            response = requests.post(f"{SPRING_BOOT_URL}/api/v1/upload/validate", 
                                   files=files, headers=headers)
            success = response.status_code < 400
            self.log_test("File Validation", success, f"Status: {response.status_code}")
            
            # Test garment image upload
            response = requests.post(f"{SPRING_BOOT_URL}/api/v1/upload/garment", 
                                   files=files, headers=headers)
            success = response.status_code < 400
            self.log_test("Garment Image Upload", success, f"Status: {response.status_code}")
            
            # Test avatar image upload
            response = requests.post(f"{SPRING_BOOT_URL}/api/v1/upload/avatar", 
                                   files=files, headers=headers)
            success = response.status_code < 400
            self.log_test("Avatar Image Upload", success, f"Status: {response.status_code}")
            
        except Exception as e:
            self.log_test("File Upload Tests", False, f"Error: {str(e)}")

    def test_garment_management(self):
        """Test garment management endpoints"""
        print("\n👗 Testing Garment Management...")
        
        if not self.jwt_token:
            self.log_test("Garment Management Tests", False, "No JWT token available")
            return
        
        # Test get public garments
        success, data, status = self.make_request('GET', '/api/v1/garments/public')
        self.log_test("Get Public Garments", success, f"Status: {status}")
        
        # Test get my garments
        success, data, status = self.make_request('GET', '/api/v1/garments/my-garments')
        self.log_test("Get My Garments", success, f"Status: {status}")
        
        # Test garment discovery endpoints
        success, data, status = self.make_request('GET', '/api/v1/garments/featured')
        self.log_test("Get Featured Garments", success, f"Status: {status}")
        
        success, data, status = self.make_request('GET', '/api/v1/garments/popular')
        self.log_test("Get Popular Garments", success, f"Status: {status}")
        
        success, data, status = self.make_request('GET', '/api/v1/garments/trending')
        self.log_test("Get Trending Garments", success, f"Status: {status}")
        
        # Test garment search
        success, data, status = self.make_request('GET', '/api/v1/garments/search?q=shirt')
        self.log_test("Search Garments", success, f"Status: {status}")
        
        # Test get garments by category (use first category if available)
        cat_success, cat_data, _ = self.make_request('GET', '/api/v1/categories/top-level')
        if cat_success and isinstance(cat_data, list) and len(cat_data) > 0:
            category_id = cat_data[0]['id']
            success, data, status = self.make_request('GET', f'/api/v1/garments/category/{category_id}')
            self.log_test("Get Garments by Category", success, f"Status: {status}")

    def test_try_on_management(self):
        """Test virtual try-on endpoints"""
        print("\n🔄 Testing Virtual Try-On Management...")
        
        if not self.jwt_token:
            self.log_test("Try-On Management Tests", False, "No JWT token available")
            return
        
        # Test get my sessions
        success, data, status = self.make_request('GET', '/api/v1/try-on/my-sessions')
        self.log_test("Get My Try-On Sessions", success, f"Status: {status}")
        
        # Test get saved sessions
        success, data, status = self.make_request('GET', '/api/v1/try-on/my-sessions/saved')
        self.log_test("Get My Saved Sessions", success, f"Status: {status}")
        
        # Test get public sessions
        success, data, status = self.make_request('GET', '/api/v1/try-on/public')
        self.log_test("Get Public Try-On Sessions", success, f"Status: {status}")
        
        # Test get high quality sessions
        success, data, status = self.make_request('GET', '/api/v1/try-on/high-quality')
        self.log_test("Get High Quality Sessions", success, f"Status: {status}")
        
        # Test get statistics
        success, data, status = self.make_request('GET', '/api/v1/try-on/statistics')
        self.log_test("Get Try-On Statistics", success, f"Status: {status}")
        
        # Test check combination
        success, data, status = self.make_request('GET', '/api/v1/try-on/check-combination?avatarId=1&garmentId=1')
        self.log_test("Check Try-On Combination", success, f"Status: {status}")

    def test_integration_workflows(self):
        """Test complex integration workflows"""
        print("\n⚙️ Testing Integration Workflows...")
        
        if not self.jwt_token:
            self.log_test("Integration Tests", False, "No JWT token available")
            return
        
        # Test workflow: Browse categories -> View garments -> Try-on flow
        
        # 1. Get categories
        cat_success, cat_data, _ = self.make_request('GET', '/api/v1/categories/top-level')
        
        if cat_success and isinstance(cat_data, list) and len(cat_data) > 0:
            category_id = cat_data[0]['id']
            
            # 2. Get garments in category
            gar_success, gar_data, _ = self.make_request('GET', f'/api/v1/garments/category/{category_id}')
            
            if gar_success and isinstance(gar_data, list) and len(gar_data) > 0:
                garment_id = gar_data[0]['id']
                
                # 3. Get garment details
                detail_success, _, detail_status = self.make_request('GET', f'/api/v1/garments/{garment_id}')
                self.log_test("Category->Garment Workflow", detail_success, 
                            f"Category {category_id} -> Garment {garment_id}")
                
                # 4. Get similar garments
                sim_success, _, _ = self.make_request('GET', f'/api/v1/garments/{garment_id}/similar')
                self.log_test("Similar Garments Discovery", sim_success, "Found similar items")
            else:
                self.log_test("Category->Garment Workflow", False, "No garments in category")
        else:
            self.log_test("Category->Garment Workflow", False, "No categories found")

    def test_error_handling(self):
        """Test error handling and edge cases"""
        print("\n🚨 Testing Error Handling...")
        
        # Test invalid endpoints
        success, data, status = self.make_request('GET', '/api/v1/invalid-endpoint')
        self.log_test("Invalid Endpoint (404)", status == 404, f"Status: {status}")
        
        # Test unauthorized access
        old_token = self.jwt_token
        self.jwt_token = "invalid-token"
        
        success, data, status = self.make_request('GET', '/api/v1/garments/my-garments')
        self.log_test("Unauthorized Access (401/403)", status in [401, 403], f"Status: {status}")
        
        self.jwt_token = old_token
        
        # Test invalid resource IDs
        success, data, status = self.make_request('GET', '/api/v1/categories/99999')
        self.log_test("Invalid Resource ID (404)", status == 404, f"Status: {status}")

    def run_all_tests(self):
        """Run all test suites"""
        print("🚀 Starting Comprehensive Miora Backend Tests")
        print("=" * 60)
        
        start_time = time.time()
        
        # Run test suites
        self.test_service_health()
        self.test_authentication()
        self.test_categories()
        self.test_file_upload()
        self.test_garment_management()
        self.test_try_on_management()
        self.test_integration_workflows()
        self.test_error_handling()
        
        # Summary
        end_time = time.time()
        duration = end_time - start_time
        
        total_tests = len(self.test_results)
        passed_tests = sum(1 for result in self.test_results if result['success'])
        failed_tests = total_tests - passed_tests
        
        print(f"\n📊 TEST SUMMARY")
        print("=" * 60)
        print(f"Total Tests: {total_tests}")
        print(f"✅ Passed: {passed_tests}")
        print(f"❌ Failed: {failed_tests}")
        print(f"⏱️ Duration: {duration:.2f} seconds")
        print(f"🎯 Success Rate: {(passed_tests/total_tests*100):.1f}%")
        
        if failed_tests > 0:
            print(f"\n❌ FAILED TESTS:")
            for result in self.test_results:
                if not result['success']:
                    print(f"   • {result['test']}: {result['details']}")
        
        return failed_tests == 0

def main():
    """Main test execution"""
    tester = MioraBackendTester()
    
    # Check if services are running
    try:
        response = requests.get(f"{SPRING_BOOT_URL}/api/v1/auth/health", timeout=5)
        if response.status_code != 200:
            print("❌ Spring Boot service is not running on port 8080")
            print("   Please start the service with: ./gradlew bootRun")
            sys.exit(1)
    except:
        print("❌ Cannot connect to Spring Boot service on port 8080")
        print("   Please ensure the service is running")
        sys.exit(1)
    
    # Run tests
    all_passed = tester.run_all_tests()
    
    print(f"\n🏁 Testing Complete!")
    if all_passed:
        print("🎉 All tests passed! Backend is ready for frontend development.")
        sys.exit(0)
    else:
        print("⚠️ Some tests failed. Please review and fix issues before proceeding.")
        sys.exit(1)

if __name__ == "__main__":
    main() 