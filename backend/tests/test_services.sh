#!/bin/bash

# Miora Backend Services Test Script
# Tests both Python ML Service and Spring Boot Service

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
ML_SERVICE_URL="http://localhost:8000"
SPRING_SERVICE_URL="http://localhost:8080"
TEST_EMAIL="test@miora.com"
TEST_PASSWORD="TestPass123!"

# Helper functions
print_header() {
    echo -e "\n${BLUE}=== $1 ===${NC}"
}

print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

test_endpoint() {
    local url=$1
    local expected_status=$2
    local description=$3
    
    echo -n "Testing $description... "
    
    response=$(curl -s -w "%{http_code}" -o /tmp/response.json "$url")
    status_code="${response: -3}"
    
    if [ "$status_code" = "$expected_status" ]; then
        print_success "PASSED (Status: $status_code)"
        return 0
    else
        print_error "FAILED (Expected: $expected_status, Got: $status_code)"
        echo "Response: $(cat /tmp/response.json)"
        return 1
    fi
}

test_post_endpoint() {
    local url=$1
    local data=$2
    local expected_status=$3
    local description=$4
    
    echo -n "Testing $description... "
    
    response=$(curl -s -w "%{http_code}" -o /tmp/response.json \
        -X POST \
        -H "Content-Type: application/json" \
        -d "$data" \
        "$url")
    status_code="${response: -3}"
    
    if [ "$status_code" = "$expected_status" ]; then
        print_success "PASSED (Status: $status_code)"
        cat /tmp/response.json | jq . 2>/dev/null || cat /tmp/response.json
        return 0
    else
        print_error "FAILED (Expected: $expected_status, Got: $status_code)"
        echo "Response: $(cat /tmp/response.json)"
        return 1
    fi
}

# Test ML Service
test_ml_service() {
    print_header "Testing Python ML Service ($ML_SERVICE_URL)"
    
    # Test health endpoint
    test_endpoint "$ML_SERVICE_URL/health" "200" "Health Check"
    
    # Test API documentation
    test_endpoint "$ML_SERVICE_URL/docs" "200" "API Documentation"
    
    # Test OpenAPI schema
    test_endpoint "$ML_SERVICE_URL/openapi.json" "200" "OpenAPI Schema"
    
    # Test size recommendation endpoint (should fail without proper data)
    test_post_endpoint "$ML_SERVICE_URL/api/v1/size/recommend" \
        '{"test": "data"}' \
        "422" \
        "Size Recommendation (validation error expected)"
    
    print_success "ML Service tests completed"
}

# Test Spring Boot Service
test_spring_service() {
    print_header "Testing Spring Boot Service ($SPRING_SERVICE_URL)"
    
    # Check if service is running
    if ! curl -s "$SPRING_SERVICE_URL/actuator/health" > /dev/null 2>&1; then
        print_warning "Spring Boot service not running on $SPRING_SERVICE_URL"
        return 1
    fi
    
    # Test health endpoint
    test_endpoint "$SPRING_SERVICE_URL/actuator/health" "200" "Actuator Health Check"
    
    # Test auth health endpoint
    test_endpoint "$SPRING_SERVICE_URL/api/v1/auth/health" "200" "Auth Health Check"
    
    # Test user registration
    local registration_data='{
        "email": "'$TEST_EMAIL'",
        "password": "'$TEST_PASSWORD'",
        "firstName": "Test",
        "lastName": "User"
    }'
    
    test_post_endpoint "$SPRING_SERVICE_URL/api/v1/auth/register" \
        "$registration_data" \
        "200" \
        "User Registration"
    
    # Test user login
    local login_data='{
        "email": "'$TEST_EMAIL'",
        "password": "'$TEST_PASSWORD'"
    }'
    
    test_post_endpoint "$SPRING_SERVICE_URL/api/v1/auth/login" \
        "$login_data" \
        "200" \
        "User Login"
    
    print_success "Spring Boot Service tests completed"
}

# Test service integration
test_integration() {
    print_header "Testing Service Integration"
    
    # Check if both services are running
    if curl -s "$ML_SERVICE_URL/health" > /dev/null && curl -s "$SPRING_SERVICE_URL/actuator/health" > /dev/null; then
        print_success "Both services are running"
        
        # Test communication between services
        echo "Testing inter-service communication..."
        # This would test Spring Boot calling ML service
        
    else
        print_warning "Cannot test integration - one or both services not running"
    fi
}

# Performance tests
test_performance() {
    print_header "Performance Tests"
    
    echo "Testing ML Service response times..."
    time curl -s "$ML_SERVICE_URL/health" > /dev/null
    
    if curl -s "$SPRING_SERVICE_URL/actuator/health" > /dev/null 2>&1; then
        echo "Testing Spring Boot Service response times..."
        time curl -s "$SPRING_SERVICE_URL/actuator/health" > /dev/null
    fi
}

# Main execution
main() {
    print_header "Miora Backend Services Test Suite"
    echo "Starting automated tests..."
    
    # Test ML Service
    test_ml_service
    
    # Test Spring Boot Service
    test_spring_service
    
    # Test Integration
    test_integration
    
    # Performance Tests
    test_performance
    
    print_header "Test Summary"
    print_success "All tests completed!"
    echo "Check individual test results above for details."
}

# Check dependencies
check_dependencies() {
    command -v curl >/dev/null 2>&1 || { print_error "curl is required but not installed."; exit 1; }
    command -v jq >/dev/null 2>&1 || print_warning "jq not found - JSON output will be raw"
}

# Run tests
check_dependencies
main 