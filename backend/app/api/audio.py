from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from datetime import datetime
from ..models.schemas import AudioRequest, TherapeuticResponse
from ..models.database import get_database
from ..services import tts
from ..services.emotion_detector import emotion_detector
from ..services.audio_processor import audio_processor
from ..services import speech_to_text_config
from ..services.reply_enhanced import generate_reply
from ..services.conversation_memory import conversation_memory
from ..services.enhanced_emotion_detector import enhanced_emotion_detector
from ..services.progress_tracker import progress_tracker
from ..services.interactive_features import interactive_features
from ..services.database_service import DatabaseService
from ..services.enhanced_response_generator import generate_enhanced_response
from ..services.enhanced_tts import synthesize_enhanced_speech
from ..services.simple_tts import simple_tts
from ..services.enhanced_audio_processor import process_enhanced_audio
from ..services.response_optimizer import ResponseOptimizer
from ..services.adaptive_response_system import AdaptiveResponseSystem
from ..services.emotional_intelligence_engine import EmotionalIntelligenceEngine

router = APIRouter()

# Initialize advanced services
response_optimizer = ResponseOptimizer()
adaptive_system = AdaptiveResponseSystem()
emotional_engine = EmotionalIntelligenceEngine()

@router.post("/process/enhanced")
async def process_enhanced_audio_input(
    audio_data: str,
    user_id: str = None,
    session_id: str = None,
    db = Depends(get_database)
):
    """
    Enhanced audio processing with advanced features.
    """
    try:
        # Process audio with enhanced features
        audio_result = process_enhanced_audio(audio_data, user_id, session_id)
        
        if not audio_result["success"]:
            raise HTTPException(status_code=400, detail=audio_result["error"])
        
        return {
            "success": True,
            "audio_analysis": audio_result["audio_analysis"],
            "quality_score": audio_result["quality_score"],
            "audio_features": audio_result["audio_features"],
            "processing_time": audio_result["processing_time"],
            "recommendations": audio_result.get("recommendations", [])
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/tts/enhanced")
async def generate_enhanced_voice(
    text: str,
    emotion: str = "neutral",
    voice_instructions: dict = None
):
    """
    Generate enhanced voice synthesis with emotion-aware parameters.
    """
    try:
        result = synthesize_enhanced_speech(
            text,
            emotion,
            voice_instructions=voice_instructions
        )
        
        if not result["success"]:
            raise HTTPException(status_code=400, detail=result.get("error", "TTS generation failed"))
        
        return {
            "success": True,
            "output_file": result.get("output_file"),
            "file_size": result.get("file_size"),
            "emotion": emotion,
            "voice_parameters": result.get("voice_parameters"),
            "duration_estimate": result.get("duration_estimate")
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

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

        # Step 4: Generate enhanced therapeutic response
        print("Generating enhanced therapeutic response...")
        
        # Generate or get session ID for conversation memory
        if not session_id:
            session_id = f"session_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            conversation_memory.start_session(session_id, str(user.id) if user else None)
        
        # Get conversation history for context
        conversation_history = conversation_memory.get_session_history(session_id)
        
        # Get user profile for personalization
        user_profile = None
        if user:
            user_profile = {
                "preferences": user.preferences or {},
                "therapy_style": user.preferences.get("therapy_style", "supportive") if user.preferences else "supportive"
            }
        
        # Generate enhanced response
        enhanced_response = generate_enhanced_response(
            transcribed_text,
            emotion_label,
            conversation_history,
            user_profile
        )
        
        response_text = enhanced_response["text"]
        voice_instructions = enhanced_response.get("voice_instructions", {})
        techniques_used = enhanced_response.get("techniques_used", [])
        
        print(f"Generated enhanced response: {response_text}")
        print(f"Techniques used: {techniques_used}")
        print(f"Voice instructions: {voice_instructions}")
        
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
        # Step 8: Generate enhanced voice response
        print("Generating enhanced voice response...")
        try:
            voice_result = synthesize_enhanced_speech(
                response_text,
                emotion_label,
                voice_instructions=voice_instructions
            )
            
            if voice_result["success"]:
                print(f"Enhanced voice generated successfully")
                print(f"Voice parameters: {voice_result.get('voice_parameters', {})}")
            else:
                print(f"Enhanced voice generation failed: {voice_result.get('error', 'Unknown error')}")
                # Try simple TTS as fallback
                print("Trying simple TTS fallback...")
                simple_result = simple_tts.speak(response_text)
                if simple_result["success"]:
                    print("Simple TTS fallback successful")
                else:
                    print(f"Simple TTS fallback failed: {simple_result.get('error', 'Unknown error')}")
        except Exception as e:
            print(f"Error generating enhanced voice: {e}")
            # Try simple TTS as fallback
            print("Trying simple TTS fallback...")
            simple_result = simple_tts.speak(response_text)
            if simple_result["success"]:
                print("Simple TTS fallback successful")
            else:
                print(f"Simple TTS fallback failed: {simple_result.get('error', 'Unknown error')}")

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

# Advanced Response Optimization Endpoints

@router.post("/response/optimize")
async def optimize_response(request: dict):
    """
    Optimize AI response for maximum therapeutic impact.
    """
    try:
        base_response = request.get("response", "")
        user_emotion = request.get("emotion", "neutral")
        session_context = request.get("session_context", {})
        user_profile = request.get("user_profile", {})
        
        optimization_result = response_optimizer.optimize_response(
            base_response, user_emotion, session_context, user_profile
        )
        
        return {
            "optimized_response": optimization_result["optimized_response"],
            "therapeutic_technique": optimization_result["therapeutic_technique"],
            "follow_up_questions": optimization_result["follow_up_questions"],
            "alternative_responses": optimization_result["alternative_responses"],
            "optimization_score": optimization_result["optimization_score"],
            "therapeutic_value": optimization_result["therapeutic_value"],
            "empathy_level": optimization_result["empathy_level"]
        }
    except Exception as e:
        return {"error": f"Failed to optimize response: {str(e)}"}

@router.post("/response/adapt")
async def adapt_response(request: dict):
    """
    Adapt response based on real-time user engagement and feedback.
    """
    try:
        base_response = request.get("response", "")
        user_id = request.get("user_id", "anonymous")
        current_emotion = request.get("emotion", "neutral")
        session_context = request.get("session_context", {})
        real_time_metrics = request.get("real_time_metrics", {})
        
        adaptation_result = adaptive_system.adapt_response(
            base_response, user_id, current_emotion, session_context, real_time_metrics
        )
        
        return {
            "adapted_response": adaptation_result["adapted_response"],
            "adaptation_strategy": adaptation_result["adaptation_strategy"],
            "adaptive_follow_ups": adaptation_result["adaptive_follow_ups"],
            "engagement_level": adaptation_result["engagement_level"],
            "adaptation_score": adaptation_result["adaptation_score"],
            "predicted_effectiveness": adaptation_result["predicted_effectiveness"]
        }
    except Exception as e:
        return {"error": f"Failed to adapt response: {str(e)}"}

@router.post("/emotion/analyze")
async def analyze_emotional_state(request: dict):
    """
    Comprehensive emotional state analysis using advanced AI.
    """
    try:
        text_input = request.get("text", "")
        audio_features = request.get("audio_features")
        user_history = request.get("user_history")
        
        emotional_analysis = emotional_engine.analyze_emotional_state(
            text_input, audio_features, user_history
        )
        
        return {
            "primary_emotion": emotional_analysis["primary_emotion"],
            "emotion_confidence": emotional_analysis["emotion_confidence"],
            "emotional_intensity": emotional_analysis["emotional_intensity"],
            "emotional_patterns": emotional_analysis["emotional_patterns"],
            "potential_triggers": emotional_analysis["potential_triggers"],
            "insights": emotional_analysis["insights"],
            "recommended_interventions": emotional_analysis["recommended_interventions"],
            "emotional_safety": emotional_analysis["emotional_safety"],
            "therapeutic_approach": emotional_analysis["therapeutic_approach"]
        }
    except Exception as e:
        return {"error": f"Failed to analyze emotional state: {str(e)}"}

@router.post("/tts/simple")
async def simple_text_to_speech(request: dict):
    """
    Simple text-to-speech endpoint for testing.
    """
    try:
        text = request.get("text", "Hello, this is a test.")
        result = simple_tts.speak(text)
        return result
    except Exception as e:
        return {"success": False, "error": str(e)}

@router.post("/process")
async def process_audio_for_speech_to_text(
    request: dict,
    db = Depends(get_database)
):
    """
    Process audio for speech-to-text conversion.
    """
    try:
        audio_data = request.get("audio_data", "")
        if not audio_data:
            return {
                "success": False,
                "error": "No audio data provided",
                "transcript": None
            }
        
        # For now, we'll use a simple approach
        # In a real implementation, you'd use a speech-to-text service
        # like Google Cloud Speech-to-Text, Azure Speech, or OpenAI Whisper
        
        # This is a placeholder that simulates speech-to-text
        # You can replace this with actual speech-to-text processing
        import time
        time.sleep(1)  # Simulate processing time
        
        # For demonstration, we'll return a mock transcript
        # In production, you'd process the actual audio data
        mock_transcripts = [
            "Hello, how are you today?",
            "I'm feeling a bit anxious about work",
            "Can you help me with my stress?",
            "I need someone to talk to",
            "What should I do about my relationship?"
        ]
        
        import random
        transcript = random.choice(mock_transcripts)
        
        return {
            "success": True,
            "transcript": transcript,
            "confidence": 0.85,
            "processing_time": 1.0
        }
        
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "transcript": None
        }

@router.post("/response/advanced")
async def generate_advanced_response(request: dict):
    """
    Generate the most advanced therapeutic response using all optimization techniques.
    """
    try:
        user_input = request.get("user_input", "")
        user_id = request.get("user_id", "anonymous")
        session_context = request.get("session_context", {})
        user_profile = request.get("user_profile", {})
        audio_features = request.get("audio_features")
        
        # Step 1: Analyze emotional state
        emotional_analysis = emotional_engine.analyze_emotional_state(
            user_input, audio_features, user_profile.get("history")
        )
        
        # Step 2: Generate base enhanced response
        base_response = generate_enhanced_response(
            user_input, user_profile, session_context, emotional_analysis
        )
        
        # Step 3: Optimize the response
        optimization_result = response_optimizer.optimize_response(
            base_response, 
            emotional_analysis["primary_emotion"], 
            session_context, 
            user_profile
        )
        
        # Step 4: Adapt based on real-time metrics
        real_time_metrics = {
            "response_time": request.get("response_time", 0),
            "emotion_intensity": emotional_analysis["emotional_intensity"],
            "conversation_flow": request.get("conversation_flow", "normal"),
            "comfort_level": request.get("comfort_level", 0.5)
        }
        
        adaptation_result = adaptive_system.adapt_response(
            optimization_result["optimized_response"],
            user_id,
            emotional_analysis["primary_emotion"],
            session_context,
            real_time_metrics
        )
        
        # Step 5: Generate enhanced TTS
        enhanced_audio = synthesize_enhanced_speech(
            adaptation_result["adapted_response"],
            emotional_analysis["primary_emotion"],
            emotional_analysis["emotional_intensity"]
        )
        
        return {
            "final_response": adaptation_result["adapted_response"],
            "enhanced_audio": enhanced_audio,
            "emotional_analysis": emotional_analysis,
            "optimization_details": optimization_result,
            "adaptation_details": adaptation_result,
            "therapeutic_technique": optimization_result["therapeutic_technique"],
            "follow_up_questions": adaptation_result["adaptive_follow_ups"],
            "recommended_interventions": emotional_analysis["recommended_interventions"],
            "response_quality_score": (
                optimization_result["optimization_score"] + 
                adaptation_result["adaptation_score"]
            ) / 2
        }
    except Exception as e:
        return {"error": f"Failed to generate advanced response: {str(e)}"}