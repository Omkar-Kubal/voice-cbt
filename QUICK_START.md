# 🚀 Voice CBT - Quick Start Guide

## ⚡ Super Quick Setup (5 minutes)

### 1. Clone & Setup
```bash
git clone https://github.com/Omkar-Kubal/voice-cbt.git
cd voice-cbt
```

### 2. Automated Setup
**Linux/macOS:**
```bash
./setup.sh
```

**Windows:**
```cmd
setup.bat
```

### 3. Configure API Keys
Edit `backend/config.env`:
```env
OPENAI_API_KEY=your_openai_key_here
ELEVENLABS_API_KEY=your_elevenlabs_key_here
SECRET_KEY=your_secret_key_here
JWT_SECRET=your_jwt_secret_here
```

### 4. Start Application
**Option A - Automated:**
```bash
# Linux/macOS
./start.sh

# Windows
start.bat
```

**Option B - Docker:**
```bash
# All platforms
./start-docker.sh
# or
start-docker.bat
```

**Option C - Manual:**
```bash
# Terminal 1 - Backend
cd backend
python -m venv venv
source venv/bin/activate  # Linux/macOS
# or
venv\Scripts\activate     # Windows
pip install -r requirements.txt
python init_database.py
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Terminal 2 - Frontend
cd frontend
npm install
npm run dev
```

## 🌐 Access Your Application

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs

## 📋 Prerequisites Checklist

- [ ] **Git** installed
- [ ] **Python 3.8+** installed
- [ ] **Node.js 18+** installed
- [ ] **Docker** (optional but recommended)
- [ ] **OpenAI API Key** (required)
- [ ] **ElevenLabs API Key** (required)

## 🔧 Troubleshooting

### Port Already in Use
```bash
# Kill processes on ports 3000 and 8000
npx kill-port 3000 8000
```

### Python Issues
```bash
pip install --upgrade pip
pip install -r requirements.txt --force-reinstall
```

### Node.js Issues
```bash
rm -rf node_modules package-lock.json
npm install
```

### Database Issues
```bash
rm voice_cbt.db
python init_database.py
```

## 🎯 What You Get

- **AI-Powered Voice CBT Therapy**
- **Real-time Emotion Detection**
- **Interactive Voice Conversations**
- **Progress Tracking**
- **Modern React Frontend**
- **FastAPI Backend**
- **Comprehensive API Documentation**

## 📚 Full Documentation

- **Complete Setup Guide**: `SETUP_COMPLETE_GUIDE.md`
- **Technical Documentation**: `TECHNICAL_README.md`
- **LLM Setup**: `LLM_SETUP.md`
- **Project Overview**: `PROJECT_OVERVIEW.md`

## 🆘 Need Help?

1. Check the troubleshooting section above
2. Review `SETUP_COMPLETE_GUIDE.md` for detailed instructions
3. Check the logs in the `logs/` directory
4. Ensure all environment variables are properly set

---

**Ready to start your Voice CBT journey? Run the setup script and you'll be up and running in minutes! 🎉**
