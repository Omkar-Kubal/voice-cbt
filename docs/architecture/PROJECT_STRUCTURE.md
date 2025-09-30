# Voice CBT - Project Structure

## 📁 Clean Project Organization

```
voice-cbt/
├── 📁 backend/                    # Backend API (FastAPI)
│   ├── 📁 app/                   # Application code
│   │   ├── 📁 api/               # API endpoints
│   │   │   ├── audio.py         # Voice processing endpoints
│   │   │   ├── mood.py          # Mood tracking endpoints
│   │   │   └── monitoring.py    # System monitoring endpoints
│   │   ├── 📁 core/              # Core configuration
│   │   │   ├── config.py        # Basic configuration
│   │   │   ├── production_config.py  # Production settings
│   │   │   └── security.py      # Security utilities
│   │   ├── 📁 middleware/        # Security middleware
│   │   │   └── security_middleware.py
│   │   ├── 📁 models/            # Database models
│   │   │   ├── database.py      # SQLAlchemy models
│   │   │   └── schemas.py       # Pydantic schemas
│   │   ├── 📁 services/          # Business logic
│   │   │   ├── analytics.py     # Analytics service
│   │   │   ├── audio_processor.py
│   │   │   ├── database_service.py
│   │   │   ├── emotion_detector.py
│   │   │   ├── monitoring.py    # System monitoring
│   │   │   ├── model_manager.py
│   │   │   ├── reply_generator.py
│   │   │   └── speech_to_text_config.py
│   │   └── main.py              # FastAPI application
│   ├── 📁 tests/                 # Test suite
│   │   ├── conftest.py          # Test configuration
│   │   ├── test_api_endpoints.py
│   │   ├── test_integration.py
│   │   └── test_services.py
│   ├── 📄 requirements.txt      # Python dependencies
│   ├── 📄 Dockerfile            # Development Dockerfile
│   ├── 📄 Dockerfile.prod       # Production Dockerfile
│   ├── 📄 init_database.py      # Database initialization
│   ├── 📄 run_tests.py          # Test runner
│   └── 📄 pytest.ini           # Test configuration
├── 📁 frontend/                  # React Frontend
│   ├── 📁 src/                  # Source code
│   │   ├── 📁 components/       # React components
│   │   ├── 📁 pages/           # Page components
│   │   ├── 📁 hooks/           # Custom hooks
│   │   └── 📁 lib/             # Utilities
│   ├── 📄 package.json         # Node dependencies
│   ├── 📄 Dockerfile           # Development Dockerfile
│   ├── 📄 Dockerfile.prod      # Production Dockerfile
│   └── 📄 nginx.conf           # Nginx configuration
├── 📁 monitoring/               # Monitoring configuration
│   ├── 📄 prometheus.yml       # Prometheus config
│   └── 📁 grafana/             # Grafana dashboards
│       ├── 📁 dashboards/
│       └── 📁 datasources/
├── 📁 nginx/                    # Nginx configuration
│   └── 📄 nginx.prod.conf      # Production nginx config
├── 📁 scripts/                  # Deployment scripts
│   ├── 📄 setup.sh             # Setup script
│   └── 📄 production_deploy.sh # Production deployment
├── 📁 .github/                  # GitHub Actions
│   └── 📁 workflows/
│       └── 📄 ci.yml           # CI/CD pipeline
├── 📄 docker-compose.yml       # Development setup
├── 📄 docker-compose.prod.yml  # Production setup
├── 📄 README.md                # Project documentation
├── 📄 LICENSE                  # MIT License
└── 📄 .gitignore              # Git ignore rules
```

## 🗑️ Removed Files

The following unnecessary files have been removed to clean up the project:

### Backend Cleanup
- ❌ `install_windows.bat` - Windows-specific installer
- ❌ `quick_install.py` - Redundant installer
- ❌ `setup_backend.py` - Redundant setup script
- ❌ `SPEECH_TO_TEXT_README.md` - Moved to main README
- ❌ `WINDOWS_INSTALLATION.md` - Moved to main README
- ❌ `requirements-basic.txt` - Redundant requirements
- ❌ `requirements-minimal.txt` - Redundant requirements
- ❌ `Dockerfile` (old) - Replaced with new Dockerfile
- ❌ `deploy.sh` (old) - Replaced with production_deploy.sh

### Root Cleanup
- ❌ `docker-compose.dev.yml` - Merged into main docker-compose.yml
- ❌ `nginx/default.conf` - Replaced with nginx.prod.conf
- ❌ `package.json` (root) - Not needed
- ❌ `Readme_KimiChat.md` - Redundant documentation
- ❌ `Readme.Md` - Replaced with main README.md
- ❌ `Repository_Layout.md` - Replaced with PROJECT_STRUCTURE.md

## 🚀 Quick Start Commands

### Development
```bash
# Setup development environment
./scripts/setup.sh dev

# Start services
docker-compose up -d

# Run tests
cd backend && python run_tests.py --type all

# Stop services
docker-compose down
```

### Production
```bash
# Setup production environment
./scripts/setup.sh prod

# Deploy to production
./scripts/production_deploy.sh deploy

# Scale services
docker-compose -f docker-compose.prod.yml up -d --scale backend=3
```

## 📦 Docker Images

### Development
- **Backend**: `voice-cbt-backend` (Python 3.11, FastAPI)
- **Frontend**: `voice-cbt-frontend` (Node.js 18, React)
- **Database**: `postgres:16-alpine`
- **Analytics**: `clickhouse/clickhouse-server`

### Production
- **Backend**: `voice-cbt-backend-prod` (Optimized, multi-stage)
- **Frontend**: `voice-cbt-frontend-prod` (Nginx, static files)
- **Monitoring**: `prometheus`, `grafana`
- **Reverse Proxy**: `nginx:alpine`

## 🔧 Configuration Files

### Environment
- `backend/config.env.example` - Development environment template
- `backend/config.production.env` - Production environment (generated)
- `backend/.env` - Local environment (created during setup)

### Docker
- `docker-compose.yml` - Development services
- `docker-compose.prod.yml` - Production services with monitoring
- `backend/Dockerfile` - Development backend image
- `backend/Dockerfile.prod` - Production backend image
- `frontend/Dockerfile` - Development frontend image
- `frontend/Dockerfile.prod` - Production frontend image

### Monitoring
- `monitoring/prometheus.yml` - Prometheus configuration
- `monitoring/grafana/` - Grafana dashboards and datasources
- `nginx/nginx.prod.conf` - Production nginx configuration

## 🧪 Testing Structure

```
backend/tests/
├── conftest.py              # Test fixtures and configuration
├── test_api_endpoints.py    # API endpoint tests
├── test_integration.py      # Integration tests
└── test_services.py         # Service layer tests
```

## 📊 Monitoring & Analytics

- **Prometheus**: Metrics collection
- **Grafana**: Visualization dashboards
- **Custom Metrics**: Application-specific monitoring
- **Health Checks**: Automated system health monitoring
- **Alerting**: Configurable alert thresholds

## 🔒 Security Features

- **Authentication**: JWT-based authentication
- **Rate Limiting**: Request rate limiting
- **Input Validation**: Comprehensive input sanitization
- **Security Headers**: CORS, CSP, security headers
- **IP Blocking**: Automatic suspicious activity detection
- **Audit Logging**: Security event logging

## 📈 Deployment Options

### Development
- Single-node Docker Compose
- Hot reloading enabled
- Debug logging
- Local database

### Production
- Multi-service Docker Compose
- Nginx reverse proxy
- SSL/TLS termination
- Monitoring and alerting
- Horizontal scaling support

## 🎯 Next Steps

1. **Clone the repository**
2. **Run setup**: `./scripts/setup.sh dev`
3. **Start development**: `docker-compose up -d`
4. **Access application**: http://localhost:3000
5. **Run tests**: `cd backend && python run_tests.py --type all`
6. **Deploy to production**: `./scripts/production_deploy.sh deploy`

The project is now clean, organized, and ready for development and production deployment! 🚀
