"""
Enhanced Text-to-Speech service with advanced voice synthesis.
Supports multiple TTS engines with emotion-aware voice generation.
"""

import pyttsx3
import os
import tempfile
import logging
from typing import Dict, Any, Optional, List, Tuple
import json
import time
from pathlib import Path

logger = logging.getLogger(__name__)

class EnhancedTTSService:
    """
    Advanced TTS service with emotion-aware voice synthesis.
    """
    
    def __init__(self):
        self.engine = None
        self.voices = {}
        self.current_voice = None
        self.voice_parameters = {
            "rate": 180,  # Words per minute
            "volume": 0.9,  # Volume level (0.0 to 1.0)
            "pitch": 1.0   # Pitch level (0.5 to 2.0)
        }
        
        # Initialize TTS engine
        self._initialize_engine()
        
        # Emotion-specific voice configurations
        self.emotion_voice_configs = {
            "sad": {
                "rate": 150,
                "volume": 0.8,
                "pitch": 0.9,
                "emphasis": "gentle, slow"
            },
            "angry": {
                "rate": 160,
                "volume": 0.7,
                "pitch": 0.8,
                "emphasis": "calm, steady"
            },
            "anxious": {
                "rate": 170,
                "volume": 0.85,
                "pitch": 1.0,
                "emphasis": "reassuring, clear"
            },
            "happy": {
                "rate": 200,
                "volume": 0.95,
                "pitch": 1.1,
                "emphasis": "warm, energetic"
            },
            "neutral": {
                "rate": 180,
                "volume": 0.9,
                "pitch": 1.0,
                "emphasis": "professional, warm"
            }
        }
    
    def _initialize_engine(self):
        """Initialize the TTS engine."""
        try:
            self.engine = pyttsx3.init()
            
            # Get available voices
            voices = self.engine.getProperty('voices')
            for voice in voices:
                voice_id = voice.id
                voice_name = voice.name
                voice_gender = getattr(voice, 'gender', 'unknown')
                
                self.voices[voice_id] = {
                    'name': voice_name,
                    'gender': voice_gender,
                    'id': voice_id
                }
            
            # Set default voice (prefer female voices for therapy)
            self._set_preferred_voice()
            
            logger.info(f"TTS engine initialized with {len(self.voices)} voices")
            
        except Exception as e:
            logger.warning(f"TTS engine initialization failed: {e}")
            logger.warning("TTS functionality will be disabled. Audio responses will not be available.")
            self.engine = None
    
    def _set_preferred_voice(self):
        """Set the preferred voice for therapy sessions."""
        # Prefer female voices for therapy
        female_voices = [
            voice_id for voice_id, voice_info in self.voices.items()
            if any(keyword in voice_info['name'].lower() for keyword in 
                   ['female', 'woman', 'samantha', 'karen', 'susan', 'zira'])
        ]
        
        if female_voices:
            self.current_voice = female_voices[0]
            self.engine.setProperty('voice', self.current_voice)
            logger.info(f"Set preferred voice: {self.voices[self.current_voice]['name']}")
        else:
            # Fallback to first available voice
            if self.voices:
                self.current_voice = list(self.voices.keys())[0]
                self.engine.setProperty('voice', self.current_voice)
                logger.info(f"Set fallback voice: {self.voices[self.current_voice]['name']}")
    
    def synthesize_with_emotion(
        self,
        text: str,
        emotion: str = "neutral",
        output_file: Optional[str] = None,
        voice_instructions: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Synthesize speech with emotion-aware voice parameters.
        """
        if self.engine is None:
            logger.warning("TTS engine not available. Returning text-only response.")
            return {
                "success": False,
                "error": "TTS engine not available",
                "text": text,
                "emotion": emotion
            }
        
        try:
            # Get emotion-specific configuration
            emotion_config = self.emotion_voice_configs.get(emotion, self.emotion_voice_configs["neutral"])
            
            # Apply voice instructions if provided
            if voice_instructions:
                emotion_config.update(voice_instructions)
            
            # Set voice parameters
            self._apply_voice_parameters(emotion_config)
            
            # Process text for better speech
            processed_text = self._process_text_for_speech(text, emotion)
            
            # Generate speech
            if output_file:
                self._synthesize_to_file(processed_text, output_file)
            else:
                # Generate to temporary file
                with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp_file:
                    output_file = temp_file.name
                    self._synthesize_to_file(processed_text, output_file)
            
            # Get file info
            file_size = os.path.getsize(output_file) if os.path.exists(output_file) else 0
            
            return {
                "success": True,
                "output_file": output_file,
                "file_size": file_size,
                "emotion": emotion,
                "voice_parameters": emotion_config,
                "processed_text": processed_text,
                "duration_estimate": self._estimate_duration(processed_text, emotion_config["rate"])
            }
            
        except Exception as e:
            logger.error(f"Error synthesizing speech: {e}")
            return {
                "success": False,
                "error": str(e),
                "emotion": emotion
            }
    
    def _apply_voice_parameters(self, parameters: Dict[str, Any]):
        """Apply voice parameters to the TTS engine."""
        if self.engine is None:
            return
            
        try:
            # Set rate (words per minute)
            if 'rate' in parameters:
                self.engine.setProperty('rate', parameters['rate'])
            
            # Set volume
            if 'volume' in parameters:
                self.engine.setProperty('volume', parameters['volume'])
            
            # Set pitch (if supported)
            if 'pitch' in parameters:
                # Note: pyttsx3 doesn't directly support pitch, but we can simulate with rate
                base_rate = parameters.get('rate', 180)
                pitch_factor = parameters['pitch']
                adjusted_rate = int(base_rate * pitch_factor)
                self.engine.setProperty('rate', adjusted_rate)
            
        except Exception as e:
            logger.error(f"Error applying voice parameters: {e}")
    
    def _process_text_for_speech(self, text: str, emotion: str) -> str:
        """Process text to improve speech synthesis."""
        processed = text
        
        # Add emotion-appropriate pauses
        if emotion == "sad":
            processed = processed.replace('.', '... ')
            processed = processed.replace('!', '. ')
        elif emotion == "anxious":
            processed = processed.replace(',', ', ')
            processed = processed.replace('.', '. ')
        elif emotion == "happy":
            processed = processed.replace('!', '! ')
            processed = processed.replace('?', '? ')
        
        # Add emphasis markers for important words
        emphasis_words = [
            "important", "valid", "understand", "support", "care", "listen",
            "together", "progress", "strength", "courage", "hope"
        ]
        
        for word in emphasis_words:
            if word in processed.lower():
                # Add slight pause before emphasized words
                processed = processed.replace(word, f" {word}")
        
        return processed
    
    def _synthesize_to_file(self, text: str, output_file: str):
        """Synthesize speech to a file."""
        if self.engine is None:
            raise RuntimeError("TTS engine not available")
            
        try:
            # Create output directory if it doesn't exist
            os.makedirs(os.path.dirname(output_file), exist_ok=True)
            
            # Save current settings
            original_rate = self.engine.getProperty('rate')
            original_volume = self.engine.getProperty('volume')
            original_voice = self.engine.getProperty('voice')
            
            # Synthesize to file
            self.engine.save_to_file(text, output_file)
            self.engine.runAndWait()
            
            # Restore original settings
            self.engine.setProperty('rate', original_rate)
            self.engine.setProperty('volume', original_volume)
            self.engine.setProperty('voice', original_voice)
            
        except Exception as e:
            logger.error(f"Error synthesizing to file: {e}")
            raise
    
    def _estimate_duration(self, text: str, rate: int) -> float:
        """Estimate speech duration in seconds."""
        word_count = len(text.split())
        duration_minutes = word_count / rate
        return duration_minutes * 60  # Convert to seconds
    
    def get_available_voices(self) -> List[Dict[str, Any]]:
        """Get list of available voices."""
        return [
            {
                "id": voice_id,
                "name": voice_info["name"],
                "gender": voice_info["gender"],
                "current": voice_id == self.current_voice
            }
            for voice_id, voice_info in self.voices.items()
        ]
    
    def set_voice(self, voice_id: str) -> bool:
        """Set the current voice."""
        try:
            if voice_id in self.voices:
                self.engine.setProperty('voice', voice_id)
                self.current_voice = voice_id
                logger.info(f"Voice set to: {self.voices[voice_id]['name']}")
                return True
            else:
                logger.warning(f"Voice not found: {voice_id}")
                return False
        except Exception as e:
            logger.error(f"Error setting voice: {e}")
            return False
    
    def get_voice_parameters(self) -> Dict[str, Any]:
        """Get current voice parameters."""
        return {
            "rate": self.engine.getProperty('rate'),
            "volume": self.engine.getProperty('volume'),
            "voice": self.engine.getProperty('voice'),
            "current_voice": self.current_voice
        }
    
    def test_synthesis(self, text: str = "Hello, this is a test of the voice synthesis system.") -> Dict[str, Any]:
        """Test the TTS system."""
        try:
            with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp_file:
                output_file = temp_file.name
            
            result = self.synthesize_with_emotion(text, "neutral", output_file)
            
            # Clean up test file
            if os.path.exists(output_file):
                os.unlink(output_file)
            
            return {
                "success": True,
                "test_result": result,
                "voices_available": len(self.voices),
                "current_voice": self.current_voice
            }
            
        except Exception as e:
            logger.error(f"TTS test failed: {e}")
            return {
                "success": False,
                "error": str(e)
            }

# Global TTS service instance
enhanced_tts_service = EnhancedTTSService()

def synthesize_enhanced_speech(
    text: str,
    emotion: str = "neutral",
    output_file: Optional[str] = None,
    voice_instructions: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """Synthesize speech with enhanced emotion-aware voice generation."""
    return enhanced_tts_service.synthesize_with_emotion(
        text, emotion, output_file, voice_instructions
    )

def get_enhanced_voices() -> List[Dict[str, Any]]:
    """Get available enhanced voices."""
    return enhanced_tts_service.get_available_voices()

def test_enhanced_tts() -> Dict[str, Any]:
    """Test the enhanced TTS system."""
    return enhanced_tts_service.test_synthesis()
