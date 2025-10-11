"""
Database models and connection management for Voice CBT application.
"""

from sqlalchemy import create_engine, Column, String, Integer, Float, DateTime, Text, Boolean, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.dialects.postgresql import UUID
import uuid
from datetime import datetime
from typing import Optional, List, Dict, Any
import os

# Database configuration
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@localhost:5432/voicecbt")

# Create engine
engine = create_engine(DATABASE_URL, echo=False)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

class User(Base):
    """User model for storing user information."""
    __tablename__ = "users"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(100), unique=True, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    is_active = Column(Boolean, default=True)
    preferences = Column(JSON, default={})

class Session(Base):
    """Therapy session model."""
    __tablename__ = "sessions"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), nullable=False)
    started_at = Column(DateTime, default=datetime.utcnow)
    ended_at = Column(DateTime, nullable=True)
    duration_minutes = Column(Integer, nullable=True)
    session_type = Column(String(50), default="voice_cbt")
    status = Column(String(20), default="active")  # active, completed, abandoned

class Interaction(Base):
    """Individual interaction within a session."""
    __tablename__ = "interactions"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    session_id = Column(UUID(as_uuid=True), nullable=False)
    user_id = Column(UUID(as_uuid=True), nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)
    
    # Audio and transcription data
    audio_data_hash = Column(String(64), nullable=True)  # Hash of audio for deduplication
    transcribed_text = Column(Text, nullable=True)
    
    # Emotion analysis
    detected_emotion = Column(String(50), nullable=True)
    emotion_confidence = Column(Float, nullable=True)
    emotion_features = Column(JSON, nullable=True)  # Raw emotion detection features
    
    # AI response
    therapeutic_response = Column(Text, nullable=True)
    response_audio_hash = Column(String(64), nullable=True)
    
    # Metadata
    processing_time_ms = Column(Integer, nullable=True)
    model_version = Column(String(20), nullable=True)
    error_message = Column(Text, nullable=True)

class MoodEntry(Base):
    """Mood tracking entries."""
    __tablename__ = "mood_entries"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)
    
    # Mood data
    emotion = Column(String(50), nullable=False)
    intensity = Column(Integer, nullable=False)  # 1-10 scale
    context = Column(Text, nullable=True)
    triggers = Column(JSON, nullable=True)
    
    # Additional metadata
    session_id = Column(UUID(as_uuid=True), nullable=True)
    source = Column(String(20), default="manual")  # manual, voice, api

class SystemMetrics(Base):
    """System performance and usage metrics."""
    __tablename__ = "system_metrics"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    timestamp = Column(DateTime, default=datetime.utcnow)
    
    # Performance metrics
    response_time_ms = Column(Integer, nullable=True)
    memory_usage_mb = Column(Float, nullable=True)
    cpu_usage_percent = Column(Float, nullable=True)
    
    # Usage metrics
    active_sessions = Column(Integer, default=0)
    total_interactions = Column(Integer, default=0)
    error_count = Column(Integer, default=0)
    
    # Model performance
    emotion_accuracy = Column(Float, nullable=True)
    stt_accuracy = Column(Float, nullable=True)
    model_loading_time_ms = Column(Integer, nullable=True)

class DatabaseManager:
    """Database manager for handling connections and operations."""
    
    def __init__(self):
        self.engine = engine
        self.SessionLocal = SessionLocal
    
    def get_db(self) -> Session:
        """Get database session."""
        db = self.SessionLocal()
        try:
            return db
        finally:
            db.close()
    
    def create_tables(self):
        """Create all database tables."""
        Base.metadata.create_all(bind=self.engine)
        print("✅ Database tables created successfully")
    
    def drop_tables(self):
        """Drop all database tables."""
        Base.metadata.drop_all(bind=self.engine)
        print("✅ Database tables dropped successfully")
    
    def reset_database(self):
        """Reset database by dropping and recreating tables."""
        self.drop_tables()
        self.create_tables()

# Global database manager instance
db_manager = DatabaseManager()

# Dependency for FastAPI
def get_database():
    """FastAPI dependency for database sessions."""
    db = db_manager.get_db()
    try:
        yield db
    finally:
        db.close()

# Database operations
class DatabaseOperations:
    """Database operations for Voice CBT application."""
    
    def __init__(self, db: Session):
        self.db = db
    
    # User operations
    def create_user(self, username: str, email: Optional[str] = None) -> User:
        """Create a new user."""
        user = User(username=username, email=email)
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user
    
    def get_user(self, user_id: str) -> Optional[User]:
        """Get user by ID."""
        return self.db.query(User).filter(User.id == user_id).first()
    
    def get_user_by_username(self, username: str) -> Optional[User]:
        """Get user by username."""
        return self.db.query(User).filter(User.username == username).first()
    
    # Session operations
    def create_session(self, user_id: str, session_type: str = "voice_cbt") -> Session:
        """Create a new therapy session."""
        session = Session(
            user_id=user_id,
            session_type=session_type
        )
        self.db.add(session)
        self.db.commit()
        self.db.refresh(session)
        return session
    
    def get_session(self, session_id: str) -> Optional[Session]:
        """Get session by ID."""
        return self.db.query(Session).filter(Session.id == session_id).first()
    
    def update_session(self, session_id: str, **kwargs) -> Optional[Session]:
        """Update session with new data."""
        session = self.get_session(session_id)
        if session:
            for key, value in kwargs.items():
                setattr(session, key, value)
            self.db.commit()
            self.db.refresh(session)
        return session
    
    def get_user_sessions(self, user_id: str, limit: int = 50) -> List[Session]:
        """Get user's recent sessions."""
        return self.db.query(Session).filter(
            Session.user_id == user_id
        ).order_by(Session.started_at.desc()).limit(limit).all()
    
    # Interaction operations
    def create_interaction(self, session_id: str, user_id: str, **kwargs) -> Interaction:
        """Create a new interaction."""
        interaction = Interaction(
            session_id=session_id,
            user_id=user_id,
            **kwargs
        )
        self.db.add(interaction)
        self.db.commit()
        self.db.refresh(interaction)
        return interaction
    
    def get_session_interactions(self, session_id: str) -> List[Interaction]:
        """Get all interactions for a session."""
        return self.db.query(Interaction).filter(
            Interaction.session_id == session_id
        ).order_by(Interaction.timestamp.asc()).all()
    
    # Mood operations
    def create_mood_entry(self, user_id: str, emotion: str, intensity: int, **kwargs) -> MoodEntry:
        """Create a new mood entry."""
        mood_entry = MoodEntry(
            user_id=user_id,
            emotion=emotion,
            intensity=intensity,
            **kwargs
        )
        self.db.add(mood_entry)
        self.db.commit()
        self.db.refresh(mood_entry)
        return mood_entry
    
    def get_user_mood_history(self, user_id: str, days: int = 30) -> List[MoodEntry]:
        """Get user's mood history."""
        from datetime import timedelta
        cutoff_date = datetime.utcnow() - timedelta(days=days)
        
        return self.db.query(MoodEntry).filter(
            MoodEntry.user_id == user_id,
            MoodEntry.timestamp >= cutoff_date
        ).order_by(MoodEntry.timestamp.desc()).all()
    
    def get_mood_trends(self, user_id: str, days: int = 30) -> Dict[str, Any]:
        """Get mood trends for a user."""
        mood_history = self.get_user_mood_history(user_id, days)
        
        if not mood_history:
            return {"trends": [], "average_intensity": 0, "emotion_distribution": {}}
        
        # Calculate trends
        emotions = [entry.emotion for entry in mood_history]
        intensities = [entry.intensity for entry in mood_history]
        
        emotion_counts = {}
        for emotion in emotions:
            emotion_counts[emotion] = emotion_counts.get(emotion, 0) + 1
        
        return {
            "trends": mood_history,
            "average_intensity": sum(intensities) / len(intensities),
            "emotion_distribution": emotion_counts,
            "total_entries": len(mood_history)
        }
    
    # Metrics operations
    def create_system_metric(self, **kwargs) -> SystemMetrics:
        """Create a system metrics entry."""
        metric = SystemMetrics(**kwargs)
        self.db.add(metric)
        self.db.commit()
        self.db.refresh(metric)
        return metric
    
    def get_recent_metrics(self, hours: int = 24) -> List[SystemMetrics]:
        """Get recent system metrics."""
        from datetime import timedelta
        cutoff_time = datetime.utcnow() - timedelta(hours=hours)
        
        return self.db.query(SystemMetrics).filter(
            SystemMetrics.timestamp >= cutoff_time
        ).order_by(SystemMetrics.timestamp.desc()).all()
