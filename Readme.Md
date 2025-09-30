# 🎙️ Voice CBT - AI-Powered Cognitive Behavioral Therapy

A comprehensive voice-enabled Cognitive Behavioral Therapy application that uses AI to provide personalized therapeutic conversations, emotion detection, and mood tracking.

## 🌟 Features

- **Voice-to-Text**: Real-time speech recognition using OpenAI Whisper
- **Emotion Detection**: AI-powered emotion analysis from audio
- **Therapeutic Responses**: RAG-based CBT responses using LangChain
- **Mood Tracking**: Comprehensive mood analytics and trends
- **Real-time Dashboard**: Live monitoring and analytics
- **Multi-Database Architecture**: PostgreSQL + ClickHouse + ChromaDB
- **Security**: JWT authentication, rate limiting, IP blocking
- **Monitoring**: Prometheus + Grafana integration

## 🏗️ Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Frontend      │    │    Backend      │    │   Databases      │
│   (React)       │◄──►│   (FastAPI)     │◄──►│   PostgreSQL    │
│   Port: 3000    │    │   Port: 8000    │    │   ClickHouse    │
└─────────────────┘    └─────────────────┘    │   ChromaDB      │
                                              └─────────────────┘
```

## 🚀 Quick Start

### Prerequisites
- Docker & Docker Compose
- Git
- 8GB+ RAM recommended

### 1. Clone and Setup
```bash
git clone https://github.com/yourusername/voice-cbt.git
cd voice-cbt
```

### 2. Start the Application
```bash
# Start all services
docker-compose up -d

# Check status
docker-compose ps
```

### 3. Initialize Database
```bash
# Initialize database tables
docker-compose exec backend python init_database.py
```

### 4. Access the Application
- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs
- **Grafana Dashboard**: http://localhost:3001 (admin/admin)

## 🎯 Complete Project Tour

### 📱 **Frontend Pages Tour**

#### 1. **Landing Page** (`/`)
- **Purpose**: Welcome and introduction to Voice CBT
- **Features**: 
  - Hero section with voice therapy introduction
  - Feature highlights (emotion detection, mood tracking)
  - Getting started button
- **Navigation**: Click "Get Started" → Onboarding

#### 2. **Onboarding Flow** (`/onboarding`)
- **Step 1**: Welcome & consent
- **Step 2**: Audio permissions setup
- **Step 3**: Initial mood assessment
- **Step 4**: Therapy goals setting
- **Step 5**: Voice calibration
- **Navigation**: Complete onboarding → Dashboard

#### 3. **Main Dashboard** (`/dashboard`)
- **Purpose**: Central hub for therapy sessions
- **Features**:
  - Voice recording interface
  - Real-time emotion display
  - Session history
  - Mood trends chart
  - Quick actions panel
- **Navigation**: 
  - "Start Session" → Voice Therapy
  - "Mood Tracker" → Mood Page
  - "History" → Session History

#### 4. **Voice Therapy Session** (`/session`)
- **Purpose**: Interactive CBT conversation
- **Features**:
  - Real-time voice recording
  - Live transcription
  - Emotion detection feedback
  - AI therapeutic responses
  - Session timer
- **Navigation**: 
  - "End Session" → Dashboard
  - "Save & Continue" → Continue session

#### 5. **Mood Tracking** (`/mood`)
- **Purpose**: Track and analyze emotional patterns
- **Features**:
  - Daily mood entry
  - Mood history calendar
  - Trend analysis
  - Emotion correlation charts
- **Navigation**: 
  - "Back to Dashboard" → Dashboard
  - "Detailed Analysis" → Analytics

#### 6. **Session History** (`/history`)
- **Purpose**: Review past therapy sessions
- **Features**:
  - Session list with dates
  - Session summaries
  - Emotion progression
  - Export functionality
- **Navigation**: 
  - Click session → Session Details
  - "Back to Dashboard" → Dashboard

#### 7. **Analytics Dashboard** (`/analytics`)
- **Purpose**: Deep insights into therapy progress
- **Features**:
  - Progress charts
  - Emotion trends
  - Session frequency
  - Therapeutic outcomes
- **Navigation**: 
  - "Back to Dashboard" → Dashboard
  - "Export Report" → Download PDF

### 🔧 **Backend API Tour**

#### 1. **Health & Status** (`/health`)
```bash
curl http://localhost:8000/health
```
- **Response**: System status, database connections, service health

#### 2. **Authentication** (`/auth`)
- **POST** `/auth/register` - User registration
- **POST** `/auth/login` - User login
- **POST** `/auth/refresh` - Token refresh

#### 3. **Session Management** (`/session`)
- **POST** `/session/start` - Start new therapy session
- **POST** `/session/end` - End current session
- **GET** `/session/history` - Get session history

#### 4. **Audio Processing** (`/audio`)
- **POST** `/audio/transcribe` - Speech-to-text
- **POST** `/audio/analyze` - Emotion detection
- **POST** `/audio/respond` - Generate therapeutic response

#### 5. **Mood Tracking** (`/mood`)
- **POST** `/mood/log` - Log mood entry
- **GET** `/mood/trends` - Get mood trends
- **GET** `/mood/analytics` - Detailed mood analytics

#### 6. **Monitoring** (`/monitoring`)
- **GET** `/monitoring/metrics` - System metrics
- **GET** `/monitoring/health` - Service health
- **GET** `/monitoring/performance` - Performance data

### 📊 **Dashboard Tour**

#### 1. **Main Dashboard Components**
```
┌─────────────────────────────────────────────────────────┐
│  🎙️ Voice CBT Dashboard                                 │
├─────────────────────────────────────────────────────────┤
│  📊 Real-time Metrics                                   │
│  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐      │
│  │ Active      │ │ Sessions    │ │ Emotions    │      │
│  │ Users: 12   │ │ Today: 45   │ │ Detected: 8 │      │
│  └─────────────┘ └─────────────┘ └─────────────┘      │
├─────────────────────────────────────────────────────────┤
│  📈 Session Trends (Last 7 Days)                       │
│  [Interactive Chart]                                    │
├─────────────────────────────────────────────────────────┤
│  🎯 Quick Actions                                       │
│  [Start Session] [View Analytics] [Export Data]        │
└─────────────────────────────────────────────────────────┘
```

#### 2. **Analytics Dashboard**
- **User Engagement**: Daily active users, session frequency
- **Emotion Analysis**: Most common emotions, trends over time
- **Therapeutic Outcomes**: Progress tracking, goal achievement
- **System Performance**: Response times, error rates

#### 3. **Real-time Monitoring**
- **Live Sessions**: Currently active therapy sessions
- **System Health**: Database status, service availability
- **Performance Metrics**: Response times, throughput

### 🗄️ **Database Architecture Tour**

#### 1. **PostgreSQL (Primary Database)**
**Purpose**: User data, sessions, and relational data

**Tables**:
```sql
-- Users table
users (
  id, email, username, password_hash, 
  created_at, last_login, preferences
)

-- Therapy sessions
sessions (
  id, user_id, start_time, end_time, 
  duration, emotion_summary, transcript
)

-- Session interactions
interactions (
  id, session_id, timestamp, user_input, 
  ai_response, emotion_detected, confidence
)

-- Mood entries
mood_entries (
  id, user_id, timestamp, mood_score, 
  emotions, notes, context
)

-- System metrics
system_metrics (
  id, timestamp, cpu_usage, memory_usage, 
  response_time, error_count
)
```

#### 2. **ClickHouse (Analytics Database)**
**Purpose**: High-performance analytics and time-series data

**Tables**:
```sql
-- Session analytics
session_analytics (
  timestamp, user_id, session_id, 
  emotion_data, response_times, user_satisfaction
)

-- Mood trends
mood_trends (
  timestamp, user_id, mood_score, 
  emotion_breakdown, environmental_factors
)

-- System performance
performance_metrics (
  timestamp, service_name, response_time, 
  error_rate, throughput, resource_usage
)
```

#### 3. **ChromaDB (Vector Database)**
**Purpose**: Semantic search and RAG (Retrieval Augmented Generation)

**Collections**:
```sql
-- CBT knowledge base
cbt_knowledge (
  id, content, embedding, metadata, 
  category, confidence_score
)

-- Therapeutic responses
therapeutic_responses (
  id, response_text, embedding, 
  emotion_context, therapeutic_technique
)

-- User context
user_context (
  user_id, session_embeddings, 
  emotional_patterns, therapeutic_history
)
```

### 🔍 **Database Queries Tour**

#### 1. **User Analytics**
```sql
-- Daily active users
SELECT DATE(created_at) as date, COUNT(DISTINCT user_id) as active_users
FROM sessions 
WHERE created_at >= NOW() - INTERVAL '30 days'
GROUP BY DATE(created_at);

-- Session duration trends
SELECT AVG(duration) as avg_duration, 
       PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY duration) as median_duration
FROM sessions 
WHERE end_time IS NOT NULL;
```

#### 2. **Emotion Analysis**
```sql
-- Most common emotions
SELECT emotion, COUNT(*) as frequency
FROM interactions 
WHERE emotion_detected IS NOT NULL
GROUP BY emotion 
ORDER BY frequency DESC;

-- Emotion trends over time
SELECT DATE(timestamp) as date, emotion, COUNT(*) as count
FROM interactions 
WHERE timestamp >= NOW() - INTERVAL '7 days'
GROUP BY DATE(timestamp), emotion;
```

#### 3. **Therapeutic Outcomes**
```sql
-- User progress tracking
SELECT u.id, u.username, 
       COUNT(s.id) as total_sessions,
       AVG(m.mood_score) as avg_mood,
       MAX(s.created_at) as last_session
FROM users u
LEFT JOIN sessions s ON u.id = s.user_id
LEFT JOIN mood_entries m ON u.id = m.user_id
GROUP BY u.id, u.username;
```

### 🛠️ **Development Commands**

#### **Docker Management**
```bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f backend
docker-compose logs -f frontend

# Restart specific service
docker-compose restart backend

# Stop all services
docker-compose down

# Rebuild after dependency changes
docker-compose build backend
```

#### **Database Operations**
```bash
# Initialize database
docker-compose exec backend python init_database.py

# Run database migrations
docker-compose exec backend alembic upgrade head

# Access PostgreSQL
docker-compose exec db psql -U voice_cbt_user -d voice_cbt_db

# Access ClickHouse
docker-compose exec clickhouse clickhouse-client
```

#### **Testing**
```bash
# Run all tests
docker-compose exec backend python -m pytest tests/ -v

# Run specific test categories
docker-compose exec backend python -m pytest tests/test_api_endpoints.py
docker-compose exec backend python -m pytest tests/test_services.py
docker-compose exec backend python -m pytest tests/test_integration.py

# Run with coverage
docker-compose exec backend python -m pytest tests/ --cov=app --cov-report=html
```

### 📈 **Monitoring & Analytics**

#### **Grafana Dashboards**
- **System Overview**: CPU, memory, disk usage
- **Application Metrics**: Request rates, response times
- **User Analytics**: Active users, session trends
- **Therapeutic Outcomes**: Progress tracking, emotion trends

#### **Prometheus Metrics**
- **Application**: Request duration, error rates
- **System**: Resource utilization, service health
- **Business**: User engagement, therapeutic outcomes

### 🔒 **Security Features**

- **Authentication**: JWT tokens with refresh mechanism
- **Rate Limiting**: API request throttling
- **IP Blocking**: Malicious IP detection and blocking
- **Input Validation**: Comprehensive request validation
- **CORS**: Cross-origin request security
- **HTTPS**: SSL/TLS encryption (production)

### 🚀 **Production Deployment**

#### **Environment Setup**
```bash
# Copy production environment
cp backend/config.production.env backend/.env

# Update environment variables
# - Database credentials
# - JWT secrets
# - API keys
# - Domain settings
```

#### **Deploy to Production**
```bash
# Build production images
docker-compose -f docker-compose.prod.yml build

# Deploy with production config
docker-compose -f docker-compose.prod.yml up -d

# Initialize production database
docker-compose -f docker-compose.prod.yml exec backend python init_database.py
```

### 📚 **API Documentation**

Visit http://localhost:8000/docs for interactive API documentation with:
- **Endpoint descriptions**
- **Request/response schemas**
- **Authentication requirements**
- **Example requests**

### 🐛 **Troubleshooting**

#### **Common Issues**
```bash
# Check container status
docker-compose ps

# View container logs
docker-compose logs backend

# Restart services
docker-compose restart

# Check database connections
docker-compose exec backend python -c "from app.models.database import engine; print('DB OK')"
```

#### **Performance Issues**
- **High Memory Usage**: Increase Docker memory limits
- **Slow Responses**: Check database indexes
- **Connection Errors**: Verify database credentials

### 📞 **Support**

- **Documentation**: Check `/docs` folder
- **Issues**: GitHub Issues
- **Discussions**: GitHub Discussions
- **Email**: support@voice-cbt.com

---

## 🎉 **You're Ready!**

Your Voice CBT application is now fully set up with:
- ✅ **Frontend**: React application with voice interface
- ✅ **Backend**: FastAPI with AI services
- ✅ **Databases**: PostgreSQL + ClickHouse + ChromaDB
- ✅ **Monitoring**: Prometheus + Grafana
- ✅ **Security**: Authentication + rate limiting
- ✅ **Testing**: Comprehensive test suite

**Next Steps:**
1. Explore the frontend at http://localhost:3000
2. Check the API docs at http://localhost:8000/docs
3. Monitor with Grafana at http://localhost:3001
4. Start your first therapy session!

## 📚 Documentation

- **[Project Overview](PROJECT_OVERVIEW.md)** - Complete project summary
- **[Technical README](TECHNICAL_README.md)** - Deep technical documentation
- **[Documentation Hub](docs/README.md)** - All documentation organized
- **[Architecture](docs/architecture/)** - System design and flowcharts
- **[Deployment](docs/deployment/)** - Production deployment guides
- **[Development](docs/development/)** - Project management and planning

**Happy Therapy! 🎙️💙**#   v o i c e - c b t  
 