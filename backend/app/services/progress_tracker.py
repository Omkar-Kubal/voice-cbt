"""
Progress tracking service for user mood, session analytics, and therapeutic outcomes.
"""

from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime, timedelta
import json
import statistics

class ProgressTracker:
    """
    Tracks user progress, mood trends, and therapeutic outcomes.
    """
    
    def __init__(self):
        self.user_progress: Dict[str, Dict[str, Any]] = {}
        self.mood_history: Dict[str, List[Dict[str, Any]]] = {}
        self.session_analytics: Dict[str, List[Dict[str, Any]]] = {}
        
    def track_mood(self, user_id: str, emotion: str, confidence: float, 
                   session_id: str, context: str = "") -> Dict[str, Any]:
        """
        Track user mood with timestamp and context.
        
        Args:
            user_id: User identifier
            emotion: Detected emotion
            confidence: Emotion confidence score
            session_id: Session identifier
            context: Additional context
            
        Returns:
            Mood tracking data
        """
        timestamp = datetime.now().isoformat()
        mood_entry = {
            "timestamp": timestamp,
            "emotion": emotion,
            "confidence": confidence,
            "session_id": session_id,
            "context": context,
            "mood_score": self._emotion_to_score(emotion, confidence)
        }
        
        # Initialize user progress if not exists
        if user_id not in self.user_progress:
            self.user_progress[user_id] = {
                "user_id": user_id,
                "first_session": timestamp,
                "total_sessions": 0,
                "total_exchanges": 0,
                "mood_trend": "neutral",
                "progress_score": 0.0,
                "therapeutic_goals": [],
                "achievements": []
            }
        
        # Add to mood history
        if user_id not in self.mood_history:
            self.mood_history[user_id] = []
        
        self.mood_history[user_id].append(mood_entry)
        
        # Update user progress
        self._update_user_progress(user_id, mood_entry)
        
        print(f"📊 Tracked mood for user {user_id}: {emotion} (score: {mood_entry['mood_score']:.2f})")
        return mood_entry
    
    def track_session(self, user_id: str, session_id: str, 
                     session_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Track session analytics and outcomes.
        
        Args:
            user_id: User identifier
            session_id: Session identifier
            session_data: Session information
            
        Returns:
            Session analytics
        """
        timestamp = datetime.now().isoformat()
        session_analytics = {
            "session_id": session_id,
            "user_id": user_id,
            "timestamp": timestamp,
            "duration_minutes": session_data.get("duration_minutes", 0),
            "exchange_count": session_data.get("exchange_count", 0),
            "emotions_discussed": session_data.get("emotions_discussed", []),
            "topics_covered": session_data.get("topics_covered", []),
            "therapeutic_techniques_used": session_data.get("techniques_used", []),
            "session_effectiveness": self._calculate_session_effectiveness(session_data),
            "user_satisfaction": session_data.get("satisfaction_score", 0.0)
        }
        
        # Add to session analytics
        if user_id not in self.session_analytics:
            self.session_analytics[user_id] = []
        
        self.session_analytics[user_id].append(session_analytics)
        
        # Update user progress
        self.user_progress[user_id]["total_sessions"] += 1
        self.user_progress[user_id]["total_exchanges"] += session_data.get("exchange_count", 0)
        
        print(f"📈 Tracked session for user {user_id}: {session_analytics['session_effectiveness']:.2f} effectiveness")
        return session_analytics
    
    def get_user_progress(self, user_id: str) -> Dict[str, Any]:
        """
        Get comprehensive user progress report.
        
        Args:
            user_id: User identifier
            
        Returns:
            User progress report
        """
        if user_id not in self.user_progress:
            return {"error": "User not found"}
        
        user_data = self.user_progress[user_id]
        mood_data = self.mood_history.get(user_id, [])
        session_data = self.session_analytics.get(user_id, [])
        
        # Calculate mood trends
        mood_trends = self._analyze_mood_trends(mood_data)
        
        # Calculate session effectiveness
        session_effectiveness = self._calculate_overall_effectiveness(session_data)
        
        # Generate progress insights
        insights = self._generate_progress_insights(user_data, mood_trends, session_effectiveness)
        
        return {
            "user_id": user_id,
            "progress_summary": user_data,
            "mood_trends": mood_trends,
            "session_analytics": {
                "total_sessions": len(session_data),
                "average_effectiveness": session_effectiveness,
                "recent_sessions": session_data[-5:] if session_data else []
            },
            "progress_insights": insights,
            "recommendations": self._generate_recommendations(mood_trends, session_effectiveness)
        }
    
    def get_mood_analytics(self, user_id: str, days: int = 30) -> Dict[str, Any]:
        """
        Get mood analytics for a specific time period.
        
        Args:
            user_id: User identifier
            days: Number of days to analyze
            
        Returns:
            Mood analytics report
        """
        if user_id not in self.mood_history:
            return {"error": "No mood data found"}
        
        # Filter data by date range
        cutoff_date = datetime.now() - timedelta(days=days)
        recent_moods = [
            mood for mood in self.mood_history[user_id]
            if datetime.fromisoformat(mood["timestamp"]) >= cutoff_date
        ]
        
        if not recent_moods:
            return {"error": "No recent mood data"}
        
        # Analyze mood patterns
        emotion_counts = {}
        mood_scores = []
        daily_averages = {}
        
        for mood in recent_moods:
            emotion = mood["emotion"]
            emotion_counts[emotion] = emotion_counts.get(emotion, 0) + 1
            mood_scores.append(mood["mood_score"])
            
            # Group by day
            date = mood["timestamp"][:10]
            if date not in daily_averages:
                daily_averages[date] = []
            daily_averages[date].append(mood["mood_score"])
        
        # Calculate daily averages
        daily_trends = {
            date: statistics.mean(scores) 
            for date, scores in daily_averages.items()
        }
        
        return {
            "period_days": days,
            "total_entries": len(recent_moods),
            "emotion_distribution": emotion_counts,
            "average_mood_score": statistics.mean(mood_scores),
            "mood_score_trend": self._calculate_trend(mood_scores),
            "daily_averages": daily_trends,
            "most_common_emotion": max(emotion_counts, key=emotion_counts.get),
            "mood_stability": self._calculate_mood_stability(mood_scores)
        }
    
    def _emotion_to_score(self, emotion: str, confidence: float) -> float:
        """Convert emotion to numerical score (-1 to 1)."""
        emotion_scores = {
            "happiness": 0.8,
            "joy": 0.9,
            "content": 0.6,
            "neutral": 0.0,
            "sadness": -0.6,
            "depression": -0.8,
            "anxiety": -0.4,
            "fear": -0.5,
            "anger": -0.3,
            "frustration": -0.2
        }
        
        base_score = emotion_scores.get(emotion, 0.0)
        return base_score * confidence
    
    def _update_user_progress(self, user_id: str, mood_entry: Dict[str, Any]) -> None:
        """Update user progress based on mood entry."""
        user_data = self.user_progress[user_id]
        user_data["total_exchanges"] += 1
        
        # Update mood trend
        recent_moods = self.mood_history[user_id][-10:]  # Last 10 moods
        if len(recent_moods) >= 3:
            recent_scores = [m["mood_score"] for m in recent_moods]
            trend = self._calculate_trend(recent_scores)
            user_data["mood_trend"] = trend
        
        # Update progress score
        if len(recent_moods) >= 5:
            avg_score = statistics.mean([m["mood_score"] for m in recent_moods])
            user_data["progress_score"] = max(0, min(1, (avg_score + 1) / 2))  # Normalize to 0-1
    
    def _analyze_mood_trends(self, mood_data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze mood trends from mood data."""
        if not mood_data:
            return {"trend": "insufficient_data"}
        
        scores = [m["mood_score"] for m in mood_data]
        emotions = [m["emotion"] for m in mood_data]
        
        return {
            "trend": self._calculate_trend(scores),
            "average_score": statistics.mean(scores),
            "score_range": [min(scores), max(scores)],
            "most_common_emotion": max(set(emotions), key=emotions.count),
            "stability": self._calculate_mood_stability(scores)
        }
    
    def _calculate_session_effectiveness(self, session_data: Dict[str, Any]) -> float:
        """Calculate session effectiveness score."""
        effectiveness = 0.5  # Base score
        
        # Factors that increase effectiveness
        if session_data.get("exchange_count", 0) > 5:
            effectiveness += 0.1
        if len(session_data.get("topics_covered", [])) > 2:
            effectiveness += 0.1
        if len(session_data.get("techniques_used", [])) > 0:
            effectiveness += 0.2
        if session_data.get("satisfaction_score", 0) > 0.7:
            effectiveness += 0.1
        
        return min(1.0, effectiveness)
    
    def _calculate_overall_effectiveness(self, session_data: List[Dict[str, Any]]) -> float:
        """Calculate overall session effectiveness."""
        if not session_data:
            return 0.0
        
        effectiveness_scores = [s["session_effectiveness"] for s in session_data]
        return statistics.mean(effectiveness_scores)
    
    def _calculate_trend(self, scores: List[float]) -> str:
        """Calculate trend from score list."""
        if len(scores) < 3:
            return "insufficient_data"
        
        recent_avg = statistics.mean(scores[-3:])
        earlier_avg = statistics.mean(scores[:-3]) if len(scores) > 3 else recent_avg
        
        if recent_avg > earlier_avg + 0.1:
            return "improving"
        elif recent_avg < earlier_avg - 0.1:
            return "declining"
        else:
            return "stable"
    
    def _calculate_mood_stability(self, scores: List[float]) -> str:
        """Calculate mood stability."""
        if len(scores) < 3:
            return "insufficient_data"
        
        variance = statistics.variance(scores)
        if variance < 0.1:
            return "very_stable"
        elif variance < 0.3:
            return "stable"
        elif variance < 0.5:
            return "variable"
        else:
            return "unstable"
    
    def _generate_progress_insights(self, user_data: Dict, mood_trends: Dict, 
                                   session_effectiveness: float) -> List[str]:
        """Generate progress insights."""
        insights = []
        
        if user_data["total_sessions"] > 0:
            insights.append(f"Completed {user_data['total_sessions']} therapy sessions")
        
        if mood_trends.get("trend") == "improving":
            insights.append("Mood trend is showing improvement")
        elif mood_trends.get("trend") == "declining":
            insights.append("Mood trend needs attention")
        
        if session_effectiveness > 0.7:
            insights.append("High session effectiveness")
        elif session_effectiveness < 0.4:
            insights.append("Sessions could be more effective")
        
        if user_data["progress_score"] > 0.7:
            insights.append("Strong therapeutic progress")
        elif user_data["progress_score"] < 0.3:
            insights.append("Consider additional support")
        
        return insights
    
    def _generate_recommendations(self, mood_trends: Dict, session_effectiveness: float) -> List[str]:
        """Generate therapeutic recommendations."""
        recommendations = []
        
        if mood_trends.get("trend") == "declining":
            recommendations.append("Consider increasing session frequency")
            recommendations.append("Focus on coping strategies for difficult emotions")
        
        if session_effectiveness < 0.5:
            recommendations.append("Try different therapeutic approaches")
            recommendations.append("Consider longer session durations")
        
        if mood_trends.get("stability") == "unstable":
            recommendations.append("Practice daily mood tracking")
            recommendations.append("Focus on emotional regulation techniques")
        
        if not recommendations:
            recommendations.append("Continue current therapeutic approach")
            recommendations.append("Maintain regular session schedule")
        
        return recommendations

# Global progress tracker instance
progress_tracker = ProgressTracker()
