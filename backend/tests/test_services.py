#!/usr/bin/env python3
"""
Miora Backend Services Test Suite
Advanced Python-based testing for both ML and Spring Boot services
"""

import asyncio
import aiohttp
import json
import time
import sys
from typing import Dict, Any, Optional
from dataclasses import dataclass
from enum import Enum

class TestResult(Enum):
    PASS = "PASS"
    FAIL = "FAIL"
    SKIP = "SKIP"

@dataclass
class TestCase:
    name: str
    url: str
    method: str = "GET"
    data: Optional[Dict[str, Any]] = None
    headers: Optional[Dict[str, str]] = None
    expected_status: int = 200
    timeout: float = 5.0

class Colors:
    RED = '\033[0;31m'
    GREEN = '\033[0;32m'
    YELLOW = '\033[1;33m'
    BLUE = '\033[0;34m'
    PURPLE = '\033[0;35m'
    CYAN = '\033[0;36m'
    NC = '\033[0m'  # No Color

class TestRunner:
    def __init__(self):
        self.ml_service_url = "http://localhost:8000"
        self.spring_service_url = "http://localhost:8080"
        self.test_results = []
        self.access_token = None
        
    def print_header(self, text: str):
        print(f"\n{Colors.BLUE}=== {text} ==={Colors.NC}")
        
    def print_success(self, text: str):
        print(f"{Colors.GREEN}✅ {text}{Colors.NC}")
        
    def print_error(self, text: str):
        print(f"{Colors.RED}❌ {text}{Colors.NC}")
        
    def print_warning(self, text: str):
        print(f"{Colors.YELLOW}⚠️  {text}{Colors.NC}")
        
    def print_info(self, text: str):
        print(f"{Colors.CYAN}ℹ️  {text}{Colors.NC}")

    async def run_test(self, session: aiohttp.ClientSession, test_case: TestCase) -> TestResult:
        """Run a single test case"""
        try:
            start_time = time.time()
            
            kwargs = {
                'timeout': aiohttp.ClientTimeout(total=test_case.timeout),
                'headers': test_case.headers or {}
            }
            
            if test_case.data:
                kwargs['json'] = test_case.data
                
            async with session.request(test_case.method, test_case.url, **kwargs) as response:
                response_time = time.time() - start_time
                response_data = await response.text()
                
                # Try to parse as JSON
                try:
                    response_json = json.loads(response_data)
                except:
                    response_json = response_data
                
                if response.status == test_case.expected_status:
                    self.print_success(f"{test_case.name} - {response.status} ({response_time:.3f}s)")
                    if isinstance(response_json, dict) and len(str(response_json)) < 200:
                        print(f"   Response: {response_json}")
                    return TestResult.PASS
                else:
                    self.print_error(f"{test_case.name} - Expected {test_case.expected_status}, got {response.status}")
                    print(f"   Response: {response_json}")
                    return TestResult.FAIL
                    
        except asyncio.TimeoutError:
            self.print_error(f"{test_case.name} - Timeout after {test_case.timeout}s")
            return TestResult.FAIL
        except Exception as e:
            self.print_error(f"{test_case.name} - Error: {str(e)}")
            return TestResult.FAIL

    async def test_ml_service(self, session: aiohttp.ClientSession):
        """Test Python ML Service"""
        self.print_header("Testing Python ML Service")
        
        test_cases = [
            TestCase("Health Check", f"{self.ml_service_url}/health"),
            TestCase("API Documentation", f"{self.ml_service_url}/docs"),
            TestCase("OpenAPI Schema", f"{self.ml_service_url}/openapi.json"),
            TestCase(
                "Size Recommendation (Invalid Data)", 
                f"{self.ml_service_url}/api/v1/size/recommend",
                method="POST",
                data={"test": "data"},
                expected_status=422
            ),
        ]
        
        results = []
        for test_case in test_cases:
            result = await self.run_test(session, test_case)
            results.append(result)
            
        return results

    async def test_spring_service(self, session: aiohttp.ClientSession):
        """Test Spring Boot Service"""
        self.print_header("Testing Spring Boot Service")
        
        # Check if service is running first
        try:
            async with session.get(f"{self.spring_service_url}/actuator/health", 
                                 timeout=aiohttp.ClientTimeout(total=2)) as response:
                if response.status != 200:
                    self.print_warning("Spring Boot service not responding")
                    return [TestResult.SKIP]
        except:
            self.print_warning("Spring Boot service not running")
            return [TestResult.SKIP]
        
        test_cases = [
            TestCase("Actuator Health", f"{self.spring_service_url}/actuator/health"),
            TestCase("Auth Health", f"{self.spring_service_url}/api/v1/auth/health"),
        ]
        
        results = []
        for test_case in test_cases:
            result = await self.run_test(session, test_case)
            results.append(result)
            
        # Test user registration
        registration_data = {
            "email": "test@miora.com",
            "password": "TestPass123!",
            "firstName": "Test",
            "lastName": "User"
        }
        
        reg_test = TestCase(
            "User Registration",
            f"{self.spring_service_url}/api/v1/auth/register",
            method="POST",
            data=registration_data,
            headers={"Content-Type": "application/json"}
        )
        
        result = await self.run_test(session, reg_test)
        results.append(result)
        
        # Test user login
        login_data = {
            "email": "test@miora.com",
            "password": "TestPass123!"
        }
        
        login_test = TestCase(
            "User Login",
            f"{self.spring_service_url}/api/v1/auth/login",
            method="POST",
            data=login_data,
            headers={"Content-Type": "application/json"}
        )
        
        result = await self.run_test(session, login_test)
        results.append(result)
        
        return results

    async def test_performance(self, session: aiohttp.ClientSession):
        """Test service performance"""
        self.print_header("Performance Tests")
        
        # Test ML service performance
        self.print_info("Testing ML Service response times...")
        times = []
        for i in range(5):
            start = time.time()
            try:
                async with session.get(f"{self.ml_service_url}/health") as response:
                    if response.status == 200:
                        times.append(time.time() - start)
            except:
                pass
                
        if times:
            avg_time = sum(times) / len(times)
            self.print_info(f"ML Service avg response time: {avg_time:.3f}s")
            
        # Test Spring Boot service performance if running
        try:
            async with session.get(f"{self.spring_service_url}/actuator/health", 
                                 timeout=aiohttp.ClientTimeout(total=2)) as response:
                if response.status == 200:
                    self.print_info("Testing Spring Boot Service response times...")
                    times = []
                    for i in range(5):
                        start = time.time()
                        try:
                            async with session.get(f"{self.spring_service_url}/actuator/health") as resp:
                                if resp.status == 200:
                                    times.append(time.time() - start)
                        except:
                            pass
                    
                    if times:
                        avg_time = sum(times) / len(times)
                        self.print_info(f"Spring Boot Service avg response time: {avg_time:.3f}s")
        except:
            self.print_warning("Spring Boot service not available for performance testing")

    async def run_all_tests(self):
        """Run all test suites"""
        self.print_header("Miora Backend Services Test Suite")
        self.print_info("Starting automated tests...")
        
        async with aiohttp.ClientSession() as session:
            # Test ML Service
            ml_results = await self.test_ml_service(session)
            
            # Test Spring Boot Service
            spring_results = await self.test_spring_service(session)
            
            # Performance Tests
            await self.test_performance(session)
            
            # Summary
            self.print_header("Test Summary")
            
            total_tests = len(ml_results) + len(spring_results)
            passed_tests = sum(1 for r in ml_results + spring_results if r == TestResult.PASS)
            failed_tests = sum(1 for r in ml_results + spring_results if r == TestResult.FAIL)
            skipped_tests = sum(1 for r in ml_results + spring_results if r == TestResult.SKIP)
            
            self.print_info(f"Total tests: {total_tests}")
            self.print_success(f"Passed: {passed_tests}")
            if failed_tests > 0:
                self.print_error(f"Failed: {failed_tests}")
            if skipped_tests > 0:
                self.print_warning(f"Skipped: {skipped_tests}")
                
            if failed_tests == 0:
                self.print_success("All tests passed! 🎉")
                return 0
            else:
                self.print_error("Some tests failed!")
                return 1

async def main():
    """Main entry point"""
    runner = TestRunner()
    exit_code = await runner.run_all_tests()
    sys.exit(exit_code)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print(f"\n{Colors.YELLOW}Tests interrupted by user{Colors.NC}")
        sys.exit(1) 