from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from datetime import datetime
from ..models.schemas import AudioRequest, TherapeuticResponse
from ..models.database import get_database
from ..services import (
    emotion_detector, 
    tts, 
    speech_to_text_config,
    audio_processor
)
from ..services.reply_enhanced import generate_reply
from ..services.conversation_memory import conversation_memory
from ..services.enhanced_emotion_detector import enhanced_emotion_detector
from ..services.progress_tracker import progress_tracker
from ..services.interactive_features import interactive_features
from ..services.database_service import DatabaseService

router = APIRouter()

@router.post("/session/start", response_model=TherapeuticResponse)
async def start_session(request: AudioRequest, db = Depends(get_database)):
    """
    Receives user's voice input, processes it, and returns a therapeutic response.
    """
    start_time = datetime.now()
    db_service = DatabaseService(db)
    
    try:
        # Create or get user
        user = db_service.create_or_get_user(
            username=request.user_id or "anonymous",
            email=None
        )
        
        # Start or get existing session
        session_data = db_service.start_therapy_session(str(user.id))
        session_id = session_data["session_id"] if session_data else None
        
        # Initialize variables
        processed_audio = None
        temp_file_path = None
        
        # Determine input type and process accordingly
        if request.audio_data:
            # Step 1: Process audio for transcription
            print("Processing audio...")
            try:
                processed_audio, sample_rate, temp_file_path = audio_processor.process_base64_audio(request.audio_data)
                print(f"Audio processed: {len(processed_audio)} samples at {sample_rate}Hz")
            except Exception as e:
                print(f"Audio processing failed: {e}")
                # Fallback to simple processing
                processed_audio = None
                temp_file_path = None

            # Step 2: Convert speech to text using configured STT service
            print("Transcribing audio...")
            transcribed_text = speech_to_text_config.transcribe_audio(request.audio_data)
            
            if not transcribed_text or transcribed_text.startswith("Error:"):
                # Fallback to a default message if transcription fails
                transcribed_text = "I'm having trouble understanding. Could you please repeat that?"
                print(f"Transcription failed or empty: {transcribed_text}")
            else:
                print(f"Transcribed text: {transcribed_text}")

            # Step 3: Detect emotion from the audio using the trained model
            print("Detecting emotion...")
            emotion_result = emotion_detector.detect_emotion_from_base64(request.audio_data)
            emotion_label = emotion_result["emotion"]
            emotion_confidence = emotion_result.get("confidence", 0.0)
            print(f"Detected emotion: {emotion_label} (confidence: {emotion_confidence:.2f})")
        else:
            # Handle text input directly
            print("Processing text input...")
            transcribed_text = request.text_data or "Hello"
            print(f"Text input: {transcribed_text}")
            
            # Enhanced emotion detection with confidence scoring
            print("Using enhanced emotion detection...")
            emotion_label, emotion_confidence, emotion_analysis = enhanced_emotion_detector.detect_emotion(
                transcribed_text, 
                context=conversation_memory.get_personalized_context(session_id) if session_id else ""
            )
            
            # Generate emotion insights
            insights = enhanced_emotion_detector.get_emotion_insights(emotion_label, emotion_confidence, emotion_analysis)
            print(f"Detected emotion: {emotion_label} (confidence: {emotion_confidence:.2f})")
            print(f"Emotion insights: {insights}")
            print(f"Analysis details: {emotion_analysis}")

        # Step 4: Generate therapeutic response using RAG and conversation memory
        print("Generating therapeutic response...")
        
        # Generate or get session ID for conversation memory
        if not session_id:
            session_id = f"session_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            conversation_memory.start_session(session_id, str(user.id) if user else None)
        
        response_text = generate_reply(transcribed_text, emotion_label, session_id)
        print(f"Generated response: {response_text}")
        
        # Add conversation exchange to memory
        conversation_memory.add_exchange(session_id, transcribed_text, emotion_label, response_text)
        
        # Track progress and mood
        user_id = str(user.id) if user else "anonymous"
        progress_tracker.track_mood(user_id, emotion_label, emotion_confidence, session_id, transcribed_text)

        # Step 5: Log interaction to database
        if session_id:
            interaction_data = {
                "transcribed_text": transcribed_text,
                "detected_emotion": emotion_label,
                "emotion_confidence": emotion_confidence,
                "therapeutic_response": response_text,
                "processing_time_ms": int((datetime.now() - start_time).total_seconds() * 1000),
                "model_version": "1.0"
            }
            db_service.log_interaction(session_id, str(user.id), **interaction_data)

        # Step 6: Clean up temporary files
        if temp_file_path:
            audio_processor.cleanup_temp_file(temp_file_path)

        # Step 7: Log system metrics
        processing_time = (datetime.now() - start_time).total_seconds() * 1000
        db_service.log_system_metrics(
            response_time_ms=int(processing_time),
            active_sessions=1,
            total_interactions=1
        )

        # Return the structured response
        return TherapeuticResponse(
            response_text=response_text,
            emotion=emotion_label,
            timestamp=datetime.now().isoformat(),
            session_id=session_id,
            transcribed_text=transcribed_text,
            confidence=emotion_confidence
        )
    except Exception as e:
        print(f"Error in start_session: {e}")
        # Log error to database
        if 'session_id' in locals() and session_id:
            db_service.log_interaction(session_id, str(user.id), 
                                     error_message=str(e),
                                     processing_time_ms=int((datetime.now() - start_time).total_seconds() * 1000))
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/transcribe", response_model=dict)
async def transcribe_audio(request: AudioRequest):
    """
    Transcribe audio to text without generating a response.
    Useful for testing speech-to-text functionality.
    """
    try:
        transcribed_text = speech_to_text_config.transcribe_audio(request.audio_data)
        
        return {
            "transcribed_text": transcribed_text,
            "success": not transcribed_text.startswith("Error:"),
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        print(f"Error in transcribe_audio: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/session/{session_id}/context")
async def get_session_context(session_id: str):
    """
    Get conversation context for a session.
    """
    try:
        context = conversation_memory.get_session_context(session_id)
        return {"session_context": context}
    except Exception as e:
        return {"error": f"Failed to get session context: {str(e)}"}

@router.get("/progress/{user_id}")
async def get_user_progress(user_id: str):
    """
    Get user progress and analytics.
    """
    try:
        progress = progress_tracker.get_user_progress(user_id)
        return {"user_progress": progress}
    except Exception as e:
        return {"error": f"Failed to get user progress: {str(e)}"}

@router.get("/progress/{user_id}/mood")
async def get_mood_analytics(user_id: str, days: int = 30):
    """
    Get mood analytics for a user.
    """
    try:
        analytics = progress_tracker.get_mood_analytics(user_id, days)
        return {"mood_analytics": analytics}
    except Exception as e:
        return {"error": f"Failed to get mood analytics: {str(e)}"}

@router.post("/session/{session_id}/complete")
async def complete_session(session_id: str, session_data: dict):
    """
    Mark a session as complete and track session analytics.
    """
    try:
        user_id = session_data.get("user_id", "anonymous")
        analytics = progress_tracker.track_session(user_id, session_id, session_data)
        return {"session_analytics": analytics}
    except Exception as e:
        return {"error": f"Failed to complete session: {str(e)}"}

# Interactive Features Endpoints
@router.get("/exercises/categories")
async def get_exercise_categories():
    """
    Get available exercise categories and exercises.
    """
    try:
        categories = interactive_features.get_exercise_categories()
        return {"exercise_categories": categories}
    except Exception as e:
        return {"error": f"Failed to get exercise categories: {str(e)}"}

@router.get("/exercises/{exercise_type}/{exercise_name}")
async def get_exercise_details(exercise_type: str, exercise_name: str):
    """
    Get detailed information about a specific exercise.
    """
    try:
        details = interactive_features.get_exercise_details(exercise_type, exercise_name)
        return {"exercise_details": details}
    except Exception as e:
        return {"error": f"Failed to get exercise details: {str(e)}"}

@router.post("/exercises/start")
async def start_exercise(request: dict):
    """
    Start an interactive exercise.
    """
    try:
        user_id = request.get("user_id", "anonymous")
        exercise_type = request.get("exercise_type")
        exercise_name = request.get("exercise_name")
        
        session = interactive_features.start_exercise(user_id, exercise_type, exercise_name)
        return {"exercise_session": session}
    except Exception as e:
        return {"error": f"Failed to start exercise: {str(e)}"}

@router.get("/exercises/{session_id}/next")
async def get_next_exercise_step(session_id: str):
    """
    Get the next step in an exercise.
    """
    try:
        step = interactive_features.get_next_step(session_id)
        return {"exercise_step": step}
    except Exception as e:
        return {"error": f"Failed to get next step: {str(e)}"}

@router.post("/exercises/{session_id}/complete-step")
async def complete_exercise_step(session_id: str):
    """
    Mark an exercise step as completed.
    """
    try:
        session = interactive_features.complete_step(session_id)
        return {"exercise_session": session}
    except Exception as e:
        return {"error": f"Failed to complete step: {str(e)}"}

@router.get("/exercises/recommendations")
async def get_exercise_recommendations(emotion: str, context: str = ""):
    """
    Get exercise recommendations based on emotion.
    """
    try:
        recommendations = interactive_features.get_exercise_recommendations(emotion, context)
        return {"recommendations": recommendations}
    except Exception as e:
        return {"error": f"Failed to get recommendations: {str(e)}"}

@router.post("/exercises/guided-session")
async def create_guided_session(request: dict):
    """
    Create a guided therapeutic session.
    """
    try:
        user_id = request.get("user_id", "anonymous")
        emotion = request.get("emotion", "neutral")
        duration_minutes = request.get("duration_minutes", 15)
        
        session = interactive_features.get_guided_session(user_id, emotion, duration_minutes)
        return {"guided_session": session}
    except Exception as e:
        return {"error": f"Failed to create guided session: {str(e)}"}