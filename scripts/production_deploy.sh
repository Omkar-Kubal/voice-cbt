#!/bin/bash
# Production deployment script for Voice CBT

set -e

# Configuration
ENVIRONMENT=${1:-production}
DOCKER_COMPOSE_FILE="docker-compose.prod.yml"
ENV_FILE="config.production.env"
BACKUP_DIR="/backups/voice-cbt"
LOG_DIR="/var/log/voice-cbt"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
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

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if running as root
check_root() {
    if [[ $EUID -eq 0 ]]; then
        log_error "This script should not be run as root"
        exit 1
    fi
}

# Check prerequisites
check_prerequisites() {
    log_info "Checking prerequisites..."
    
    # Check Docker
    if ! command -v docker &> /dev/null; then
        log_error "Docker is not installed"
        exit 1
    fi
    
    # Check Docker Compose
    if ! command -v docker-compose &> /dev/null; then
        log_error "Docker Compose is not installed"
        exit 1
    fi
    
    # Check environment file
    if [ ! -f "$ENV_FILE" ]; then
        log_error "Environment file $ENV_FILE not found"
        log_info "Run: python app/core/production_config.py generate"
        exit 1
    fi
    
    # Check disk space
    available_space=$(df / | awk 'NR==2 {print $4}')
    if [ "$available_space" -lt 10485760 ]; then  # 10GB in KB
        log_warning "Low disk space: $(($available_space / 1024 / 1024))GB available"
    fi
    
    log_success "Prerequisites check passed"
}

# Create directories
create_directories() {
    log_info "Creating necessary directories..."
    
    sudo mkdir -p "$BACKUP_DIR" "$LOG_DIR" "/app/voice-cbt"
    sudo chown -R $USER:$USER "$BACKUP_DIR" "$LOG_DIR" "/app/voice-cbt"
    
    log_success "Directories created"
}

# Backup existing deployment
backup_existing() {
    if docker-compose -f $DOCKER_COMPOSE_FILE ps | grep -q "Up"; then
        log_info "Backing up existing deployment..."
        
        BACKUP_NAME="backup-$(date +%Y%m%d-%H%M%S)"
        sudo mkdir -p "$BACKUP_DIR/$BACKUP_NAME"
        
        # Backup database
        docker-compose -f $DOCKER_COMPOSE_FILE exec -T db pg_dump -U voicecbt_user voicecbt_prod > "$BACKUP_DIR/$BACKUP_NAME/database.sql"
        
        # Backup application data
        sudo cp -r /app/voice-cbt/trained_models "$BACKUP_DIR/$BACKUP_NAME/" 2>/dev/null || true
        sudo cp -r /app/voice-cbt/chroma_db "$BACKUP_DIR/$BACKUP_NAME/" 2>/dev/null || true
        
        log_success "Backup created: $BACKUP_DIR/$BACKUP_NAME"
    fi
}

# Pull latest images
pull_images() {
    log_info "Pulling latest Docker images..."
    
    docker-compose -f $DOCKER_COMPOSE_FILE pull
    
    log_success "Images pulled successfully"
}

# Build application
build_application() {
    log_info "Building application..."
    
    # Build with production optimizations
    docker-compose -f $DOCKER_COMPOSE_FILE build --no-cache
    
    log_success "Application built successfully"
}

# Deploy application
deploy_application() {
    log_info "Deploying application..."
    
    # Stop existing services
    docker-compose -f $DOCKER_COMPOSE_FILE down --remove-orphans
    
    # Start services in order
    docker-compose -f $DOCKER_COMPOSE_FILE --env-file $ENV_FILE up -d db clickhouse redis
    
    # Wait for databases
    log_info "Waiting for databases to be ready..."
    sleep 30
    
    # Initialize database
    docker-compose -f $DOCKER_COMPOSE_FILE exec -T backend python init_database.py
    
    # Start remaining services
    docker-compose -f $DOCKER_COMPOSE_FILE --env-file $ENV_FILE up -d
    
    log_success "Application deployed"
}

# Health check
health_check() {
    log_info "Performing health check..."
    
    # Wait for services to start
    sleep 60
    
    # Check backend
    if curl -f http://localhost:8000/health > /dev/null 2>&1; then
        log_success "Backend health check passed"
    else
        log_error "Backend health check failed"
        return 1
    fi
    
    # Check frontend
    if curl -f http://localhost:3000 > /dev/null 2>&1; then
        log_success "Frontend health check passed"
    else
        log_error "Frontend health check failed"
        return 1
    fi
    
    # Check monitoring
    if curl -f http://localhost:9090 > /dev/null 2>&1; then
        log_success "Monitoring health check passed"
    else
        log_warning "Monitoring health check failed"
    fi
    
    log_success "All health checks passed"
}

# Setup monitoring
setup_monitoring() {
    log_info "Setting up monitoring..."
    
    # Create log rotation
    sudo tee /etc/logrotate.d/voice-cbt > /dev/null <<EOF
$LOG_DIR/*.log {
    daily
    missingok
    rotate 30
    compress
    delaycompress
    notifempty
    create 644 $USER $USER
}
EOF
    
    # Setup systemd service for monitoring
    sudo tee /etc/systemd/system/voice-cbt-monitor.service > /dev/null <<EOF
[Unit]
Description=Voice CBT Monitoring
After=network.target

[Service]
Type=simple
User=$USER
WorkingDirectory=/app/voice-cbt
ExecStart=/usr/bin/docker-compose -f $DOCKER_COMPOSE_FILE logs -f
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF
    
    sudo systemctl daemon-reload
    sudo systemctl enable voice-cbt-monitor.service
    
    log_success "Monitoring setup completed"
}

# Setup SSL
setup_ssl() {
    if [ -f "/etc/ssl/certs/voice-cbt.crt" ] && [ -f "/etc/ssl/private/voice-cbt.key" ]; then
        log_info "SSL certificates found, configuring HTTPS..."
        
        # SSL is already configured in nginx.prod.conf
        log_success "SSL configuration completed"
    else
        log_warning "SSL certificates not found, using HTTP only"
        log_info "To enable HTTPS, place certificates at:"
        log_info "  /etc/ssl/certs/voice-cbt.crt"
        log_info "  /etc/ssl/private/voice-cbt.key"
    fi
}

# Main deployment function
main() {
    log_info "Starting production deployment for environment: $ENVIRONMENT"
    
    check_root
    check_prerequisites
    create_directories
    backup_existing
    pull_images
    build_application
    deploy_application
    
    if health_check; then
        setup_monitoring
        setup_ssl
        
        log_success "🎉 Production deployment completed successfully!"
        log_info "Application URLs:"
        log_info "  Frontend: http://localhost:3000"
        log_info "  Backend API: http://localhost:8000"
        log_info "  API Documentation: http://localhost:8000/docs"
        log_info "  Monitoring: http://localhost:9090"
        log_info "  Grafana: http://localhost:3001"
        
        log_info "Useful commands:"
        log_info "  View logs: docker-compose -f $DOCKER_COMPOSE_FILE logs -f"
        log_info "  Stop services: docker-compose -f $DOCKER_COMPOSE_FILE down"
        log_info "  Restart services: docker-compose -f $DOCKER_COMPOSE_FILE restart"
        log_info "  Scale backend: docker-compose -f $DOCKER_COMPOSE_FILE up -d --scale backend=3"
    else
        log_error "Deployment failed health checks"
        exit 1
    fi
}

# Handle script arguments
case "${1:-}" in
    "deploy")
        main
        ;;
    "backup")
        backup_existing
        ;;
    "health")
        health_check
        ;;
    "logs")
        docker-compose -f $DOCKER_COMPOSE_FILE logs -f
        ;;
    "stop")
        docker-compose -f $DOCKER_COMPOSE_FILE down
        ;;
    "restart")
        docker-compose -f $DOCKER_COMPOSE_FILE restart
        ;;
    "scale")
        SCALE=${2:-2}
        docker-compose -f $DOCKER_COMPOSE_FILE up -d --scale backend=$SCALE
        ;;
    *)
        echo "Usage: $0 {deploy|backup|health|logs|stop|restart|scale [num]}"
        echo ""
        echo "Commands:"
        echo "  deploy   - Full production deployment"
        echo "  backup   - Create backup of current deployment"
        echo "  health   - Run health checks"
        echo "  logs     - View application logs"
        echo "  stop     - Stop all services"
        echo "  restart  - Restart all services"
        echo "  scale    - Scale backend services (default: 2)"
        exit 1
        ;;
esac
