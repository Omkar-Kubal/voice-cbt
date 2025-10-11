# 🚀 Voice CBT - Complete Setup Guide

## 📋 Prerequisites

### Required Software
- **Git** (latest version)
- **Python 3.8+** 
- **Node.js 18+** and npm/bun
- **Docker & Docker Compose** (recommended)
- **Visual Studio Code** (recommended IDE)

### API Keys Required
- **OpenAI API Key** - for LLM integration
- **ElevenLabs API Key** - for text-to-speech
- **Optional**: Other service keys as needed

## 🏗️ Complete Setup Process

### Step 1: Clone Repository
```bash
git clone https://github.com/Omkar-Kubal/voice-cbt.git
cd voice-cbt
```

### Step 2: Backend Setup
```bash
cd backend

# Create and activate virtual environment
python -m venv venv

# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate

# Install Python dependencies
pip install -r requirements.txt

# Set up environment variables
cp config.env.example config.env
```

### Step 3: Frontend Setup
```bash
cd frontend

# Install dependencies (choose one)
npm install
# OR
bun install
```

### Step 4: Database Initialization
```bash
cd backend
python init_database.py
```

### Step 5: Environment Configuration
Edit `backend/config.env` with your settings:

```env
# Database Configuration
DATABASE_URL=sqlite:///./voice_cbt.db

# API Keys
OPENAI_API_KEY=your_openai_api_key_here
ELEVENLABS_API_KEY=your_elevenlabs_api_key_here

# Security Keys
SECRET_KEY=your_secret_key_here
JWT_SECRET=your_jwt_secret_here

# Model Paths
EMOTION_MODEL_PATH=./best_crema_emotion_model.pth
SIMPLE_EMOTION_MODEL_PATH=./simple_emotion_model.pth

# Server Configuration
HOST=0.0.0.0
PORT=8000
DEBUG=True

# CORS Settings
CORS_ORIGINS=["http://localhost:3000", "http://127.0.0.1:3000"]
```

## 🐳 Docker Setup (Recommended)

### Option A: Full Docker Setup
```bash
# From project root
docker-compose up --build
```

### Option B: Development with Docker
```bash
# Backend only
docker-compose up backend

# Frontend only  
docker-compose up frontend
```

## 🖥️ Manual Development Setup

### Backend Server
```bash
cd backend
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Frontend Server
```bash
cd frontend
npm run dev
# OR
bun dev
```

## 🌐 Access Points

- **Frontend Application**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs
- **Interactive API**: http://localhost:8000/redoc

## 🔧 Project Structure

```
voice-cbt/
├── backend/                 # Python FastAPI backend
│   ├── app/
│   │   ├── api/            # API endpoints
│   │   ├── core/           # Core configuration
│   │   ├── middleware/     # Custom middleware
│   │   ├── models/         # Database models
│   │   └── services/       # Business logic services
│   ├── requirements.txt    # Python dependencies
│   └── config.env.example  # Environment template
├── frontend/               # React TypeScript frontend
│   ├── src/
│   │   ├── components/     # React components
│   │   ├── pages/          # Page components
│   │   └── hooks/          # Custom hooks
│   └── package.json        # Node.js dependencies
├── data/                   # Training data and models
├── docs/                   # Documentation
└── docker-compose.yml      # Docker configuration
```

## 🧪 Testing

### Backend Tests
```bash
cd backend
python -m pytest
```

### Frontend Tests
```bash
cd frontend
npm test
```

## 🚀 Production Deployment

### Using Docker
```bash
docker-compose -f docker-compose.prod.yml up --build
```

### Manual Production Setup
1. Set production environment variables
2. Use production database (PostgreSQL recommended)
3. Configure reverse proxy (nginx)
4. Set up SSL certificates
5. Configure monitoring and logging

## 🔍 Troubleshooting

### Common Issues

1. **Port Already in Use**
   ```bash
   # Kill processes on ports 3000 and 8000
   npx kill-port 3000 8000
   ```

2. **Python Dependencies Issues**
   ```bash
   pip install --upgrade pip
   pip install -r requirements.txt --force-reinstall
   ```

3. **Node.js Dependencies Issues**
   ```bash
   rm -rf node_modules package-lock.json
   npm install
   ```

4. **Database Issues**
   ```bash
   rm voice_cbt.db
   python init_database.py
   ```

### Environment-Specific Issues

#### Windows
- Use PowerShell or Command Prompt
- Ensure Python and Node.js are in PATH
- Use `venv\Scripts\activate` for virtual environment

#### macOS/Linux
- Use bash or zsh terminal
- May need `sudo` for some installations
- Use `source venv/bin/activate` for virtual environment

## 📚 Additional Resources

- **API Documentation**: http://localhost:8000/docs
- **Project README**: README.md
- **LLM Setup Guide**: LLM_SETUP.md
- **Technical Documentation**: TECHNICAL_README.md
- **Deployment Guide**: docs/deployment/DEPLOYMENT_GUIDE.md

## 🆘 Support

If you encounter issues:
1. Check the troubleshooting section above
2. Review the logs in the `logs/` directory
3. Check the GitHub issues page
4. Ensure all environment variables are properly set

## 🎯 Quick Start Commands

```bash
# Clone and setup everything
git clone https://github.com/Omkar-Kubal/voice-cbt.git
cd voice-cbt
./setup.sh  # If setup script exists

# Or manual setup
cd backend && python -m venv venv && venv\Scripts\activate && pip install -r requirements.txt && python init_database.py
cd ../frontend && npm install
cd .. && docker-compose up --build
```

Your Voice CBT application should now be running at http://localhost:3000! 🎉
