# Miora Backend API

Virtual Fashion Try-On Platform - Django REST API

## 🚀 Features

- **User Authentication**: JWT-based authentication with OAuth support
- **Avatar Management**: 3D avatar creation from photos or manual measurements
- **Garment Processing**: AI-powered garment digitization and 3D model generation
- **Virtual Try-On**: Physics-based cloth simulation for realistic fit visualization
- **Size Recommendations**: ML-based size prediction with 90%+ accuracy
- **Analytics Dashboard**: Anonymous brand analytics and insights
- **RESTful API**: Well-documented API with OpenAPI/Swagger support

## 📋 Prerequisites

- Python 3.11+
- PostgreSQL 14+
- Redis 6+
- Node.js 18+ (for frontend development)

## 🛠️ Installation

### 1. Navigate to backend directory
```bash
cd backend
```

### 2. Activate virtual environment
```bash
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Set up environment variables
```bash
cp .env.example .env
# Edit .env with your configuration
```

### 5. Set up database
```bash
# Create PostgreSQL database
createdb miora_db

# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser
```

### 6. Load sample data (optional)
```bash
python manage.py create_test_users
python create_sample_data.py
```

### 7. Run development server
```bash
python manage.py runserver
```

## 🐳 Docker Setup

### Using Docker Compose
```bash
# Build and start all services
docker-compose up --build

# Run migrations
docker-compose exec backend python manage.py migrate

# Create superuser
docker-compose exec backend python manage.py createsuperuser
```

### Production Docker
```bash
# Build production image
docker build -f Dockerfile -t miora-backend:latest .

# Run with environment variables
docker run -d \
  --name miora-backend \
  -p 8000:8000 \
  --env-file .env \
  miora-backend:latest
```

## 📚 API Documentation

### Interactive Documentation
- Swagger UI: http://localhost:8000/api/docs/
- ReDoc: http://localhost:8000/api/redoc/
- Admin Panel: http://localhost:8000/admin/

### Default Test Accounts
- Admin: `admin@miora.com` / `admin123`
- Demo User: `demo@miora.com` / `demo123`
- Test User 1: `test1@miora.com` / `testpass123`
- Test User 2: `test2@miora.com` / `testpass123`

### Authentication
```bash
# Register new user
curl -X POST http://localhost:8000/api/v1/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{"email": "user@example.com", "password": "securepass123", "password_confirm": "securepass123"}'

# Login
curl -X POST http://localhost:8000/api/v1/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"email": "user@example.com", "password": "securepass123"}'

# Use JWT token in requests
curl -X GET http://localhost:8000/api/v1/avatars/ \
  -H "Authorization: Bearer <your-access-token>"
```

### Core Endpoints

#### Avatars
- `GET /api/v1/avatars/` - List user's avatars
- `POST /api/v1/avatars/` - Create new avatar
- `GET /api/v1/avatars/{id}/` - Get avatar details
- `PUT /api/v1/avatars/{id}/` - Update avatar
- `DELETE /api/v1/avatars/{id}/` - Delete avatar
- `POST /api/v1/avatars/{id}/set_active/` - Set as active avatar
- `POST /api/v1/avatars/{id}/generate_from_photo/` - Generate from photo

#### Garments
- `GET /api/v1/garments/garments/` - List user's garments
- `POST /api/v1/garments/garments/upload/` - Upload new garment
- `GET /api/v1/garments/garments/{id}/` - Get garment details
- `GET /api/v1/garments/garments/{id}/processing_status/` - Check processing status
- `GET /api/v1/garments/size-charts/` - Get brand size charts

#### Virtual Try-On
- `POST /api/v1/try-on/sessions/` - Create try-on session
- `GET /api/v1/try-on/sessions/{id}/` - Get session details
- `POST /api/v1/try-on/sessions/{id}/save_as_outfit/` - Save as outfit
- `GET /api/v1/try-on/outfits/` - List saved outfits
- `POST /api/v1/try-on/outfits/{id}/duplicate/` - Duplicate outfit

#### Size Recommendations
- `POST /api/v1/recommendations/get/` - Get size recommendation
- `POST /api/v1/recommendations/feedback/` - Provide feedback
- `GET /api/v1/recommendations/history/` - Recommendation history

#### Analytics
- `GET /api/v1/analytics/metrics/` - Get metrics
- `GET /api/v1/analytics/dashboard/` - Dashboard data

## 🧪 Testing

### Run all tests
```bash
pytest
```

### Run with coverage
```bash
pytest --cov=. --cov-report=html
```

### Run specific test module
```bash
pytest accounts/tests/test_views.py
```

### Test categories
```bash
# Unit tests only
pytest -m unit

# Integration tests
pytest -m integration

# Slow tests
pytest -m slow
```

## 📦 Background Tasks

Miora uses Celery for background task processing:

### Start Celery worker
```bash
celery -A core worker -l info
```

### Start Celery beat (periodic tasks)
```bash
celery -A core beat -l info
```

### Monitor tasks with Flower
```bash
pip install flower
celery -A core flower
```

## 📁 Project Structure
```
backend/
├── core/               # Django project settings
│   ├── settings/       # Environment-specific settings
│   ├── urls.py         # Main URL configuration
│   ├── wsgi.py         # WSGI configuration
│   └── celery.py       # Celery configuration
├── accounts/           # User authentication & management
├── profiles/           # User profiles & preferences
├── avatars/            # Avatar creation & management
├── garments/           # Garment processing & storage
├── try_on/             # Virtual try-on engine
├── recommendations/    # Size recommendation system
├── analytics/          # Analytics & monitoring
├── media/              # User uploaded files
├── static/             # Static assets
├── staticfiles/        # Collected static files
├── logs/               # Application logs
├── templates/          # Email templates
├── requirements.txt    # Python dependencies
├── manage.py           # Django management script
├── docker-compose.yml  # Docker services
├── Dockerfile          # Docker image definition
├── gunicorn.confg.py   # Gunicorn configuration
└── nginx.conf          # Nginx configuration
```

## 🚀 Deployment

### Production Checklist
- [ ] Set `DEBUG = False`
- [ ] Configure production database
- [ ] Set up Redis for caching
- [ ] Configure AWS S3 for media storage
- [ ] Set up email service (SendGrid/AWS SES)
- [ ] Configure Sentry for error tracking
- [ ] Set up SSL certificates
- [ ] Configure firewall rules
- [ ] Set up monitoring (Prometheus/Grafana)
- [ ] Configure backup strategy

### Environment Variables
```bash
# Django
SECRET_KEY=your-production-secret-key
DEBUG=False
ALLOWED_HOSTS=api.miora.com,www.api.miora.com

# Database
DB_ENGINE=django.db.backends.postgresql
DB_NAME=miora_production
DB_USER=miora_user
DB_PASSWORD=secure-password
DB_HOST=your-db-host
DB_PORT=5432

# Redis
REDIS_URL=redis://your-redis-host:6379/0

# AWS S3
AWS_ACCESS_KEY_ID=your-access-key
AWS_SECRET_ACCESS_KEY=your-secret-key
AWS_STORAGE_BUCKET_NAME=miora-media
AWS_S3_REGION_NAME=us-east-1

# Email
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.sendgrid.net
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=apikey
EMAIL_HOST_PASSWORD=your-sendgrid-api-key

# Security
SECURE_SSL_REDIRECT=True
SESSION_COOKIE_SECURE=True
CSRF_COOKIE_SECURE=True
```

### Deployment with Gunicorn & Nginx
```bash
# Install production dependencies
pip install gunicorn psycopg2-binary

# Collect static files
python manage.py collectstatic --noinput

# Run Gunicorn
gunicorn core.wsgi:application --bind 0.0.0.0:8000 --workers 4

# Configure Nginx (see nginx.conf)
sudo nginx -s reload
```

## 📊 Monitoring

### Health Check
```bash
curl http://localhost:8000/health/
```

### Metrics Endpoint
```bash
curl http://localhost:8000/api/v1/analytics/metrics/
```

### Log Files
- Application logs: `logs/django.log`
- Celery logs: `logs/celery.log`
- Nginx access logs: `/var/log/nginx/access.log` (production)
- Nginx error logs: `/var/log/nginx/error.log` (production)

## 🔧 Troubleshooting

### Common Issues

#### Database connection error
```bash
# Check PostgreSQL is running
sudo systemctl status postgresql

# Check connection
psql -U miora_user -d miora_db -h localhost
```

#### Redis connection error
```bash
# Check Redis is running
redis-cli ping

# Should return: PONG
```

#### Static files not loading
```bash
# Collect static files
python manage.py collectstatic --noinput

# Check STATIC_ROOT setting
python manage.py shell
>>> from django.conf import settings
>>> print(settings.STATIC_ROOT)
```

#### Celery tasks not processing
```bash
# Check Celery worker is running
celery -A core inspect active

# Check Redis connection
python manage.py shell
>>> from django.core.cache import cache
>>> cache.set('test', 'value')
>>> cache.get('test')
```

## 🛠️ Development Commands

```bash
# Create new app
python manage.py startapp app_name

# Make migrations
python manage.py makemigrations

# Create superuser
python manage.py createsuperuser

# Run shell with auto-imports
python manage.py shell_plus

# Database shell
python manage.py dbshell

# Load test data
python manage.py create_test_users

# Generate sample analytics data
python create_sample_data.py
```

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Code Style
- Follow PEP 8
- Use Black for formatting: `black .`
- Use isort for imports: `isort .`
- Run flake8: `flake8 .`

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- Django REST Framework for the excellent API toolkit
- Three.js community for 3D rendering insights
- MediaPipe team for pose detection models
- All contributors and testers

## 📞 Support

- Documentation: https://docs.miora.com
- Issues: https://github.com/your-org/miora-backend/issues
- Email: support@miora.com
- Discord: https://discord.gg/miora

---

Built with ❤️ by the Miora Team