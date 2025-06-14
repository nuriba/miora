# Miora Backend - Hybrid Architecture

Virtual Fashion Try-On Platform backend implementation using Spring Boot + Python ML service architecture.

## Architecture Overview

```
┌─────────────────┐    ┌─────────────────────┐    ┌─────────────────┐
│   Frontend      │───▶│   Spring Boot API   │───▶│   PostgreSQL    │
│   (React/Vue)   │    │   Port: 8080        │    │   + Redis       │
└─────────────────┘    │   - Authentication  │    └─────────────────┘
                       │   - User Management │
                       │   - Social Features │
                       │   - Business Logic  │
                       └─────────────────────┘
                                 │
                                 ▼ HTTP/REST
                       ┌─────────────────────┐
                       │   Python ML Service │
                       │   Port: 8000        │
                       │   - Avatar Generation│
                       │   - Garment Analysis │
                       │   - 3D Processing    │
                       │   - Size Recommendations │
                       └─────────────────────┘
```

## Services

### 1. Spring Boot Backend (`spring-boot/`)
- **Port**: 8080
- **Purpose**: Core business logic, authentication, user management, social features
- **Tech Stack**: Spring Boot 3.2, Spring WebFlux, Spring Security, R2DBC, PostgreSQL, Redis
- **Key Features**:
  - JWT authentication with refresh tokens
  - User profile management
  - Avatar and garment metadata storage
  - Social sharing capabilities
  - Communication with ML service

### 2. Python ML Service (`python-ml-service/`)
- **Port**: 8000
- **Purpose**: Machine learning, computer vision, 3D processing
- **Tech Stack**: FastAPI, OpenCV, TensorFlow, Trimesh, Open3D
- **Key Features**:
  - Avatar generation from photos
  - SMPL-X body model integration
  - Garment 3D reconstruction
  - Size recommendation engine
  - Cloth simulation support

## Requirements Coverage

### MVP (Must-Have) Features ✅
- **ACC-01 to ACC-13**: Complete authentication system with OAuth, JWT, 2FA
- **UPR-01 to UPR-10**: User profile management with privacy controls
- **AVR-01 to AVR-13**: Avatar creation and management
- **GIC-01 to GIC-14**: Garment import and processing
- **SRE-01 to SRE-08**: Size recommendation engine
- **VTO-01 to VTO-10**: Virtual try-on support
- **SOC-01 to SOC-10**: Social sharing features

### Performance Targets 🎯
- Login: ≤ 1.2s (ACC-PERF-01)
- Profile operations: ≤ 400ms (UPR-PERF-01)
- Avatar generation: ≤ 10s (AVR-PERF-01)
- Size recommendations: ≤ 300ms (SRE-PERF-01)

## Quick Start

### Prerequisites
- Docker & Docker Compose
- Java 21+ (for local development)
- Python 3.9+ (for local development)
- Node.js 18+ (for frontend)

### 1. Clone and Setup
```bash
git clone <repository-url>
cd miora/backend
```

### 2. Environment Configuration
```bash
# Copy environment template
cp .env.example .env

# Edit environment variables
nano .env
```

### 3. Start All Services
```bash
# Start complete stack
docker-compose up -d

# Or for development with logs
docker-compose up
```

### 4. Initialize Database
```bash
# Run database migrations
docker-compose exec miora-backend ./mvnw flyway:migrate
```

### 5. Verify Services
```bash
# Check all services are healthy
docker-compose ps

# Test endpoints
curl http://localhost:8080/health  # Spring Boot
curl http://localhost:8000/health  # Python ML Service
```

## API Documentation

### Spring Boot API
- **Swagger UI**: http://localhost:8080/swagger-ui.html
- **API Docs**: http://localhost:8080/v3/api-docs

### Python ML Service API
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## Development Setup

### Spring Boot Local Development
```bash
cd spring-boot/

# Install dependencies
./mvnw clean install

# Run locally (requires PostgreSQL and Redis)
./mvnw spring-boot:run
```

### Python ML Service Local Development
```bash
cd python-ml-service/

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt

# Run locally
uvicorn app.main:app --reload --port 8000
```

## Configuration

### Environment Variables

#### Spring Boot
- `DB_HOST`, `DB_PORT`, `DB_NAME`: Database connection
- `REDIS_HOST`, `REDIS_PORT`: Redis connection
- `JWT_SECRET`: JWT signing secret
- `ML_SERVICE_URL`: Python ML service URL
- `GOOGLE_CLIENT_ID`, `GOOGLE_CLIENT_SECRET`: OAuth credentials

#### Python ML Service
- `REDIS_URL`: Redis connection string
- `SPRING_BOOT_BASE_URL`: Spring Boot service URL
- `MODEL_CACHE_DIR`: ML model storage directory
- `USE_GPU`: Enable GPU acceleration

## Production Deployment

### 1. Security Checklist
- [ ] Change default passwords and secrets
- [ ] Configure SSL/TLS certificates
- [ ] Set up firewall rules
- [ ] Enable security monitoring

### 2. Scaling Considerations
- [ ] Use load balancer for Spring Boot instances
- [ ] Scale Python ML service based on processing load
- [ ] Configure Redis clustering for high availability
- [ ] Set up database read replicas

### 3. Monitoring
- [ ] Prometheus metrics: http://localhost:8080/actuator/prometheus
- [ ] Application logs via Docker logging driver
- [ ] Health check endpoints for load balancer

## Testing

### Automated Test Suite
The project includes comprehensive automated test scripts in the `tests/` directory:

```bash
# Quick test (bash script - no dependencies)
cd tests/
./test_services.sh

# Advanced test (Python script - requires aiohttp)
cd tests/
pip install aiohttp
python test_services.py
```

**Test Features:**
- ✅ Health endpoint validation
- ✅ API documentation checks
- ✅ Input validation testing
- ✅ Performance benchmarking
- ✅ Error handling verification
- ✅ Concurrent request testing

### Unit Tests
```bash
# Spring Boot
cd spring-boot/
./mvnw test

# Python ML Service
cd python-ml-service/
pytest
```

### Integration Tests
```bash
# Start test environment
docker-compose -f docker-compose.test.yml up -d

# Run comprehensive test suite
cd tests/
./test_services.sh
```

### Test Documentation
See `tests/README.md` for detailed testing instructions and `tests/TEST_PLAN.md` for comprehensive test scenarios.

## Troubleshooting

### Common Issues

1. **Services not starting**: Check Docker logs with `docker-compose logs <service-name>`
2. **Database connection issues**: Verify PostgreSQL is running and credentials are correct
3. **ML processing failures**: Check GPU availability and model file permissions
4. **High memory usage**: Adjust JVM heap size and Python worker processes

### Debug Commands
```bash
# View service logs
docker-compose logs -f miora-backend
docker-compose logs -f miora-ml-service

# Connect to containers
docker-compose exec miora-backend bash
docker-compose exec miora-ml-service bash

# Check resource usage
docker stats
```

## Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Commit changes: `git commit -m 'Add amazing feature'`
4. Push to branch: `git push origin feature/amazing-feature`
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Support

For support and questions:
- Create an issue in the repository
- Check the [documentation](docs/)
- Contact the development team

---

**Status**: 🚧 MVP Development Phase
**Last Updated**: December 2024 