from fastapi import APIRouter, Depends, HTTPException
from typing import List, Dict, Any
from ..models.schemas import MoodEntry
from ..models.database import get_database
from ..services.database_service import DatabaseService

router = APIRouter()

@router.post("/mood/log")
async def log_mood(mood_data: Dict[str, Any], db = Depends(get_database)):
    """
    Log a mood entry for a user.
    """
    try:
        db_service = DatabaseService(db)
        
        # Extract required fields
        user_id = mood_data.get("user_id")
        emotion = mood_data.get("emotion")
        intensity = mood_data.get("intensity")
        
        if not all([user_id, emotion, intensity]):
            raise HTTPException(status_code=400, detail="Missing required fields: user_id, emotion, intensity")
        
        # Create or get user
        user = db_service.create_or_get_user(username=user_id)
        
        # Log mood entry
        result = db_service.log_mood_entry(
            user_id=str(user.id),
            emotion=emotion,
            intensity=intensity,
            context=mood_data.get("context"),
            triggers=mood_data.get("triggers"),
            source=mood_data.get("source", "api")
        )
        
        if result:
            return {"message": "Mood entry logged successfully", "mood_entry_id": result["mood_entry_id"]}
        else:
            raise HTTPException(status_code=500, detail="Failed to log mood entry")
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/mood/trends/{user_id}")
async def get_mood_trends(user_id: str, days: int = 30, db = Depends(get_database)):
    """
    Retrieves the historical mood trends for a specific user.
    """
    try:
        db_service = DatabaseService(db)
        
        # Create or get user
        user = db_service.create_or_get_user(username=user_id)
        
        # Get mood analytics
        analytics = db_service.get_mood_analytics(str(user.id), days)
        
        return analytics
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/mood/analytics/{user_id}")
async def get_mood_analytics(user_id: str, days: int = 30, db = Depends(get_database)):
    """
    Get comprehensive mood analytics for a user.
    """
    try:
        db_service = DatabaseService(db)
        
        # Create or get user
        user = db_service.create_or_get_user(username=user_id)
        
        # Get detailed analytics
        analytics = db_service.get_mood_analytics(str(user.id), days)
        
        return analytics
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/sessions/{user_id}")
async def get_user_sessions(user_id: str, limit: int = 50, db = Depends(get_database)):
    """
    Get user's therapy sessions.
    """
    try:
        db_service = DatabaseService(db)
        
        # Create or get user
        user = db_service.create_or_get_user(username=user_id)
        
        # Get user sessions
        sessions = db_service.ops.get_user_sessions(str(user.id), limit)
        
        return {
            "user_id": str(user.id),
            "sessions": [
                {
                    "session_id": str(session.id),
                    "started_at": session.started_at.isoformat(),
                    "ended_at": session.ended_at.isoformat() if session.ended_at else None,
                    "duration_minutes": session.duration_minutes,
                    "status": session.status
                }
                for session in sessions
            ]
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/sessions/{session_id}/summary")
async def get_session_summary(session_id: str, db = Depends(get_database)):
    """
    Get detailed summary of a therapy session.
    """
    try:
        db_service = DatabaseService(db)
        
        # Get session summary
        summary = db_service.get_session_summary(session_id)
        
        if not summary:
            raise HTTPException(status_code=404, detail="Session not found")
        
        return summary
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))