# Miora Backend Testing Plan

## Current Status ✅
- **Python ML Service**: Running on port 8000
- **Spring Boot Service**: Waiting for Maven installation

## Test Scenarios

### 1. Python ML Service Tests (Port 8000)

#### Health Check ✅
```bash
curl http://localhost:8000/health
# Expected: {"status":"healthy","service":"miora-ml-service","version":"1.0.0"}
```

#### API Documentation ✅
```bash
curl http://localhost:8000/docs
# Expected: Swagger UI HTML page
```

#### Avatar Generation (POST)
```bash
# Test with form data (expected format)
curl -X POST http://localhost:8000/api/v1/avatar/generate \
  -F "user_id=123" \
  -F "privacy_level=private" \
  -F "images=@test_image.jpg"
```

#### Size Recommendation (POST)
```bash
curl -X POST http://localhost:8000/api/v1/size/recommend \
  -H "Content-Type: application/json" \
  -d '{
    "user_measurements": {
      "height": 175,
      "weight": 70,
      "chest": 95,
      "waist": 80
    },
    "garment_info": {
      "brand": "nike",
      "category": "shirt",
      "size_chart": "us"
    }
  }'
```

### 2. Spring Boot Service Tests (Port 8080)

#### Health Check
```bash
curl http://localhost:8080/actuator/health
```

#### User Registration
```bash
curl -X POST http://localhost:8080/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "password123",
    "firstName": "John",
    "lastName": "Doe"
  }'
```

#### User Login
```bash
curl -X POST http://localhost:8080/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "password123"
  }'
```

#### Protected Endpoint (with JWT)
```bash
# After login, use the access token
curl -X GET http://localhost:8080/api/v1/avatars \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

### 3. Service Integration Tests

#### Avatar Generation Flow
1. Register/Login to Spring Boot service
2. Get JWT token
3. Call Spring Boot avatar endpoint
4. Spring Boot forwards to ML service
5. ML service processes and returns task ID
6. Check processing status

#### End-to-End User Journey
1. User registration
2. Email verification
3. Login and get tokens
4. Upload avatar images
5. Generate avatar
6. Check avatar status
7. Retrieve avatar data

## Test Data

### Sample User Data
```json
{
  "email": "john.doe@example.com",
  "password": "SecurePass123!",
  "firstName": "John",
  "lastName": "Doe"
}
```

### Sample Avatar Request
```json
{
  "user_id": "1",
  "image_urls": ["https://example.com/photo1.jpg"],
  "privacy_level": "private"
}
```

### Sample Measurements
```json
{
  "height": 175,
  "weight": 70,
  "chest": 95,
  "waist": 80,
  "hip": 95
}
```

## Expected Responses

### Successful Registration
```json
{
  "message": "Registration successful. Please verify your email.",
  "accessToken": null,
  "refreshToken": null
}
```

### Successful Login
```json
{
  "message": "Login successful",
  "accessToken": "eyJ...",
  "refreshToken": "eyJ..."
}
```

### Avatar Generation Started
```json
{
  "task_id": "uuid-string",
  "status": "processing",
  "message": "Avatar generation started"
}
```

## Performance Targets
- Login response: ≤ 1.2s
- Avatar generation start: ≤ 2s
- Health checks: ≤ 100ms
- API documentation load: ≤ 500ms

## Security Tests
- JWT token validation
- CORS policy verification
- Input validation
- SQL injection prevention
- XSS protection 