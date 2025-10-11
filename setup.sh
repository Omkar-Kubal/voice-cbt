#!/bin/bash

# Voice CBT - Automated Setup Script
# This script sets up the entire Voice CBT project on a new machine

set -e  # Exit on any error

echo "🚀 Voice CBT - Automated Setup Script"
echo "======================================"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if we're in the right directory
if [ ! -f "README.md" ] || [ ! -d "backend" ] || [ ! -d "frontend" ]; then
    print_error "Please run this script from the voice-cbt project root directory"
    exit 1
fi

print_status "Starting Voice CBT setup..."

# Check prerequisites
print_status "Checking prerequisites..."

# Check Git
if ! command -v git &> /dev/null; then
    print_error "Git is not installed. Please install Git first."
    exit 1
fi

# Check Python
if ! command -v python3 &> /dev/null && ! command -v python &> /dev/null; then
    print_error "Python is not installed. Please install Python 3.8+ first."
    exit 1
fi

# Check Node.js
if ! command -v node &> /dev/null; then
    print_error "Node.js is not installed. Please install Node.js 18+ first."
    exit 1
fi

# Check Docker (optional)
if ! command -v docker &> /dev/null; then
    print_warning "Docker is not installed. You can still run manually, but Docker is recommended."
fi

print_success "Prerequisites check completed"

# Backend Setup
print_status "Setting up backend..."

cd backend

# Create virtual environment
print_status "Creating Python virtual environment..."
if [ -d "venv" ]; then
    print_warning "Virtual environment already exists. Removing old one..."
    rm -rf venv
fi

python3 -m venv venv || python -m venv venv

# Activate virtual environment
print_status "Activating virtual environment..."
if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
    source venv/Scripts/activate
else
    source venv/bin/activate
fi

# Upgrade pip
print_status "Upgrading pip..."
pip install --upgrade pip

# Install dependencies
print_status "Installing Python dependencies..."
pip install -r requirements.txt

# Set up environment file
print_status "Setting up environment configuration..."
if [ ! -f "config.env" ]; then
    if [ -f "config.env.example" ]; then
        cp config.env.example config.env
        print_warning "Created config.env from template. Please edit it with your API keys!"
    else
        print_warning "No config.env.example found. You'll need to create config.env manually."
    fi
else
    print_status "config.env already exists"
fi

# Initialize database
print_status "Initializing database..."
python init_database.py

print_success "Backend setup completed"

# Frontend Setup
print_status "Setting up frontend..."

cd ../frontend

# Install dependencies
print_status "Installing Node.js dependencies..."
if command -v bun &> /dev/null; then
    print_status "Using Bun package manager..."
    bun install
else
    print_status "Using npm package manager..."
    npm install
fi

print_success "Frontend setup completed"

# Return to root directory
cd ..

# Create startup scripts
print_status "Creating startup scripts..."

# Create start script
cat > start.sh << 'EOF'
#!/bin/bash
echo "🚀 Starting Voice CBT Application..."

# Start backend
echo "Starting backend server..."
cd backend
source venv/bin/activate 2>/dev/null || source venv/Scripts/activate 2>/dev/null
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000 &
BACKEND_PID=$!

# Start frontend
echo "Starting frontend server..."
cd ../frontend
npm run dev &
FRONTEND_PID=$!

echo "✅ Application started!"
echo "Frontend: http://localhost:3000"
echo "Backend API: http://localhost:8000"
echo "API Docs: http://localhost:8000/docs"
echo ""
echo "Press Ctrl+C to stop both servers"

# Wait for interrupt
trap "echo 'Stopping servers...'; kill $BACKEND_PID $FRONTEND_PID; exit" INT
wait
EOF

chmod +x start.sh

# Create Docker start script
cat > start-docker.sh << 'EOF'
#!/bin/bash
echo "🐳 Starting Voice CBT with Docker..."
docker-compose up --build
EOF

chmod +x start-docker.sh

print_success "Startup scripts created"

# Final instructions
echo ""
echo "🎉 Voice CBT setup completed successfully!"
echo ""
echo "📋 Next steps:"
echo "1. Edit backend/config.env with your API keys:"
echo "   - OPENAI_API_KEY"
echo "   - ELEVENLABS_API_KEY"
echo "   - SECRET_KEY"
echo "   - JWT_SECRET"
echo ""
echo "2. Start the application:"
echo "   Manual: ./start.sh"
echo "   Docker: ./start-docker.sh"
echo ""
echo "3. Access the application:"
echo "   Frontend: http://localhost:3000"
echo "   Backend API: http://localhost:8000"
echo "   API Documentation: http://localhost:8000/docs"
echo ""
echo "📚 For detailed setup instructions, see SETUP_COMPLETE_GUIDE.md"
echo ""
print_success "Setup completed! Happy coding! 🚀"
