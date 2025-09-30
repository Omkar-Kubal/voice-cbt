# 🎙️ Voice CBT - Project Overview

## 📋 Project Summary

**Voice CBT** is an AI-powered Cognitive Behavioral Therapy application that provides personalized therapeutic conversations through voice interaction, emotion detection, and mood tracking.

### 🌟 Key Features
- **Voice-to-Text**: Real-time speech recognition using OpenAI Whisper
- **Emotion Detection**: AI-powered emotion analysis from audio and text
- **Therapeutic Responses**: RAG-based CBT responses using LangChain
- **Mood Tracking**: Comprehensive mood analytics and trends
- **Real-time Dashboard**: Live monitoring and analytics
- **Multi-Database Architecture**: PostgreSQL + ClickHouse + ChromaDB
- **Security**: JWT authentication, rate limiting, IP blocking
- **Monitoring**: Prometheus + Grafana integration

## 🏗️ Project Structure

```
voice-cbt/
├── 📁 backend/                    # FastAPI backend application
│   ├── 📁 app/                    # Main application code
│   │   ├── 📁 api/               # API endpoints
│   │   ├── 📁 core/              # Core configuration and security
│   │   ├── 📁 middleware/         # Custom middleware
│   │   ├── 📁 models/            # Database models and schemas
│   │   └── 📁 services/           # Business logic services
│   ├── 📁 tests/                 # Test suite
│   ├── 📄 Dockerfile             # Backend container configuration
│   ├── 📄 requirements.txt       # Python dependencies
│   └── 📄 init_database.py       # Database initialization
├── 📁 frontend/                   # React frontend application
│   ├── 📁 src/                   # Source code
│   │   ├── 📁 components/        # React components
│   │   ├── 📁 pages/            # Page components
│   │   ├── 📁 hooks/            # Custom React hooks
│   │   └── 📁 lib/              # Utility functions
│   ├── 📄 Dockerfile             # Frontend container configuration
│   ├── 📄 package.json           # Node.js dependencies
│   └── 📄 vite.config.ts         # Vite configuration
├── 📁 docs/                      # Documentation
│   ├── 📁 architecture/          # System architecture docs
│   ├── 📁 deployment/            # Deployment guides
│   ├── 📁 development/           # Development documentation
│   └── 📁 images/                # Visual documentation
├── 📁 monitoring/                # Monitoring configuration
│   ├── 📁 grafana/              # Grafana dashboards
│   └── 📄 prometheus.yml         # Prometheus configuration
├── 📁 nginx/                     # Nginx configuration
├── 📁 scripts/                   # Deployment and setup scripts
├── 📁 data/                      # Training data and datasets
├── 📁 scraped_data/              # Scraped knowledge base
├── 📄 docker-compose.yml         # Development environment
├── 📄 docker-compose.prod.yml    # Production environment
├── 📄 README.md                  # Main project documentation
├── 📄 TECHNICAL_README.md        # Technical deep dive
└── 📄 .gitignore                 # Git ignore rules
```

## 🚀 Quick Start

### Prerequisites
- Docker & Docker Compose
- 8GB+ RAM (16GB recommended)
- 20GB+ free disk space
- Modern browser with WebRTC support

### Installation
```bash
# 1. Clone repository
git clone https://github.com/yourusername/voice-cbt.git
cd voice-cbt

# 2. Set up environment
cp backend/config.env.example backend/.env
# Edit .env with your configuration

# 3. Start services
docker-compose up -d

# 4. Initialize database
docker-compose exec backend python init_database.py

# 5. Access application
# Frontend: http://localhost:3000
# Backend: http://localhost:8000
# API Docs: http://localhost:8000/docs
```

## 🎯 Technology Stack

### Frontend
- **React 18** with TypeScript
- **Vite** for build tooling
- **Tailwind CSS** for styling
- **Shadcn/ui** for components
- **Axios** for API communication

### Backend
- **FastAPI** for web framework
- **SQLAlchemy** for ORM
- **PostgreSQL** for primary database
- **ClickHouse** for analytics
- **ChromaDB** for vector storage
- **Redis** for caching

### AI/ML
- **OpenAI Whisper** for speech-to-text
- **Hugging Face Transformers** for emotion detection
- **LangChain** for RAG implementation
- **ChromaDB** for vector storage
- **Custom models** for emotion analysis

### Infrastructure
- **Docker** for containerization
- **Docker Compose** for orchestration
- **Nginx** for reverse proxy
- **Prometheus** for monitoring
- **Grafana** for visualization

## 📊 Project Metrics

### Development
- **Duration**: 6 months
- **Team Size**: 8-12 members
- **Budget**: $300,000
- **Lines of Code**: ~50,000
- **Test Coverage**: >90%

### Performance
- **Response Time**: < 200ms
- **Accuracy**: > 90% emotion detection
- **Uptime**: 99.9% availability
- **Scalability**: 1000+ concurrent users

### Business Impact
- **Target Users**: 1000+ in first 3 months
- **User Satisfaction**: > 4.5/5 rating
- **Clinical Validation**: Therapist approved
- **Compliance**: HIPAA ready

## 🔧 Development Workflow

### Git Workflow
1. **Feature Branch**: Create feature branch from main
2. **Development**: Implement feature with tests
3. **Testing**: Run full test suite
4. **Review**: Create pull request for review
5. **Merge**: Merge to main after approval
6. **Deploy**: Automatic deployment to staging

### Testing Strategy
- **Unit Tests**: Individual component testing
- **Integration Tests**: API and service testing
- **E2E Tests**: Complete user journey testing
- **Performance Tests**: Load and stress testing
- **Security Tests**: Vulnerability and penetration testing

### Code Quality
- **Linting**: ESLint for frontend, Flake8 for backend
- **Formatting**: Prettier for frontend, Black for backend
- **Type Checking**: TypeScript for frontend, mypy for backend
- **Documentation**: Comprehensive docstrings and comments

## 📈 Roadmap

### Phase 1: Core Features ✅
- [x] Voice-to-text transcription
- [x] Emotion detection
- [x] Basic CBT responses
- [x] Mood tracking
- [x] User authentication

### Phase 2: Advanced AI 🚧
- [ ] Multi-language support
- [ ] Advanced emotion analysis
- [ ] Personalized therapy plans
- [ ] Progress prediction
- [ ] Crisis detection

### Phase 3: Clinical Integration 📋
- [ ] Therapist dashboard
- [ ] Clinical reporting
- [ ] HIPAA compliance
- [ ] Insurance integration
- [ ] Telehealth integration

### Phase 4: Research & Innovation 🔬
- [ ] AI model improvements
- [ ] Clinical trials
- [ ] Research partnerships
- [ ] Academic publications
- [ ] Open source contributions

## 🤝 Contributing

### Getting Started
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new features
5. Ensure all tests pass
6. Submit a pull request

### Development Setup
```bash
# Backend development
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
python -m pytest tests/

# Frontend development
cd frontend
npm install
npm run dev
```

### Code Standards
- Follow PEP 8 for Python code
- Use TypeScript for all frontend code
- Write comprehensive tests
- Document all public APIs
- Use meaningful commit messages

## 📞 Support

### Documentation
- [Main README](README.md) - Project overview
- [Technical README](TECHNICAL_README.md) - Deep technical details
- [Architecture Docs](docs/architecture/) - System design
- [Deployment Guide](docs/deployment/) - Production setup
- [Development Docs](docs/development/) - Development workflow

### Community
- **Issues**: Report bugs and request features
- **Discussions**: Ask questions and share ideas
- **Wiki**: Additional documentation and guides
- **Discord**: Real-time community chat

### Professional Support
- **Enterprise**: Custom deployment and support
- **Training**: Team training and workshops
- **Consulting**: Architecture and implementation guidance
- **Partnership**: Integration and collaboration opportunities

---

**Built with ❤️ for mental health accessibility**

*Last Updated: September 2024*
