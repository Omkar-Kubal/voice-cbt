import os
import base64
import tempfile
import librosa
import numpy as np
from typing import Optional
import whisper
import torch

class SpeechToTextService:
    """
    Service for converting speech to text using Whisper model.
    """
    
    def __init__(self):
        self.model = None
        self.model_name = "base"  # Options: tiny, base, small, medium, large
        
    def load_model(self):
        """
        Load the Whisper model for speech recognition.
        """
        if self.model is None:
            try:
                print("Loading Whisper model...")
                self.model = whisper.load_model(self.model_name)
                print(f"Whisper model '{self.model_name}' loaded successfully.")
            except Exception as e:
                print(f"Error loading Whisper model: {e}")
                self.model = None
                
    def transcribe_audio_file(self, audio_path: str) -> str:
        """
        Transcribe audio file to text using Whisper.
        
        Args:
            audio_path: Path to the audio file
            
        Returns:
            Transcribed text
        """
        if self.model is None:
            self.load_model()
            
        if self.model is None:
            return "Error: Could not load speech recognition model"
            
        try:
            # Load and transcribe audio
            result = self.model.transcribe(audio_path)
            return result["text"].strip()
        except Exception as e:
            print(f"Error transcribing audio: {e}")
            return "Error: Could not transcribe audio"
    
    def transcribe_base64_audio(self, base64_audio: str, sample_rate: int = 16000) -> str:
        """
        Transcribe base64 encoded audio to text.
        
        Args:
            base64_audio: Base64 encoded audio data
            sample_rate: Audio sample rate
            
        Returns:
            Transcribed text
        """
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
    
    def transcribe_audio_array(self, audio_array: np.ndarray, sample_rate: int = 16000) -> str:
        """
        Transcribe audio array to text.
        
        Args:
            audio_array: Audio data as numpy array
            sample_rate: Audio sample rate
            
        Returns:
            Transcribed text
        """
        try:
            # Create temporary file
            with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp_file:
                # Save audio array to temporary file
                import soundfile as sf
                sf.write(temp_file.name, audio_array, sample_rate)
                temp_path = temp_file.name
            
            # Transcribe the audio
            transcription = self.transcribe_audio_file(temp_path)
            
            # Clean up temporary file
            os.unlink(temp_path)
            
            return transcription
            
        except Exception as e:
            print(f"Error processing audio array: {e}")
            return "Error: Could not process audio data"

# Global instance
speech_to_text_service = SpeechToTextService()

def transcribe_audio(audio_data: str) -> str:
    """
    Main function to transcribe audio data.
    
    Args:
        audio_data: Base64 encoded audio string
        
    Returns:
        Transcribed text
    """
    return speech_to_text_service.transcribe_base64_audio(audio_data)
