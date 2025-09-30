# Voice CBT - Deployment Guide

## 🚀 Quick Deployment

### 1. Development Setup
```bash
# Clone repository
git clone <your-repo-url>
cd voice-cbt

# Setup development environment
./scripts/setup.sh dev

# Start services
docker-compose up -d

# Access application
# Frontend: http://localhost:3000
# Backend: http://localhost:8000
# API Docs: http://localhost:8000/docs
```

### 2. Production Deployment
```bash
# Setup production environment
./scripts/setup.sh prod

# Deploy to production
./scripts/production_deploy.sh deploy

# Access production
# Frontend: http://your-domain.com
# Backend: http://your-domain.com/api
# Monitoring: http://your-domain.com:9090
```

## 📦 Docker Commands

### Development
```bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down

# Rebuild and restart
docker-compose up -d --build
```

### Production
```bash
# Deploy production
docker-compose -f docker-compose.prod.yml up -d

# Scale backend
docker-compose -f docker-compose.prod.yml up -d --scale backend=3

# View production logs
docker-compose -f docker-compose.prod.yml logs -f

# Stop production
docker-compose -f docker-compose.prod.yml down
```

## 🧪 Testing

```bash
# Run all tests
cd backend && python run_tests.py --type all

# Run specific test types
python run_tests.py --type unit
python run_tests.py --type integration
python run_tests.py --type coverage

# Run tests with Docker
docker-compose exec backend python run_tests.py --type all
```

## 🔧 Configuration

### Environment Variables
- Copy `backend/config.env.example` to `backend/.env`
- For production: Run `python backend/app/core/production_config.py generate`

### Database
```bash
# Initialize database
docker-compose exec backend python init_database.py

# Reset database
docker-compose exec backend python init_database.py --reset
```

## 📊 Monitoring

### Access Monitoring
- **Prometheus**: http://localhost:9090
- **Grafana**: http://localhost:3001
- **Health Check**: http://localhost:8000/health
- **Metrics**: http://localhost:8000/api/v1/metrics/summary

### View Logs
```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f backend
docker-compose logs -f frontend
docker-compose logs -f db
```

## 🔒 Security

### Security Features
- JWT Authentication
- Rate Limiting
- Input Validation
- Security Headers
- IP Blocking
- Audit Logging

### Security Endpoints
- `/security/status` - Security status
- `/security/block-ip` - Block IP address
- `/security/unblock-ip` - Unblock IP address

## 📈 Scaling

### Horizontal Scaling
```bash
# Scale backend services
docker-compose -f docker-compose.prod.yml up -d --scale backend=3

# Scale with load balancer
docker-compose -f docker-compose.prod.yml up -d --scale backend=5
```

### Performance Tuning
- Adjust `MAX_WORKERS` in environment
- Configure `WORKER_TIMEOUT`
- Set `KEEPALIVE_TIMEOUT`
- Optimize database connections

## 🛠️ Troubleshooting

### Common Issues

1. **Port conflicts**
   ```bash
   # Check port usage
   netstat -tulpn | grep :8000
   netstat -tulpn | grep :3000
   ```

2. **Database connection issues**
   ```bash
   # Check database status
   docker-compose exec db pg_isready
   ```

3. **Memory issues**
   ```bash
   # Check memory usage
   docker stats
   ```

4. **Permission issues**
   ```bash
   # Fix permissions
   sudo chown -R $USER:$USER .
   ```

### Health Checks
```bash
# Backend health
curl http://localhost:8000/health

# Frontend health
curl http://localhost:3000

# Database health
docker-compose exec db pg_isready
```

## 📋 Maintenance

### Backup
```bash
# Backup database
docker-compose exec db pg_dump -U postgres voicecbt > backup.sql

# Backup application data
tar -czf app-data-backup.tar.gz trained_models/ chroma_db/
```

### Updates
```bash
# Pull latest changes
git pull origin main

# Rebuild and restart
docker-compose up -d --build

# Run migrations
docker-compose exec backend python init_database.py
```

### Log Rotation
```bash
# Configure log rotation
sudo tee /etc/logrotate.d/voice-cbt > /dev/null <<EOF
/var/log/voice-cbt/*.log {
    daily
    missingok
    rotate 30
    compress
    delaycompress
    notifempty
    create 644 $USER $USER
}
EOF
```

## 🎯 Production Checklist

- [ ] Environment variables configured
- [ ] SSL certificates installed
- [ ] Database initialized
- [ ] Monitoring configured
- [ ] Security settings applied
- [ ] Backup strategy implemented
- [ ] Log rotation configured
- [ ] Health checks passing
- [ ] Performance optimized
- [ ] Scaling configured

## 🆘 Support

For issues and questions:
1. Check the logs: `docker-compose logs -f`
2. Run health checks: `curl http://localhost:8000/health`
3. Check system resources: `docker stats`
4. Review configuration files
5. Create an issue on GitHub

---

**Your Voice CBT application is now ready for production deployment! 🚀**
