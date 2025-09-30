"""
Database service for Voice CBT application.
Handles all database operations with proper error handling and logging.
"""

import logging
from typing import Optional, List, Dict, Any
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from ..models.database import (
    DatabaseOperations, User, Session as TherapySession, 
    Interaction, MoodEntry, SystemMetrics
)

logger = logging.getLogger(__name__)

class DatabaseService:
    """Service class for database operations."""
    
    def __init__(self, db: Session):
        self.db = db
        self.ops = DatabaseOperations(db)
    
    # User management
    def create_or_get_user(self, username: str, email: Optional[str] = None) -> User:
        """Create a new user or get existing one."""
        try:
            # Try to get existing user
            user = self.ops.get_user_by_username(username)
            if user:
                logger.info(f"Found existing user: {username}")
                return user
            
            # Create new user
            user = self.ops.create_user(username, email)
            logger.info(f"Created new user: {username}")
            return user
            
        except SQLAlchemyError as e:
            logger.error(f"Error creating/getting user {username}: {e}")
            raise
    
    def get_user_profile(self, user_id: str) -> Optional[Dict[str, Any]]:
        """Get user profile with statistics."""
        try:
            user = self.ops.get_user(user_id)
            if not user:
                return None
            
            # Get user statistics
            sessions = self.ops.get_user_sessions(user_id, limit=100)
            mood_history = self.ops.get_user_mood_history(user_id, days=30)
            
            return {
                "user": {
                    "id": str(user.id),
                    "username": user.username,
                    "email": user.email,
                    "created_at": user.created_at.isoformat(),
                    "is_active": user.is_active
                },
                "statistics": {
                    "total_sessions": len(sessions),
                    "total_mood_entries": len(mood_history),
                    "last_session": sessions[0].started_at.isoformat() if sessions else None
                }
            }
            
        except SQLAlchemyError as e:
            logger.error(f"Error getting user profile {user_id}: {e}")
            return None
    
    # Session management
    def start_therapy_session(self, user_id: str, session_type: str = "voice_cbt") -> Optional[Dict[str, Any]]:
        """Start a new therapy session."""
        try:
            session = self.ops.create_session(user_id, session_type)
            logger.info(f"Started new session {session.id} for user {user_id}")
            
            return {
                "session_id": str(session.id),
                "user_id": str(session.user_id),
                "started_at": session.started_at.isoformat(),
                "session_type": session.session_type,
                "status": session.status
            }
            
        except SQLAlchemyError as e:
            logger.error(f"Error starting session for user {user_id}: {e}")
            return None
    
    def end_therapy_session(self, session_id: str) -> bool:
        """End a therapy session."""
        try:
            session = self.ops.get_session(session_id)
            if not session:
                logger.warning(f"Session {session_id} not found")
                return False
            
            # Calculate duration
            duration = datetime.utcnow() - session.started_at
            duration_minutes = int(duration.total_seconds() / 60)
            
            # Update session
            updated_session = self.ops.update_session(
                session_id,
                ended_at=datetime.utcnow(),
                duration_minutes=duration_minutes,
                status="completed"
            )
            
            if updated_session:
                logger.info(f"Ended session {session_id}, duration: {duration_minutes} minutes")
                return True
            
            return False
            
        except SQLAlchemyError as e:
            logger.error(f"Error ending session {session_id}: {e}")
            return False
    
    def get_session_summary(self, session_id: str) -> Optional[Dict[str, Any]]:
        """Get session summary with interactions."""
        try:
            session = self.ops.get_session(session_id)
            if not session:
                return None
            
            interactions = self.ops.get_session_interactions(session_id)
            
            # Calculate session statistics
            emotions = [i.detected_emotion for i in interactions if i.detected_emotion]
            emotion_counts = {}
            for emotion in emotions:
                emotion_counts[emotion] = emotion_counts.get(emotion, 0) + 1
            
            # Calculate average confidence
            confidences = [i.emotion_confidence for i in interactions if i.emotion_confidence]
            avg_confidence = sum(confidences) / len(confidences) if confidences else 0
            
            return {
                "session": {
                    "id": str(session.id),
                    "user_id": str(session.user_id),
                    "started_at": session.started_at.isoformat(),
                    "ended_at": session.ended_at.isoformat() if session.ended_at else None,
                    "duration_minutes": session.duration_minutes,
                    "status": session.status
                },
                "interactions": [
                    {
                        "id": str(i.id),
                        "timestamp": i.timestamp.isoformat(),
                        "transcribed_text": i.transcribed_text,
                        "detected_emotion": i.detected_emotion,
                        "emotion_confidence": i.emotion_confidence,
                        "therapeutic_response": i.therapeutic_response
                    }
                    for i in interactions
                ],
                "statistics": {
                    "total_interactions": len(interactions),
                    "emotion_distribution": emotion_counts,
                    "average_confidence": avg_confidence,
                    "processing_errors": len([i for i in interactions if i.error_message])
                }
            }
            
        except SQLAlchemyError as e:
            logger.error(f"Error getting session summary {session_id}: {e}")
            return None
    
    # Interaction logging
    def log_interaction(self, session_id: str, user_id: str, **interaction_data) -> Optional[Dict[str, Any]]:
        """Log a new interaction."""
        try:
            interaction = self.ops.create_interaction(session_id, user_id, **interaction_data)
            logger.info(f"Logged interaction {interaction.id} for session {session_id}")
            
            return {
                "interaction_id": str(interaction.id),
                "timestamp": interaction.timestamp.isoformat(),
                "detected_emotion": interaction.detected_emotion,
                "confidence": interaction.emotion_confidence
            }
            
        except SQLAlchemyError as e:
            logger.error(f"Error logging interaction for session {session_id}: {e}")
            return None
    
    # Mood tracking
    def log_mood_entry(self, user_id: str, emotion: str, intensity: int, **mood_data) -> Optional[Dict[str, Any]]:
        """Log a mood entry."""
        try:
            # Validate intensity
            if not (1 <= intensity <= 10):
                logger.warning(f"Invalid intensity {intensity} for user {user_id}")
                intensity = max(1, min(10, intensity))  # Clamp to valid range
            
            mood_entry = self.ops.create_mood_entry(user_id, emotion, intensity, **mood_data)
            logger.info(f"Logged mood entry {mood_entry.id} for user {user_id}")
            
            return {
                "mood_entry_id": str(mood_entry.id),
                "timestamp": mood_entry.timestamp.isoformat(),
                "emotion": mood_entry.emotion,
                "intensity": mood_entry.intensity
            }
            
        except SQLAlchemyError as e:
            logger.error(f"Error logging mood entry for user {user_id}: {e}")
            return None
    
    def get_mood_analytics(self, user_id: str, days: int = 30) -> Dict[str, Any]:
        """Get comprehensive mood analytics for a user."""
        try:
            trends_data = self.ops.get_mood_trends(user_id, days)
            
            if not trends_data["trends"]:
                return {
                    "message": "No mood data available",
                    "trends": [],
                    "analytics": {}
                }
            
            # Calculate additional analytics
            mood_history = trends_data["trends"]
            intensities = [entry.intensity for entry in mood_history]
            emotions = [entry.emotion for entry in mood_history]
            
            # Time-based analysis
            recent_week = [entry for entry in mood_history 
                          if entry.timestamp >= datetime.utcnow() - timedelta(days=7)]
            
            # Emotion trends over time
            emotion_timeline = []
            for entry in mood_history[-10:]:  # Last 10 entries
                emotion_timeline.append({
                    "date": entry.timestamp.isoformat(),
                    "emotion": entry.emotion,
                    "intensity": entry.intensity
                })
            
            return {
                "trends": emotion_timeline,
                "analytics": {
                    "total_entries": len(mood_history),
                    "average_intensity": trends_data["average_intensity"],
                    "emotion_distribution": trends_data["emotion_distribution"],
                    "recent_week_entries": len(recent_week),
                    "most_common_emotion": max(trends_data["emotion_distribution"].items(), 
                                             key=lambda x: x[1])[0] if trends_data["emotion_distribution"] else None,
                    "intensity_range": {
                        "min": min(intensities),
                        "max": max(intensities)
                    }
                }
            }
            
        except SQLAlchemyError as e:
            logger.error(f"Error getting mood analytics for user {user_id}: {e}")
            return {"error": "Failed to retrieve mood analytics"}
    
    # System metrics
    def log_system_metrics(self, **metrics_data) -> bool:
        """Log system performance metrics."""
        try:
            self.ops.create_system_metric(**metrics_data)
            return True
        except SQLAlchemyError as e:
            logger.error(f"Error logging system metrics: {e}")
            return False
    
    def get_system_health(self, hours: int = 24) -> Dict[str, Any]:
        """Get system health metrics."""
        try:
            metrics = self.ops.get_recent_metrics(hours)
            
            if not metrics:
                return {"status": "no_data", "message": "No metrics available"}
            
            # Calculate averages
            response_times = [m.response_time_ms for m in metrics if m.response_time_ms]
            memory_usage = [m.memory_usage_mb for m in metrics if m.memory_usage_mb]
            error_counts = [m.error_count for m in metrics if m.error_count]
            
            avg_response_time = sum(response_times) / len(response_times) if response_times else 0
            avg_memory = sum(memory_usage) / len(memory_usage) if memory_usage else 0
            total_errors = sum(error_counts)
            
            # Determine health status
            health_status = "healthy"
            if avg_response_time > 5000:  # > 5 seconds
                health_status = "degraded"
            if total_errors > 10:
                health_status = "unhealthy"
            
            return {
                "status": health_status,
                "metrics": {
                    "average_response_time_ms": avg_response_time,
                    "average_memory_usage_mb": avg_memory,
                    "total_errors": total_errors,
                    "data_points": len(metrics)
                },
                "timestamp": datetime.utcnow().isoformat()
            }
            
        except SQLAlchemyError as e:
            logger.error(f"Error getting system health: {e}")
            return {"status": "error", "message": "Failed to retrieve system health"}
