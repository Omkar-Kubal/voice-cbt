"""
Simplified data ingestion service for development.
This version doesn't require ClickHouse and uses in-memory storage.
"""

from typing import List, Dict, Any
import json
from datetime import datetime

# In-memory storage for development
_memory_storage = []

def get_clickhouse_client():
    """
    Placeholder for ClickHouse client.
    In production, this would establish a real ClickHouse connection.
    """
    print("Using in-memory storage for development.")
    return True

def ingest_session_data(user_id: str, emotion_label: str, audio_features: list, timestamp: str):
    """
    Simplified data ingestion that stores data in memory.
    In production, this would store data in ClickHouse.
    
    Args:
        user_id: The ID of the user
        emotion_label: The emotion detected during the session
        audio_features: A list of extracted audio features
        timestamp: The timestamp of the session
    """
    session_data = {
        "user_id": user_id,
        "emotion_label": emotion_label,
        "audio_features": audio_features,
        "timestamp": timestamp
    }
    
    _memory_storage.append(session_data)
    print(f"Session data stored in memory: {session_data}")

def get_mood_trends(user_id: str) -> List[Dict[str, Any]]:
    """
    Simplified mood trends retrieval from memory.
    In production, this would query ClickHouse.
    
    Args:
        user_id: The user ID to query
    
    Returns:
        A list of mood entries for the user
    """
    user_sessions = [session for session in _memory_storage if session["user_id"] == user_id]
    
    mood_entries = []
    for session in user_sessions:
        mood_entries.append({
            "emotion_label": session["emotion_label"],
            "timestamp": session["timestamp"]
        })
    
    return mood_entries

