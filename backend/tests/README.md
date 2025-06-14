# Miora Backend Tests

This directory contains automated test scripts and documentation for testing the Miora backend services.

## Test Scripts

### 1. Bash Test Script (`test_services.sh`)
Simple, dependency-free test script that works on any Unix-like system.

```bash
# Make executable (if needed)
chmod +x test_services.sh

# Run tests
./test_services.sh
```

**Features:**
- ✅ No dependencies (only requires `curl`)
- ✅ Color-coded output
- ✅ Tests both ML and Spring Boot services
- ✅ Performance timing
- ✅ Detailed error reporting

### 2. Python Test Script (`test_services.py`)
Advanced async test script with comprehensive features.

```bash
# Install dependencies
pip install aiohttp

# Run tests
python test_services.py
```

**Features:**
- ✅ Async/concurrent testing
- ✅ Advanced performance metrics
- ✅ Detailed response analysis
- ✅ JSON response validation
- ✅ Timeout handling
- ✅ Test result statistics

## Test Documentation

### `TEST_PLAN.md`
Comprehensive test plan including:
- Test scenarios for both services
- Expected responses
- Performance targets
- Security test cases
- Sample test data

## Quick Start

### Test ML Service Only
```bash
# Check if ML service is running
curl http://localhost:8000/health

# Run ML service tests
./test_services.sh
```

### Test Both Services
```bash
# Start ML service (in one terminal)
cd ../python-ml-service
DEBUG=true python app/main.py

# Start Spring Boot service (in another terminal)
cd ../spring-boot
mvn spring-boot:run

# Run all tests (in third terminal)
cd tests
./test_services.sh
```

## Test Results

### Current Status
- **ML Service**: ✅ All tests passing
- **Spring Boot Service**: ⏳ Waiting for Maven setup

### Performance Benchmarks
- ML Service health check: ~8ms
- API documentation load: ~1ms
- OpenAPI schema: ~1ms

## Adding New Tests

### Bash Script
Add new test cases to `test_services.sh`:

```bash
# Add to test_ml_service() function
test_endpoint "$ML_SERVICE_URL/new-endpoint" "200" "New Endpoint Test"
```

### Python Script
Add new test cases to `test_services.py`:

```python
# Add to test_ml_service() method
TestCase("New Test", f"{self.ml_service_url}/new-endpoint"),
```

## Continuous Integration

These test scripts are designed to be CI/CD friendly:

```yaml
# Example GitHub Actions step
- name: Run Backend Tests
  run: |
    cd backend/tests
    ./test_services.sh
```

## Troubleshooting

### Common Issues

1. **Service not running**
   ```
   ⚠️ Spring Boot service not running on http://localhost:8080
   ```
   **Solution**: Start the service first

2. **Permission denied**
   ```
   bash: ./test_services.sh: Permission denied
   ```
   **Solution**: `chmod +x test_services.sh`

3. **Module not found (Python)**
   ```
   ModuleNotFoundError: No module named 'aiohttp'
   ```
   **Solution**: `pip install aiohttp`

### Debug Mode

Run tests with verbose output:
```bash
# Bash script with debug
bash -x test_services.sh

# Python script with debug
python -v test_services.py
```

## Test Coverage

- [x] Health endpoints
- [x] API documentation
- [x] Authentication flow
- [x] Input validation
- [x] Error handling
- [x] Performance metrics
- [ ] Database operations (requires DB setup)
- [ ] File upload/download
- [ ] Email notifications
- [ ] OAuth integration

## Contributing

When adding new tests:
1. Update both bash and Python scripts
2. Add test cases to `TEST_PLAN.md`
3. Update this README
4. Ensure tests are idempotent
5. Add proper error handling 