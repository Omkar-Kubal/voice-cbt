"""
Configuration for speech-to-text services.
Choose between different STT implementations based on your needs.
"""

import os
from typing import Optional

# Configuration options
STT_SERVICE = os.getenv("STT_SERVICE", "simple")  # Options: "whisper", "simple", "azure", "google"

def get_speech_to_text_service():
    """
    Get the configured speech-to-text service.
    
    Returns:
        The appropriate STT service based on configuration
    """
    if STT_SERVICE == "whisper":
        try:
            from .speech_to_text import speech_to_text_service
            return speech_to_text_service
        except ImportError:
            print("Whisper not available, falling back to simple STT")
            from .speech_to_text_simple import simple_speech_to_text_service
            return simple_speech_to_text_service
    
    elif STT_SERVICE == "simple":
        try:
            from .speech_to_text_simple import simple_speech_to_text_service
            # Check if speech recognition is actually available
            if not hasattr(simple_speech_to_text_service, 'recognizer') or simple_speech_to_text_service.recognizer is None:
                print("Simple STT not available (pyaudio missing), falling back to Whisper")
                try:
                    from .speech_to_text import speech_to_text_service
                    return speech_to_text_service
                except ImportError:
                    print("Neither simple STT nor Whisper available. Using fallback.")
                    return None
            return simple_speech_to_text_service
        except ImportError:
            print("Simple STT not available, trying Whisper")
            try:
                from .speech_to_text import speech_to_text_service
                return speech_to_text_service
            except ImportError:
                print("No STT services available")
                return None
    
    elif STT_SERVICE == "azure":
        # Future implementation for Azure Speech Services
        print("Azure Speech Services not implemented yet, using simple STT")
        from .speech_to_text_simple import simple_speech_to_text_service
        return simple_speech_to_text_service
    
    elif STT_SERVICE == "google":
        # Future implementation for Google Cloud Speech-to-Text
        print("Google Cloud Speech-to-Text not implemented yet, using simple STT")
        from .speech_to_text_simple import simple_speech_to_text_service
        return simple_speech_to_text_service
    
    else:
        # Default to simple STT
        from .speech_to_text_simple import simple_speech_to_text_service
        return simple_speech_to_text_service

def transcribe_audio(audio_data: str) -> str:
    """
    Main function to transcribe audio using the configured service.
    
    Args:
        audio_data: Base64 encoded audio string
        
    Returns:
        Transcribed text
    """
    service = get_speech_to_text_service()
    
    if service is None:
        return "Error: No speech-to-text service available. Please install required dependencies."
    
    try:
        if hasattr(service, 'transcribe_base64_audio'):
            return service.transcribe_base64_audio(audio_data)
        else:
            # Fallback for different service interfaces
            return service.transcribe_audio(audio_data)
    except Exception as e:
        return f"Error: Speech-to-text failed - {e}"
