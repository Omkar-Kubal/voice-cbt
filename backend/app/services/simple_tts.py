"""
Simple and reliable Text-to-Speech service.
Fallback TTS service that works across different environments.
"""

import pyttsx3
import logging
from typing import Dict, Any, Optional

logger = logging.getLogger(__name__)

class SimpleTTSService:
    """
    Simple TTS service with basic voice synthesis.
    """
    
    def __init__(self):
        self.engine = None
        self.available = False
        self._initialize_engine()
    
    def _initialize_engine(self):
        """Initialize the TTS engine with fallback options."""
        try:
            self.engine = pyttsx3.init()
            
            # Get available voices
            voices = self.engine.getProperty('voices')
            logger.info(f"Found {len(voices) if voices else 0} voices")
            
            if voices:
                # Try to find a female voice
                female_voice = None
                for voice in voices:
                    voice_name = voice.name.lower()
                    if any(keyword in voice_name for keyword in 
                           ['female', 'woman', 'samantha', 'karen', 'susan', 'zira', 'hazel']):
                        female_voice = voice
                        break
                
                # Set voice
                if female_voice:
                    self.engine.setProperty('voice', female_voice.id)
                    logger.info(f"Using female voice: {female_voice.name}")
                else:
                    # Use first available voice
                    self.engine.setProperty('voice', voices[0].id)
                    logger.info(f"Using voice: {voices[0].name}")
            
            # Set default properties
            self.engine.setProperty('rate', 180)  # Speed
            self.engine.setProperty('volume', 0.9)  # Volume
            
            self.available = True
            logger.info("Simple TTS engine initialized successfully")
            
        except Exception as e:
            logger.warning(f"TTS engine initialization failed: {e}")
            self.engine = None
            self.available = False
    
    def speak(self, text: str, rate: int = 180, volume: float = 0.9) -> Dict[str, Any]:
        """
        Speak the given text.
        """
        if not self.available or not self.engine:
            return {
                "success": False,
                "error": "TTS engine not available",
                "text": text
            }
        
        try:
            # Set properties
            self.engine.setProperty('rate', rate)
            self.engine.setProperty('volume', volume)
            
            # Speak the text
            self.engine.say(text)
            self.engine.runAndWait()
            
            return {
                "success": True,
                "text": text,
                "rate": rate,
                "volume": volume
            }
            
        except Exception as e:
            logger.error(f"TTS speak error: {e}")
            return {
                "success": False,
                "error": str(e),
                "text": text
            }
    
    def synthesize_to_file(self, text: str, filename: str, rate: int = 180, volume: float = 0.9) -> Dict[str, Any]:
        """
        Synthesize speech to a file.
        """
        if not self.available or not self.engine:
            return {
                "success": False,
                "error": "TTS engine not available",
                "text": text
            }
        
        try:
            # Set properties
            self.engine.setProperty('rate', rate)
            self.engine.setProperty('volume', volume)
            
            # Save to file
            self.engine.save_to_file(text, filename)
            self.engine.runAndWait()
            
            return {
                "success": True,
                "filename": filename,
                "text": text,
                "rate": rate,
                "volume": volume
            }
            
        except Exception as e:
            logger.error(f"TTS file synthesis error: {e}")
            return {
                "success": False,
                "error": str(e),
                "text": text
            }

# Global instance
simple_tts = SimpleTTSService()
