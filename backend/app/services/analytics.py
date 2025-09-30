"""
Analytics service for Voice CBT application.
Provides insights into user behavior, system performance, and therapeutic outcomes.
"""

import logging
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional, Tuple
from dataclasses import dataclass
from sqlalchemy.orm import Session
from sqlalchemy import func, desc, and_

from ..models.database import User, Session as TherapySession, Interaction, MoodEntry, SystemMetrics
from ..services.database_service import DatabaseService

logger = logging.getLogger(__name__)

@dataclass
class UserAnalytics:
    """User analytics data."""
    user_id: str
    total_sessions: int
    total_interactions: int
    average_session_duration: float
    most_common_emotions: List[Tuple[str, int]]
    mood_trend: str  # improving, declining, stable
    engagement_score: float
    last_activity: datetime

@dataclass
class SystemAnalytics:
    """System analytics data."""
    total_users: int
    active_users: int
    total_sessions: int
    total_interactions: int
    average_response_time: float
    system_uptime: float
    error_rate: float
    peak_usage_hour: int
    most_common_emotions: List[Tuple[str, int]]

class AnalyticsService:
    """Comprehensive analytics service."""
    
    def __init__(self, db: Session):
        self.db = db
        self.db_service = DatabaseService(db)
    
    def get_user_analytics(self, user_id: str, days: int = 30) -> Optional[UserAnalytics]:
        """Get comprehensive analytics for a specific user."""
        try:
            # Get user sessions
            sessions = self.db.query(TherapySession).filter(
                TherapySession.user_id == user_id,
                TherapySession.started_at >= datetime.now() - timedelta(days=days)
            ).all()
            
            if not sessions:
                return None
            
            # Get user interactions
            interactions = self.db.query(Interaction).filter(
                Interaction.user_id == user_id,
                Interaction.timestamp >= datetime.now() - timedelta(days=days)
            ).all()
            
            # Get mood entries
            mood_entries = self.db.query(MoodEntry).filter(
                MoodEntry.user_id == user_id,
                MoodEntry.timestamp >= datetime.now() - timedelta(days=days)
            ).all()
            
            # Calculate analytics
            total_sessions = len(sessions)
            total_interactions = len(interactions)
            
            # Average session duration
            completed_sessions = [s for s in sessions if s.duration_minutes]
            avg_duration = sum(s.duration_minutes for s in completed_sessions) / len(completed_sessions) if completed_sessions else 0
            
            # Most common emotions
            emotions = [i.detected_emotion for i in interactions if i.detected_emotion]
            emotion_counts = {}
            for emotion in emotions:
                emotion_counts[emotion] = emotion_counts.get(emotion, 0) + 1
            most_common_emotions = sorted(emotion_counts.items(), key=lambda x: x[1], reverse=True)[:5]
            
            # Mood trend analysis
            mood_trend = self._analyze_mood_trend(mood_entries)
            
            # Engagement score (based on session frequency and duration)
            engagement_score = self._calculate_engagement_score(sessions, interactions)
            
            # Last activity
            last_activity = max(
                max((s.started_at for s in sessions), default=datetime.min),
                max((i.timestamp for i in interactions), default=datetime.min)
            )
            
            return UserAnalytics(
                user_id=user_id,
                total_sessions=total_sessions,
                total_interactions=total_interactions,
                average_session_duration=avg_duration,
                most_common_emotions=most_common_emotions,
                mood_trend=mood_trend,
                engagement_score=engagement_score,
                last_activity=last_activity
            )
            
        except Exception as e:
            logger.error(f"Error getting user analytics for {user_id}: {e}")
            return None
    
    def get_system_analytics(self, days: int = 30) -> SystemAnalytics:
        """Get comprehensive system analytics."""
        try:
            cutoff_date = datetime.now() - timedelta(days=days)
            
            # Basic counts
            total_users = self.db.query(User).count()
            active_users = self.db.query(User).filter(
                User.created_at >= cutoff_date
            ).count()
            
            total_sessions = self.db.query(TherapySession).filter(
                TherapySession.started_at >= cutoff_date
            ).count()
            
            total_interactions = self.db.query(Interaction).filter(
                Interaction.timestamp >= cutoff_date
            ).count()
            
            # Average response time
            recent_metrics = self.db.query(SystemMetrics).filter(
                SystemMetrics.timestamp >= cutoff_date,
                SystemMetrics.response_time_ms.isnot(None)
            ).all()
            
            avg_response_time = sum(m.response_time_ms for m in recent_metrics) / len(recent_metrics) if recent_metrics else 0
            
            # System uptime (placeholder)
            system_uptime = 99.9  # Would need actual uptime tracking
            
            # Error rate
            total_errors = sum(m.error_count for m in recent_metrics)
            error_rate = total_errors / total_interactions if total_interactions > 0 else 0
            
            # Peak usage hour
            peak_hour = self._find_peak_usage_hour(interactions)
            
            # Most common emotions
            emotions = self.db.query(Interaction.detected_emotion, func.count(Interaction.id)).filter(
                Interaction.timestamp >= cutoff_date,
                Interaction.detected_emotion.isnot(None)
            ).group_by(Interaction.detected_emotion).all()
            
            most_common_emotions = sorted(emotions, key=lambda x: x[1], reverse=True)[:5]
            
            return SystemAnalytics(
                total_users=total_users,
                active_users=active_users,
                total_sessions=total_sessions,
                total_interactions=total_interactions,
                average_response_time=avg_response_time,
                system_uptime=system_uptime,
                error_rate=error_rate,
                peak_usage_hour=peak_hour,
                most_common_emotions=most_common_emotions
            )
            
        except Exception as e:
            logger.error(f"Error getting system analytics: {e}")
            return SystemAnalytics(0, 0, 0, 0, 0, 0, 0, 0, [])
    
    def get_emotion_analytics(self, days: int = 30) -> Dict[str, Any]:
        """Get emotion detection analytics."""
        try:
            cutoff_date = datetime.now() - timedelta(days=days)
            
            # Emotion distribution
            emotion_stats = self.db.query(
                Interaction.detected_emotion,
                func.count(Interaction.id).label('count'),
                func.avg(Interaction.emotion_confidence).label('avg_confidence')
            ).filter(
                Interaction.timestamp >= cutoff_date,
                Interaction.detected_emotion.isnot(None)
            ).group_by(Interaction.detected_emotion).all()
            
            # Confidence analysis
            confidence_stats = self.db.query(
                func.avg(Interaction.emotion_confidence).label('avg_confidence'),
                func.min(Interaction.emotion_confidence).label('min_confidence'),
                func.max(Interaction.emotion_confidence).label('max_confidence')
            ).filter(
                Interaction.timestamp >= cutoff_date,
                Interaction.emotion_confidence.isnot(None)
            ).first()
            
            return {
                "emotion_distribution": [
                    {"emotion": emotion, "count": count, "avg_confidence": float(avg_confidence)}
                    for emotion, count, avg_confidence in emotion_stats
                ],
                "confidence_stats": {
                    "average": float(confidence_stats.avg_confidence) if confidence_stats.avg_confidence else 0,
                    "minimum": float(confidence_stats.min_confidence) if confidence_stats.min_confidence else 0,
                    "maximum": float(confidence_stats.max_confidence) if confidence_stats.max_confidence else 0
                },
                "period_days": days
            }
            
        except Exception as e:
            logger.error(f"Error getting emotion analytics: {e}")
            return {"error": "Failed to retrieve emotion analytics"}
    
    def get_usage_patterns(self, days: int = 30) -> Dict[str, Any]:
        """Get usage pattern analytics."""
        try:
            cutoff_date = datetime.now() - timedelta(days=days)
            
            # Hourly usage patterns
            hourly_usage = self.db.query(
                func.extract('hour', Interaction.timestamp).label('hour'),
                func.count(Interaction.id).label('count')
            ).filter(
                Interaction.timestamp >= cutoff_date
            ).group_by(func.extract('hour', Interaction.timestamp)).all()
            
            # Daily usage patterns
            daily_usage = self.db.query(
                func.date(Interaction.timestamp).label('date'),
                func.count(Interaction.id).label('count')
            ).filter(
                Interaction.timestamp >= cutoff_date
            ).group_by(func.date(Interaction.timestamp)).all()
            
            # Session duration analysis
            session_durations = self.db.query(TherapySession.duration_minutes).filter(
                TherapySession.started_at >= cutoff_date,
                TherapySession.duration_minutes.isnot(None)
            ).all()
            
            durations = [s.duration_minutes for s in session_durations]
            avg_duration = sum(durations) / len(durations) if durations else 0
            
            return {
                "hourly_usage": [
                    {"hour": int(hour), "count": int(count)}
                    for hour, count in hourly_usage
                ],
                "daily_usage": [
                    {"date": date.isoformat(), "count": int(count)}
                    for date, count in daily_usage
                ],
                "session_duration": {
                    "average_minutes": avg_duration,
                    "total_sessions": len(durations)
                },
                "period_days": days
            }
            
        except Exception as e:
            logger.error(f"Error getting usage patterns: {e}")
            return {"error": "Failed to retrieve usage patterns"}
    
    def get_therapeutic_outcomes(self, days: int = 30) -> Dict[str, Any]:
        """Get therapeutic outcome analytics."""
        try:
            cutoff_date = datetime.now() - timedelta(days=days)
            
            # Mood trend analysis
            mood_entries = self.db.query(MoodEntry).filter(
                MoodEntry.timestamp >= cutoff_date
            ).order_by(MoodEntry.timestamp).all()
            
            # Analyze mood progression
            mood_progression = self._analyze_mood_progression(mood_entries)
            
            # Session effectiveness
            sessions = self.db.query(TherapySession).filter(
                TherapySession.started_at >= cutoff_date,
                TherapySession.duration_minutes.isnot(None)
            ).all()
            
            avg_session_duration = sum(s.duration_minutes for s in sessions) / len(sessions) if sessions else 0
            
            # User retention
            new_users = self.db.query(User).filter(
                User.created_at >= cutoff_date
            ).count()
            
            returning_users = self.db.query(User).filter(
                and_(
                    User.created_at < cutoff_date,
                    User.id.in_(
                        self.db.query(TherapySession.user_id).filter(
                            TherapySession.started_at >= cutoff_date
                        )
                    )
                )
            ).count()
            
            return {
                "mood_progression": mood_progression,
                "session_effectiveness": {
                    "average_duration_minutes": avg_session_duration,
                    "total_sessions": len(sessions)
                },
                "user_retention": {
                    "new_users": new_users,
                    "returning_users": returning_users,
                    "retention_rate": returning_users / (new_users + returning_users) if (new_users + returning_users) > 0 else 0
                },
                "period_days": days
            }
            
        except Exception as e:
            logger.error(f"Error getting therapeutic outcomes: {e}")
            return {"error": "Failed to retrieve therapeutic outcomes"}
    
    def _analyze_mood_trend(self, mood_entries: List[MoodEntry]) -> str:
        """Analyze mood trend from mood entries."""
        if len(mood_entries) < 2:
            return "insufficient_data"
        
        # Simple trend analysis based on intensity
        intensities = [entry.intensity for entry in mood_entries]
        first_half = intensities[:len(intensities)//2]
        second_half = intensities[len(intensities)//2:]
        
        avg_first = sum(first_half) / len(first_half)
        avg_second = sum(second_half) / len(second_half)
        
        if avg_second > avg_first + 1:
            return "improving"
        elif avg_second < avg_first - 1:
            return "declining"
        else:
            return "stable"
    
    def _calculate_engagement_score(self, sessions: List[TherapySession], interactions: List[Interaction]) -> float:
        """Calculate user engagement score."""
        if not sessions:
            return 0.0
        
        # Factors: session frequency, duration, interaction count
        session_frequency = len(sessions) / 30  # sessions per day
        avg_duration = sum(s.duration_minutes for s in sessions if s.duration_minutes) / len(sessions) if sessions else 0
        interaction_rate = len(interactions) / len(sessions) if sessions else 0
        
        # Normalize and combine
        score = (session_frequency * 0.4 + (avg_duration / 60) * 0.3 + interaction_rate * 0.3)
        return min(1.0, max(0.0, score))
    
    def _find_peak_usage_hour(self, interactions: List[Interaction]) -> int:
        """Find peak usage hour."""
        if not interactions:
            return 0
        
        hourly_counts = {}
        for interaction in interactions:
            hour = interaction.timestamp.hour
            hourly_counts[hour] = hourly_counts.get(hour, 0) + 1
        
        return max(hourly_counts.items(), key=lambda x: x[1])[0]
    
    def _analyze_mood_progression(self, mood_entries: List[MoodEntry]) -> Dict[str, Any]:
        """Analyze mood progression over time."""
        if len(mood_entries) < 2:
            return {"trend": "insufficient_data", "data_points": len(mood_entries)}
        
        # Group by emotion and analyze intensity trends
        emotion_trends = {}
        for entry in mood_entries:
            emotion = entry.emotion
            if emotion not in emotion_trends:
                emotion_trends[emotion] = []
            emotion_trends[emotion].append(entry.intensity)
        
        # Calculate trends for each emotion
        emotion_analysis = {}
        for emotion, intensities in emotion_trends.items():
            if len(intensities) >= 2:
                first_half = intensities[:len(intensities)//2]
                second_half = intensities[len(intensities)//2:]
                
                avg_first = sum(first_half) / len(first_half)
                avg_second = sum(second_half) / len(second_half)
                
                if avg_second > avg_first + 0.5:
                    trend = "increasing"
                elif avg_second < avg_first - 0.5:
                    trend = "decreasing"
                else:
                    trend = "stable"
                
                emotion_analysis[emotion] = {
                    "trend": trend,
                    "average_intensity": sum(intensities) / len(intensities),
                    "data_points": len(intensities)
                }
        
        return {
            "emotion_trends": emotion_analysis,
            "overall_trend": "mixed",  # Would need more sophisticated analysis
            "data_points": len(mood_entries)
        }
