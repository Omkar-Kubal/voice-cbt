"""
Test suite for service components.
"""

import pytest
import numpy as np
from unittest.mock import Mock, patch, MagicMock
import tempfile
import os

class TestEmotionDetector:
    """Test cases for emotion detection service."""
    
    def test_emotion_detection_success(self, sample_audio_data):
        """Test successful emotion detection."""
        with patch('app.services.emotion_detector.EmotionDetector') as mock_detector_class:
            mock_detector = Mock()
            mock_detector.detect_emotion_from_base64.return_value = {
                "emotion": "happy",
                "confidence": 0.92,
                "error": False
            }
            mock_detector_class.return_value = mock_detector
            
            from app.services.emotion_detector import emotion_detector
            result = emotion_detector.detect_emotion_from_base64(sample_audio_data)
            
            assert result["emotion"] == "happy"
            assert result["confidence"] == 0.92
            assert not result["error"]
    
    def test_emotion_detection_fallback(self, sample_audio_data):
        """Test emotion detection fallback when model fails."""
        with patch('app.services.emotion_detector.EmotionDetector') as mock_detector_class:
            mock_detector = Mock()
            mock_detector.detect_emotion_from_base64.return_value = {
                "emotion": "neutral",
                "confidence": 0.5,
                "error": True,
                "fallback": True
            }
            mock_detector_class.return_value = mock_detector
            
            from app.services.emotion_detector import emotion_detector
            result = emotion_detector.detect_emotion_from_base64(sample_audio_data)
            
            assert result["fallback"] is True
            assert result["error"] is True

class TestReplyGenerator:
    """Test cases for reply generation service."""
    
    def test_reply_generation_success(self):
        """Test successful reply generation."""
        with patch('app.services.reply_generator.ReplyGenerator') as mock_generator_class:
            mock_generator = Mock()
            mock_generator.generate_reply.return_value = "I understand your feelings. Let's work through this together."
            mock_generator_class.return_value = mock_generator
            
            from app.services.reply_generator import reply_generator
            result = reply_generator.generate_reply("I'm feeling anxious", "fear")
            
            assert isinstance(result, str)
            assert len(result) > 0
    
    def test_reply_generation_with_emotion(self):
        """Test reply generation with specific emotion context."""
        with patch('app.services.reply_generator.ReplyGenerator') as mock_generator_class:
            mock_generator = Mock()
            mock_generator.generate_reply.return_value = "It sounds like you're experiencing some anxiety. That's completely normal."
            mock_generator_class.return_value = mock_generator
            
            from app.services.reply_generator import reply_generator
            result = reply_generator.generate_reply("I'm worried about my job", "anxiety")
            
            assert "anxiety" in result.lower() or "worry" in result.lower()

class TestSpeechToText:
    """Test cases for speech-to-text service."""
    
    def test_speech_to_text_success(self, sample_audio_data):
        """Test successful speech-to-text conversion."""
        with patch('app.services.speech_to_text_config.transcribe_audio') as mock_stt:
            mock_stt.return_value = "Hello, I'm feeling anxious today"
            
            from app.services.speech_to_text_config import transcribe_audio
            result = transcribe_audio(sample_audio_data)
            
            assert result == "Hello, I'm feeling anxious today"
    
    def test_speech_to_text_error_handling(self, sample_audio_data):
        """Test speech-to-text error handling."""
        with patch('app.services.speech_to_text_config.transcribe_audio') as mock_stt:
            mock_stt.return_value = "Error: Could not process audio"
            
            from app.services.speech_to_text_config import transcribe_audio
            result = transcribe_audio(sample_audio_data)
            
            assert result.startswith("Error:")
    
    def test_speech_to_text_empty_result(self, sample_audio_data):
        """Test speech-to-text with empty result."""
        with patch('app.services.speech_to_text_config.transcribe_audio') as mock_stt:
            mock_stt.return_value = ""
            
            from app.services.speech_to_text_config import transcribe_audio
            result = transcribe_audio(sample_audio_data)
            
            assert result == ""

class TestModelManager:
    """Test cases for model management service."""
    
    def test_model_initialization(self, mock_model_manager):
        """Test model initialization."""
        status = mock_model_manager.get_model_status()
        assert status["models_loaded"] is True
        assert "available_services" in status
    
    def test_system_ready_check(self, mock_model_manager):
        """Test system readiness check."""
        is_ready = mock_model_manager.is_system_ready()
        assert is_ready is True
    
    def test_model_loading_failure(self):
        """Test model loading failure handling."""
        with patch('app.services.model_manager.ModelManager') as mock_manager_class:
            mock_manager = Mock()
            mock_manager.get_model_status.return_value = {
                "models_loaded": False,
                "available_services": {
                    "emotion_detection": False,
                    "speech_to_text": False,
                    "reply_generation": False,
                    "text_to_speech": False
                }
            }
            mock_manager.is_system_ready.return_value = False
            mock_manager_class.return_value = mock_manager
            
            from app.services.model_manager import model_manager
            status = model_manager.get_model_status()
            
            assert status["models_loaded"] is False
            assert not model_manager.is_system_ready()

class TestAudioProcessor:
    """Test cases for audio processing service."""
    
    def test_audio_processing_success(self, sample_audio_data):
        """Test successful audio processing."""
        with patch('app.services.audio_processor.AudioProcessor') as mock_processor_class:
            mock_processor = Mock()
            mock_audio = np.random.random(32000)  # 2 seconds at 16kHz
            mock_processor.process_base64_audio.return_value = (mock_audio, 16000, "/tmp/test.wav")
            mock_processor_class.return_value = mock_processor
            
            from app.services.audio_processor import audio_processor
            audio, sample_rate, temp_path = audio_processor.process_base64_audio(sample_audio_data)
            
            assert len(audio) > 0
            assert sample_rate == 16000
            assert isinstance(temp_path, str)
    
    def test_audio_processing_error_handling(self, sample_audio_data):
        """Test audio processing error handling."""
        with patch('app.services.audio_processor.AudioProcessor') as mock_processor_class:
            mock_processor = Mock()
            mock_processor.process_base64_audio.side_effect = Exception("Audio processing failed")
            mock_processor_class.return_value = mock_processor
            
            from app.services.audio_processor import audio_processor
            with pytest.raises(Exception):
                audio_processor.process_base64_audio(sample_audio_data)
