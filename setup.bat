@echo off
REM Voice CBT - Windows Automated Setup Script
REM This script sets up the entire Voice CBT project on a new Windows machine

echo 🚀 Voice CBT - Windows Automated Setup Script
echo ============================================

REM Check if we're in the right directory
if not exist "README.md" (
    echo [ERROR] Please run this script from the voice-cbt project root directory
    exit /b 1
)
if not exist "backend" (
    echo [ERROR] Please run this script from the voice-cbt project root directory
    exit /b 1
)
if not exist "frontend" (
    echo [ERROR] Please run this script from the voice-cbt project root directory
    exit /b 1
)

echo [INFO] Starting Voice CBT setup...

REM Check prerequisites
echo [INFO] Checking prerequisites...

REM Check Git
git --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Git is not installed. Please install Git first.
    exit /b 1
)

REM Check Python
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python is not installed. Please install Python 3.8+ first.
    exit /b 1
)

REM Check Node.js
node --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Node.js is not installed. Please install Node.js 18+ first.
    exit /b 1
)

REM Check Docker (optional)
docker --version >nul 2>&1
if errorlevel 1 (
    echo [WARNING] Docker is not installed. You can still run manually, but Docker is recommended.
)

echo [SUCCESS] Prerequisites check completed

REM Backend Setup
echo [INFO] Setting up backend...

cd backend

REM Create virtual environment
echo [INFO] Creating Python virtual environment...
if exist "venv" (
    echo [WARNING] Virtual environment already exists. Removing old one...
    rmdir /s /q venv
)

python -m venv venv
if errorlevel 1 (
    echo [ERROR] Failed to create virtual environment
    exit /b 1
)

REM Activate virtual environment
echo [INFO] Activating virtual environment...
call venv\Scripts\activate.bat

REM Upgrade pip
echo [INFO] Upgrading pip...
python -m pip install --upgrade pip

REM Install dependencies
echo [INFO] Installing Python dependencies...
pip install -r requirements.txt
if errorlevel 1 (
    echo [ERROR] Failed to install Python dependencies
    exit /b 1
)

REM Set up environment file
echo [INFO] Setting up environment configuration...
if not exist "config.env" (
    if exist "config.env.example" (
        copy config.env.example config.env
        echo [WARNING] Created config.env from template. Please edit it with your API keys!
    ) else (
        echo [WARNING] No config.env.example found. You'll need to create config.env manually.
    )
) else (
    echo [INFO] config.env already exists
)

REM Initialize database
echo [INFO] Initializing database...
python init_database.py
if errorlevel 1 (
    echo [ERROR] Failed to initialize database
    exit /b 1
)

echo [SUCCESS] Backend setup completed

REM Frontend Setup
echo [INFO] Setting up frontend...

cd ..\frontend

REM Install dependencies
echo [INFO] Installing Node.js dependencies...
npm install
if errorlevel 1 (
    echo [ERROR] Failed to install Node.js dependencies
    exit /b 1
)

echo [SUCCESS] Frontend setup completed

REM Return to root directory
cd ..

REM Create startup scripts
echo [INFO] Creating startup scripts...

REM Create start script
echo @echo off > start.bat
echo echo 🚀 Starting Voice CBT Application... >> start.bat
echo. >> start.bat
echo echo Starting backend server... >> start.bat
echo start "Backend Server" cmd /k "cd backend ^&^& call venv\Scripts\activate.bat ^&^& python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000" >> start.bat
echo timeout /t 3 /nobreak ^>nul >> start.bat
echo echo Starting frontend server... >> start.bat
echo start "Frontend Server" cmd /k "cd frontend ^&^& npm run dev" >> start.bat
echo. >> start.bat
echo echo ✅ Application started! >> start.bat
echo echo Frontend: http://localhost:3000 >> start.bat
echo echo Backend API: http://localhost:8000 >> start.bat
echo echo API Docs: http://localhost:8000/docs >> start.bat
echo echo. >> start.bat
echo echo Press any key to stop this script... >> start.bat
echo pause ^>nul >> start.bat

REM Create Docker start script
echo @echo off > start-docker.bat
echo echo 🐳 Starting Voice CBT with Docker... >> start-docker.bat
echo docker-compose up --build >> start-docker.bat

echo [SUCCESS] Startup scripts created

REM Final instructions
echo.
echo 🎉 Voice CBT setup completed successfully!
echo.
echo 📋 Next steps:
echo 1. Edit backend\config.env with your API keys:
echo    - OPENAI_API_KEY
echo    - ELEVENLABS_API_KEY
echo    - SECRET_KEY
echo    - JWT_SECRET
echo.
echo 2. Start the application:
echo    Manual: start.bat
echo    Docker: start-docker.bat
echo.
echo 3. Access the application:
echo    Frontend: http://localhost:3000
echo    Backend API: http://localhost:8000
echo    API Documentation: http://localhost:8000/docs
echo.
echo 📚 For detailed setup instructions, see SETUP_COMPLETE_GUIDE.md
echo.
echo [SUCCESS] Setup completed! Happy coding! 🚀

pause
