"""
Advanced analytics API endpoints for Voice CBT dashboard.
Provides comprehensive insights and metrics.
"""

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta
import json

from ..models.database import get_database, User, Session as TherapySession, MoodEntry, Interaction
from ..core.logging import get_logger, LogContext
from ..core.exceptions import DatabaseError, ValidationError

router = APIRouter(prefix="/api/v1/analytics", tags=["analytics"])
logger = get_logger('voice-cbt.analytics')

@router.get("/overview")
async def get_analytics_overview(
    days: int = Query(30, description="Number of days to analyze"),
    db: Session = Depends(get_database)
):
    """Get comprehensive analytics overview."""
    
    with LogContext(logger, endpoint="analytics_overview", days=days):
        try:
            # Calculate date range
            end_date = datetime.now()
            start_date = end_date - timedelta(days=days)
            
            # Get basic metrics
            total_users = db.query(User).count()
            active_users = db.query(User).filter(User.is_active == True).count()
            
            # Session metrics
            total_sessions = db.query(TherapySession).filter(
                TherapySession.started_at >= start_date
            ).count()
            
            completed_sessions = db.query(TherapySession).filter(
                TherapySession.started_at >= start_date,
                TherapySession.status == "completed"
            ).count()
            
            # Average session duration
            sessions_with_duration = db.query(TherapySession).filter(
                TherapySession.started_at >= start_date,
                TherapySession.duration_minutes.isnot(None)
            ).all()
            
            avg_duration = sum(s.duration_minutes for s in sessions_with_duration) / len(sessions_with_duration) if sessions_with_duration else 0
            
            # Mood analytics
            mood_entries = db.query(MoodEntry).filter(
                MoodEntry.timestamp >= start_date
            ).all()
            
            # Emotion distribution
            emotion_counts = {}
            for entry in mood_entries:
                emotion = entry.emotion
                emotion_counts[emotion] = emotion_counts.get(emotion, 0) + 1
            
            # Calculate emotion percentages
            total_mood_entries = len(mood_entries)
            emotion_percentages = {
                emotion: (count / total_mood_entries * 100) if total_mood_entries > 0 else 0
                for emotion, count in emotion_counts.items()
            }
            
            # Recent activity (last 7 days)
            recent_start = end_date - timedelta(days=7)
            recent_sessions = db.query(TherapySession).filter(
                TherapySession.started_at >= recent_start
            ).count()
            
            recent_mood_entries = db.query(MoodEntry).filter(
                MoodEntry.timestamp >= recent_start
            ).count()
            
            return {
                "period": {
                    "start_date": start_date.isoformat(),
                    "end_date": end_date.isoformat(),
                    "days": days
                },
                "users": {
                    "total": total_users,
                    "active": active_users,
                    "growth_rate": 0  # TODO: Calculate growth rate
                },
                "sessions": {
                    "total": total_sessions,
                    "completed": completed_sessions,
                    "completion_rate": (completed_sessions / total_sessions * 100) if total_sessions > 0 else 0,
                    "average_duration_minutes": round(avg_duration, 2)
                },
                "emotions": {
                    "total_entries": total_mood_entries,
                    "distribution": emotion_percentages,
                    "most_common": max(emotion_counts.items(), key=lambda x: x[1])[0] if emotion_counts else "neutral"
                },
                "recent_activity": {
                    "sessions_last_7_days": recent_sessions,
                    "mood_entries_last_7_days": recent_mood_entries
                }
            }
            
        except Exception as e:
            logger.error(f"Error getting analytics overview: {e}")
            raise DatabaseError("Failed to retrieve analytics overview")

@router.get("/emotions/trends")
async def get_emotion_trends(
    days: int = Query(30, description="Number of days to analyze"),
    db: Session = Depends(get_database)
):
    """Get emotion trends over time."""
    
    with LogContext(logger, endpoint="emotion_trends", days=days):
        try:
            end_date = datetime.now()
            start_date = end_date - timedelta(days=days)
            
            # Get mood entries grouped by day
            mood_entries = db.query(MoodEntry).filter(
                MoodEntry.timestamp >= start_date
            ).order_by(MoodEntry.timestamp).all()
            
            # Group by date and emotion
            daily_emotions = {}
            for entry in mood_entries:
                date_key = entry.timestamp.date().isoformat()
                if date_key not in daily_emotions:
                    daily_emotions[date_key] = {}
                daily_emotions[date_key][entry.emotion] = daily_emotions[date_key].get(entry.emotion, 0) + 1
            
            # Calculate trends
            trends = []
            for date, emotions in daily_emotions.items():
                total = sum(emotions.values())
                trends.append({
                    "date": date,
                    "total_entries": total,
                    "emotions": emotions,
                    "percentages": {
                        emotion: (count / total * 100) if total > 0 else 0
                        for emotion, count in emotions.items()
                    }
                })
            
            return {
                "period": {
                    "start_date": start_date.isoformat(),
                    "end_date": end_date.isoformat(),
                    "days": days
                },
                "trends": trends
            }
            
        except Exception as e:
            logger.error(f"Error getting emotion trends: {e}")
            raise DatabaseError("Failed to retrieve emotion trends")

@router.get("/sessions/analytics")
async def get_session_analytics(
    days: int = Query(30, description="Number of days to analyze"),
    db: Session = Depends(get_database)
):
    """Get detailed session analytics."""
    
    with LogContext(logger, endpoint="session_analytics", days=days):
        try:
            end_date = datetime.now()
            start_date = end_date - timedelta(days=days)
            
            # Get sessions
            sessions = db.query(TherapySession).filter(
                TherapySession.started_at >= start_date
            ).all()
            
            # Calculate metrics
            total_sessions = len(sessions)
            completed_sessions = len([s for s in sessions if s.status == "completed"])
            active_sessions = len([s for s in sessions if s.status == "active"])
            
            # Duration analysis
            sessions_with_duration = [s for s in sessions if s.duration_minutes is not None]
            durations = [s.duration_minutes for s in sessions_with_duration]
            
            duration_stats = {
                "average": sum(durations) / len(durations) if durations else 0,
                "min": min(durations) if durations else 0,
                "max": max(durations) if durations else 0,
                "median": sorted(durations)[len(durations)//2] if durations else 0
            }
            
            # Session types
            session_types = {}
            for session in sessions:
                session_type = session.session_type
                session_types[session_type] = session_types.get(session_type, 0) + 1
            
            # Daily session counts
            daily_sessions = {}
            for session in sessions:
                date_key = session.started_at.date().isoformat()
                daily_sessions[date_key] = daily_sessions.get(date_key, 0) + 1
            
            return {
                "period": {
                    "start_date": start_date.isoformat(),
                    "end_date": end_date.isoformat(),
                    "days": days
                },
                "summary": {
                    "total_sessions": total_sessions,
                    "completed_sessions": completed_sessions,
                    "active_sessions": active_sessions,
                    "completion_rate": (completed_sessions / total_sessions * 100) if total_sessions > 0 else 0
                },
                "duration_stats": duration_stats,
                "session_types": session_types,
                "daily_counts": daily_sessions
            }
            
        except Exception as e:
            logger.error(f"Error getting session analytics: {e}")
            raise DatabaseError("Failed to retrieve session analytics")

@router.get("/users/engagement")
async def get_user_engagement(
    days: int = Query(30, description="Number of days to analyze"),
    db: Session = Depends(get_database)
):
    """Get user engagement metrics."""
    
    with LogContext(logger, endpoint="user_engagement", days=days):
        try:
            end_date = datetime.now()
            start_date = end_date - timedelta(days=days)
            
            # Get users who were active in the period
            active_users = db.query(User).filter(
                User.is_active == True
            ).all()
            
            # Calculate engagement metrics for each user
            user_engagement = []
            for user in active_users:
                # Get user's sessions in the period
                user_sessions = db.query(TherapySession).filter(
                    TherapySession.user_id == user.id,
                    TherapySession.started_at >= start_date
                ).all()
                
                # Get user's mood entries
                user_mood_entries = db.query(MoodEntry).filter(
                    MoodEntry.user_id == user.id,
                    MoodEntry.timestamp >= start_date
                ).all()
                
                engagement_score = len(user_sessions) * 0.7 + len(user_mood_entries) * 0.3
                
                user_engagement.append({
                    "user_id": str(user.id),
                    "username": user.username,
                    "sessions_count": len(user_sessions),
                    "mood_entries_count": len(user_mood_entries),
                    "engagement_score": round(engagement_score, 2),
                    "last_activity": max(
                        [s.started_at for s in user_sessions] + 
                        [m.timestamp for m in user_mood_entries],
                        default=None
                    ).isoformat() if user_sessions or user_mood_entries else None
                })
            
            # Sort by engagement score
            user_engagement.sort(key=lambda x: x["engagement_score"], reverse=True)
            
            return {
                "period": {
                    "start_date": start_date.isoformat(),
                    "end_date": end_date.isoformat(),
                    "days": days
                },
                "total_active_users": len(active_users),
                "user_engagement": user_engagement[:50],  # Top 50 users
                "average_engagement": sum(u["engagement_score"] for u in user_engagement) / len(user_engagement) if user_engagement else 0
            }
            
        except Exception as e:
            logger.error(f"Error getting user engagement: {e}")
            raise DatabaseError("Failed to retrieve user engagement metrics")

@router.get("/health/metrics")
async def get_health_metrics(db: Session = Depends(get_database)):
    """Get system health metrics."""
    
    with LogContext(logger, endpoint="health_metrics"):
        try:
            # Database health
            db_health = {
                "users_count": db.query(User).count(),
                "sessions_count": db.query(TherapySession).count(),
                "mood_entries_count": db.query(MoodEntry).count(),
                "interactions_count": db.query(Interaction).count()
            }
            
            # Recent activity (last hour)
            recent_start = datetime.now() - timedelta(hours=1)
            recent_activity = {
                "sessions_last_hour": db.query(TherapySession).filter(
                    TherapySession.started_at >= recent_start
                ).count(),
                "mood_entries_last_hour": db.query(MoodEntry).filter(
                    MoodEntry.timestamp >= recent_start
                ).count()
            }
            
            return {
                "timestamp": datetime.now().isoformat(),
                "database_health": db_health,
                "recent_activity": recent_activity,
                "status": "healthy"
            }
            
        except Exception as e:
            logger.error(f"Error getting health metrics: {e}")
            raise DatabaseError("Failed to retrieve health metrics")
