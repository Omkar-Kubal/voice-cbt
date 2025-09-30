#!/bin/bash
# Voice CBT Setup Script

set -e

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m'

log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

# Check prerequisites
check_prerequisites() {
    log_info "Checking prerequisites..."
    
    # Check Docker
    if ! command -v docker &> /dev/null; then
        log_warning "Docker is not installed. Please install Docker first."
        exit 1
    fi
    
    # Check Docker Compose
    if ! command -v docker-compose &> /dev/null; then
        log_warning "Docker Compose is not installed. Please install Docker Compose first."
        exit 1
    fi
    
    log_success "Prerequisites check passed"
}

# Setup development environment
setup_dev() {
    log_info "Setting up development environment..."
    
    # Create necessary directories
    mkdir -p logs trained_models chroma_db data/backups
    
    # Copy environment file
    if [ ! -f "backend/.env" ]; then
        cp backend/config.env.example backend/.env
        log_info "Created .env file from example"
    fi
    
    # Start services
    docker-compose up -d
    
    # Wait for services to be ready
    log_info "Waiting for services to start..."
    sleep 30
    
    # Initialize database
    docker-compose exec backend python init_database.py
    
    log_success "Development environment setup complete"
}

# Setup production environment
setup_prod() {
    log_info "Setting up production environment..."
    
    # Generate production config
    cd backend
    python app/core/production_config.py generate
    cd ..
    
    # Create production directories
    sudo mkdir -p /app/voice-cbt/{logs,trained_models,chroma_db,data}
    sudo chown -R $USER:$USER /app/voice-cbt
    
    log_success "Production environment setup complete"
}

# Main function
main() {
    echo "🚀 Voice CBT Setup"
    echo "=================="
    
    check_prerequisites
    
    case "${1:-dev}" in
        "dev")
            setup_dev
            echo ""
            echo "✅ Development environment ready!"
            echo "Frontend: http://localhost:3000"
            echo "Backend: http://localhost:8000"
            echo "API Docs: http://localhost:8000/docs"
            ;;
        "prod")
            setup_prod
            echo ""
            echo "✅ Production environment ready!"
            echo "Run: ./scripts/production_deploy.sh deploy"
            ;;
        *)
            echo "Usage: $0 {dev|prod}"
            echo "  dev  - Setup development environment"
            echo "  prod - Setup production environment"
            exit 1
            ;;
    esac
}

main "$@"
