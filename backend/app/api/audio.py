from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from datetime import datetime
from ..models.schemas import AudioRequest, TherapeuticResponse
from ..models.database import get_database
from ..services import (
    emotion_detector, 
    reply_generator, 
    tts, 
    speech_to_text_config,
    audio_processor
)
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

        # Step 4: Generate therapeutic response using RAG
        print("Generating therapeutic response...")
        response_text = reply_generator.generate_reply(transcribed_text, emotion_label)
        print(f"Generated response: {response_text}")

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