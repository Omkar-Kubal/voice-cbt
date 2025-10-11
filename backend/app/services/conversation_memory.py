"""
Conversation memory service for tracking user sessions and conversation history.
"""

from typing import Dict, List, Optional, Any
from datetime import datetime
import json

class ConversationMemory:
    """
    Manages conversation memory and session tracking.
    """
    
    def __init__(self):
        self.sessions: Dict[str, Dict[str, Any]] = {}
        self.max_session_length = 20  # Keep last 20 exchanges per session
    
    def start_session(self, session_id: str, user_id: Optional[str] = None) -> Dict[str, Any]:
        """
        Start a new conversation session.
        
        Args:
            session_id: Unique session identifier
            user_id: Optional user identifier
            
        Returns:
            Session information
        """
        self.sessions[session_id] = {
            "session_id": session_id,
            "user_id": user_id,
            "start_time": datetime.now().isoformat(),
            "conversation_history": [],
            "emotion_history": [],
            "topics_discussed": set(),
            "session_summary": ""
        }
        
        print(f"🔄 Started new session: {session_id}")
        return self.sessions[session_id]
    
    def add_exchange(self, session_id: str, user_input: str, emotion: str, 
                    response: str, timestamp: Optional[str] = None) -> None:
        """
        Add a conversation exchange to the session.
        
        Args:
            session_id: Session identifier
            user_input: User's input text
            emotion: Detected emotion
            response: System response
            timestamp: Optional timestamp
        """
        if session_id not in self.sessions:
            self.start_session(session_id)
        
        if timestamp is None:
            timestamp = datetime.now().isoformat()
        
        exchange = {
            "timestamp": timestamp,
            "user_input": user_input,
            "emotion": emotion,
            "response": response,
            "exchange_id": len(self.sessions[session_id]["conversation_history"])
        }
        
        # Add to conversation history
        self.sessions[session_id]["conversation_history"].append(exchange)
        
        # Add to emotion history
        self.sessions[session_id]["emotion_history"].append({
            "timestamp": timestamp,
            "emotion": emotion,
            "confidence": 0.8  # Default confidence
        })
        
        # Extract topics from user input
        topics = self._extract_topics(user_input)
        self.sessions[session_id]["topics_discussed"].update(topics)
        
        # Keep only recent exchanges
        if len(self.sessions[session_id]["conversation_history"]) > self.max_session_length:
            self.sessions[session_id]["conversation_history"] = \
                self.sessions[session_id]["conversation_history"][-self.max_session_length:]
        
        print(f"💬 Added exchange to session {session_id}: {emotion} -> {len(topics)} topics")
    
    def get_session_context(self, session_id: str) -> Dict[str, Any]:
        """
        Get conversation context for a session.
        
        Args:
            session_id: Session identifier
            
        Returns:
            Session context information
        """
        if session_id not in self.sessions:
            return {"error": "Session not found"}
        
        session = self.sessions[session_id]
        
        # Get recent conversation history
        recent_history = session["conversation_history"][-5:]  # Last 5 exchanges
        
        # Get emotion trends
        emotion_trends = self._analyze_emotion_trends(session["emotion_history"])
        
        # Get session summary
        session_summary = self._generate_session_summary(session)
        
        return {
            "session_id": session_id,
            "conversation_count": len(session["conversation_history"]),
            "recent_history": recent_history,
            "emotion_trends": emotion_trends,
            "topics_discussed": list(session["topics_discussed"]),
            "session_summary": session_summary,
            "session_duration": self._calculate_session_duration(session)
        }
    
    def get_personalized_context(self, session_id: str) -> str:
        """
        Get personalized context for response generation.
        
        Args:
            session_id: Session identifier
            
        Returns:
            Personalized context string
        """
        if session_id not in self.sessions:
            return ""
        
        session = self.sessions[session_id]
        context_parts = []
        
        # Add recent emotion context
        if session["emotion_history"]:
            recent_emotions = [e["emotion"] for e in session["emotion_history"][-3:]]
            if recent_emotions:
                context_parts.append(f"Recent emotions: {', '.join(recent_emotions)}")
        
        # Add topics context
        if session["topics_discussed"]:
            topics = list(session["topics_discussed"])[:5]  # Top 5 topics
            context_parts.append(f"Topics discussed: {', '.join(topics)}")
        
        # Add conversation length context
        exchange_count = len(session["conversation_history"])
        if exchange_count > 0:
            context_parts.append(f"Session length: {exchange_count} exchanges")
        
        return " | ".join(context_parts) if context_parts else ""
    
    def _extract_topics(self, text: str) -> List[str]:
        """Extract topics from user input."""
        topics = []
        text_lower = text.lower()
        
        # Common therapeutic topics
        topic_keywords = {
            "anxiety": ["anxious", "worry", "nervous", "panic", "fear"],
            "depression": ["sad", "depressed", "down", "hopeless", "blue"],
            "stress": ["stressed", "overwhelmed", "pressure", "tension"],
            "relationships": ["relationship", "partner", "family", "friend", "social"],
            "work": ["work", "job", "career", "boss", "colleague"],
            "health": ["health", "sick", "pain", "medical", "doctor"],
            "sleep": ["sleep", "insomnia", "tired", "exhausted"],
            "self-esteem": ["confidence", "self-worth", "value", "worthless"],
            "trauma": ["trauma", "abuse", "ptsd", "flashback", "trigger"]
        }
        
        for topic, keywords in topic_keywords.items():
            if any(keyword in text_lower for keyword in keywords):
                topics.append(topic)
        
        return topics
    
    def _analyze_emotion_trends(self, emotion_history: List[Dict]) -> Dict[str, Any]:
        """Analyze emotion trends in the session."""
        if not emotion_history:
            return {"trend": "neutral", "stability": "unknown"}
        
        emotions = [e["emotion"] for e in emotion_history]
        
        # Calculate emotion distribution
        emotion_counts = {}
        for emotion in emotions:
            emotion_counts[emotion] = emotion_counts.get(emotion, 0) + 1
        
        # Determine trend
        if len(emotions) >= 3:
            recent_emotions = emotions[-3:]
            if len(set(recent_emotions)) == 1:
                trend = "stable"
            elif recent_emotions[-1] in ["happiness", "neutral"]:
                trend = "improving"
            else:
                trend = "fluctuating"
        else:
            trend = "developing"
        
        return {
            "trend": trend,
            "dominant_emotion": max(emotion_counts, key=emotion_counts.get),
            "emotion_distribution": emotion_counts,
            "stability": "stable" if len(set(emotions)) <= 2 else "variable"
        }
    
    def _generate_session_summary(self, session: Dict) -> str:
        """Generate a summary of the session."""
        if not session["conversation_history"]:
            return "New session started"
        
        exchange_count = len(session["conversation_history"])
        topics = list(session["topics_discussed"])
        
        summary_parts = [f"Session with {exchange_count} exchanges"]
        
        if topics:
            summary_parts.append(f"discussing {', '.join(topics[:3])}")
        
        if session["emotion_history"]:
            recent_emotion = session["emotion_history"][-1]["emotion"]
            summary_parts.append(f"current emotion: {recent_emotion}")
        
        return " | ".join(summary_parts)
    
    def _calculate_session_duration(self, session: Dict) -> str:
        """Calculate session duration."""
        if not session["conversation_history"]:
            return "0 minutes"
        
        start_time = datetime.fromisoformat(session["start_time"])
        end_time = datetime.fromisoformat(session["conversation_history"][-1]["timestamp"])
        duration = end_time - start_time
        
        minutes = int(duration.total_seconds() / 60)
        return f"{minutes} minutes"

# Global conversation memory instance
conversation_memory = ConversationMemory()
