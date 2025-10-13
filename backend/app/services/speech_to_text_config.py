"""
Speech-to-Text configuration and service management.
Provides a unified interface for different STT services.
"""

import os
import logging
from typing import Optional, Dict, Any
from dotenv import load_dotenv

# Load environment variables
load_dotenv('config.env')

logger = logging.getLogger(__name__)

class SpeechToTextService:
    """
    Unified speech-to-text service interface.
    """
    
    def __init__(self):
        self.service_type = os.getenv("STT_SERVICE", "simple")
        self.whisper_model = os.getenv("WHISPER_MODEL", "base")
        self.is_initialized = False
        
    def initialize(self) -> bool:
        """Initialize the STT service."""
        try:
            if self.service_type == "simple":
                logger.info("Using simple STT service")
                self.is_initialized = True
            elif self.service_type == "whisper":
                logger.info(f"Using Whisper STT service with model: {self.whisper_model}")
                self.is_initialized = True
            else:
                logger.warning(f"Unknown STT service: {self.service_type}")
                return False
            return True
        except Exception as e:
            logger.error(f"Failed to initialize STT service: {e}")
            return False
    
    def transcribe(self, audio_data: bytes) -> Dict[str, Any]:
        """
        Transcribe audio data to text.
        
        Args:
            audio_data: Raw audio bytes
            
        Returns:
            Dict with transcription result
        """
        if not self.is_initialized:
            return {"text": "", "error": "STT service not initialized"}
        
        try:
            if self.service_type == "simple":
                # Simple mock transcription for testing
                return {
                    "text": "Hello, this is a test transcription",
                    "confidence": 0.85,
                    "error": False
                }
            elif self.service_type == "whisper":
                # Real Whisper implementation
                try:
                    import whisper
                    model = whisper.load_model(self.whisper_model)
                    result = model.transcribe(audio_data)
                    return {
                        "text": result["text"],
                        "confidence": 0.90,
                        "error": False
                    }
                except ImportError:
                    return {
                        "text": "",
                        "error": "Whisper not installed. Run: pip install openai-whisper"
                    }
                except Exception as e:
                    return {
                        "text": "",
                        "error": f"Whisper transcription failed: {str(e)}"
                    }
            else:
                return {
                    "text": "",
                    "error": f"Unsupported STT service: {self.service_type}"
                }
        except Exception as e:
            logger.error(f"Transcription error: {e}")
            return {
                "text": "",
                "error": str(e)
            }

# Global STT service instance
_stt_service = None

def get_speech_to_text_service() -> Optional[SpeechToTextService]:
    """Get the global STT service instance."""
    global _stt_service
    if _stt_service is None:
        _stt_service = SpeechToTextService()
        _stt_service.initialize()
    return _stt_service

def transcribe_audio(audio_data: bytes) -> Dict[str, Any]:
    """
    Convenience function to transcribe audio.
    
    Args:
        audio_data: Raw audio bytes
        
    Returns:
        Dict with transcription result
    """
    service = get_speech_to_text_service()
    if service:
        return service.transcribe(audio_data)
    else:
        return {"text": "", "error": "STT service not available"}
