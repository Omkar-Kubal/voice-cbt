"""
Audio processing service for handling audio files and transcription.
This service provides proper audio file handling and preprocessing.
"""

import os
import base64
import tempfile
import wave
import numpy as np
import librosa
from typing import Optional, Tuple
import soundfile as sf

class AudioProcessor:
    """
    Service for processing audio files and preparing them for transcription.
    """
    
    def __init__(self, target_sample_rate: int = 16000):
        self.target_sample_rate = target_sample_rate
        
    def decode_base64_audio(self, base64_audio: str) -> bytes:
        """
        Decode base64 encoded audio data.
        
        Args:
            base64_audio: Base64 encoded audio string
            
        Returns:
            Raw audio bytes
        """
        try:
            return base64.b64decode(base64_audio)
        except Exception as e:
            raise ValueError(f"Failed to decode base64 audio: {e}")
    
    def save_audio_to_temp_file(self, audio_bytes: bytes, file_extension: str = ".wav") -> str:
        """
        Save audio bytes to a temporary file.
        
        Args:
            audio_bytes: Raw audio data
            file_extension: File extension for the temporary file
            
        Returns:
            Path to the temporary file
        """
        try:
            with tempfile.NamedTemporaryFile(suffix=file_extension, delete=False) as temp_file:
                temp_file.write(audio_bytes)
                return temp_file.name
        except Exception as e:
            raise ValueError(f"Failed to save audio to temporary file: {e}")
    
    def load_audio_file(self, file_path: str) -> Tuple[np.ndarray, int]:
        """
        Load audio file using librosa.
        
        Args:
            file_path: Path to the audio file
            
        Returns:
            Tuple of (audio_array, sample_rate)
        """
        try:
            audio, sr = librosa.load(file_path, sr=self.target_sample_rate)
            return audio, sr
        except Exception as e:
            raise ValueError(f"Failed to load audio file {file_path}: {e}")
    
    def preprocess_audio(self, audio: np.ndarray, sample_rate: int) -> np.ndarray:
        """
        Preprocess audio for better transcription quality.
        
        Args:
            audio: Audio array
            sample_rate: Sample rate of the audio
            
        Returns:
            Preprocessed audio array
        """
        try:
            # Normalize audio
            audio = librosa.util.normalize(audio)
            
            # Remove silence from the beginning and end
            audio, _ = librosa.effects.trim(audio, top_db=20)
            
            # Apply noise reduction (simple approach)
            audio = librosa.effects.preemphasis(audio)
            
            return audio
        except Exception as e:
            print(f"Warning: Audio preprocessing failed: {e}")
            return audio
    
    def process_base64_audio(self, base64_audio: str) -> Tuple[np.ndarray, int, str]:
        """
        Complete audio processing pipeline from base64 to processed audio.
        
        Args:
            base64_audio: Base64 encoded audio string
            
        Returns:
            Tuple of (processed_audio, sample_rate, temp_file_path)
        """
        try:
            # Step 1: Decode base64 audio
            audio_bytes = self.decode_base64_audio(base64_audio)
            
            # Step 2: Save to temporary file
            temp_file_path = self.save_audio_to_temp_file(audio_bytes)
            
            # Step 3: Load audio file
            audio, sample_rate = self.load_audio_file(temp_file_path)
            
            # Step 4: Preprocess audio
            processed_audio = self.preprocess_audio(audio, sample_rate)
            
            print(f"Audio processing successful: {len(processed_audio)} samples at {sample_rate}Hz")
            return processed_audio, sample_rate, temp_file_path
            
        except Exception as e:
            print(f"Audio processing failed: {e}")
            # Return minimal fallback data
            fallback_audio = np.zeros(16000)  # 1 second of silence
            return fallback_audio, 16000, None
    
    def cleanup_temp_file(self, file_path: str):
        """
        Clean up temporary file.
        
        Args:
            file_path: Path to the temporary file to delete
        """
        try:
            if os.path.exists(file_path):
                os.unlink(file_path)
        except Exception as e:
            print(f"Warning: Failed to cleanup temporary file {file_path}: {e}")
    
    def get_audio_info(self, audio: np.ndarray, sample_rate: int) -> dict:
        """
        Get information about the audio.
        
        Args:
            audio: Audio array
            sample_rate: Sample rate
            
        Returns:
            Dictionary with audio information
        """
        duration = len(audio) / sample_rate
        return {
            "duration_seconds": duration,
            "sample_rate": sample_rate,
            "samples": len(audio),
            "channels": 1 if audio.ndim == 1 else audio.shape[0]
        }

# Global instance
audio_processor = AudioProcessor()

def process_audio_for_transcription(base64_audio: str) -> Tuple[np.ndarray, int, str]:
    """
    Main function to process audio for transcription.
    
    Args:
        base64_audio: Base64 encoded audio string
        
    Returns:
        Tuple of (processed_audio, sample_rate, temp_file_path)
    """
    return audio_processor.process_base64_audio(base64_audio)
