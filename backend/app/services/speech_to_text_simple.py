import os
import base64
import tempfile
from typing import Optional

# Try to import speech_recognition, handle gracefully if not available
try:
    import speech_recognition as sr
    SPEECH_RECOGNITION_AVAILABLE = True
except ImportError:
    print("Warning: speech_recognition not available. Install with: pip install SpeechRecognition")
    SPEECH_RECOGNITION_AVAILABLE = False
    sr = None

class SimpleSpeechToTextService:
    """
    Simple speech-to-text service using Google Speech Recognition API.
    This is a lighter alternative to Whisper for basic transcription.
    """
    
    def __init__(self):
        if not SPEECH_RECOGNITION_AVAILABLE:
            self.recognizer = None
            self.microphone = None
            return
            
        try:
            self.recognizer = sr.Recognizer()
            self.microphone = sr.Microphone()
        except Exception as e:
            print(f"Warning: Could not initialize speech recognition: {e}")
            self.recognizer = None
            self.microphone = None
        
    def transcribe_audio_file(self, audio_path: str) -> str:
        """
        Transcribe audio file to text using Google Speech Recognition.
        
        Args:
            audio_path: Path to the audio file
            
        Returns:
            Transcribed text
        """
        if not SPEECH_RECOGNITION_AVAILABLE or self.recognizer is None:
            return "Error: Speech recognition not available. Install SpeechRecognition and pyaudio."
            
        try:
            with sr.AudioFile(audio_path) as source:
                # Adjust for ambient noise
                self.recognizer.adjust_for_ambient_noise(source)
                audio = self.recognizer.record(source)
                
            # Use Google Speech Recognition
            text = self.recognizer.recognize_google(audio)
            return text.strip()
            
        except sr.UnknownValueError:
            return "Error: Could not understand the audio"
        except sr.RequestError as e:
            return f"Error: Could not request results from speech recognition service; {e}"
        except Exception as e:
            return f"Error: {e}"
    
    def transcribe_base64_audio(self, base64_audio: str) -> str:
        """
        Transcribe base64 encoded audio to text.
        
        Args:
            base64_audio: Base64 encoded audio data
            
        Returns:
            Transcribed text
        """
        if not SPEECH_RECOGNITION_AVAILABLE or self.recognizer is None:
            return "Error: Speech recognition not available. Install SpeechRecognition and pyaudio."
            
        try:
            # Decode base64 audio
            audio_bytes = base64.b64decode(base64_audio)
            
            # Create temporary file
            with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp_file:
                temp_file.write(audio_bytes)
                temp_path = temp_file.name
            
            # Transcribe the audio
            transcription = self.transcribe_audio_file(temp_path)
            
            # Clean up temporary file
            os.unlink(temp_path)
            
            return transcription
            
        except Exception as e:
            print(f"Error processing base64 audio: {e}")
            return "Error: Could not process audio data"

# Global instance
simple_speech_to_text_service = SimpleSpeechToTextService()

def transcribe_audio_simple(audio_data: str) -> str:
    """
    Simple function to transcribe audio data using Google Speech Recognition.
    
    Args:
        audio_data: Base64 encoded audio string
        
    Returns:
        Transcribed text
    """
    return simple_speech_to_text_service.transcribe_base64_audio(audio_data)
