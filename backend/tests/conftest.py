"""
Pytest configuration and fixtures for the Voice CBT testing suite.
"""

import pytest
import asyncio
import tempfile
import os
import sys
from unittest.mock import Mock, patch
from fastapi.testclient import TestClient
import numpy as np
import base64

# Add the app directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'app'))

from app.main import app
from app.services.model_manager import ModelManager
from app.services.emotion_detector import EmotionDetector
from app.services.reply_generator import ReplyGenerator
from app.services.speech_to_text_config import transcribe_audio

@pytest.fixture(scope="session")
def event_loop():
    """Create an instance of the default event loop for the test session."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()

@pytest.fixture
def client():
    """Create a test client for the FastAPI application."""
    return TestClient(app)

@pytest.fixture
def sample_audio_data():
    """Generate sample audio data for testing."""
    # Create a simple sine wave as test audio
    duration = 2.0  # seconds
    sample_rate = 16000
    frequency = 440  # A4 note
    
    t = np.linspace(0, duration, int(sample_rate * duration), False)
    audio = np.sin(2 * np.pi * frequency * t)
    
    # Add some noise to make it more realistic
    noise = np.random.normal(0, 0.1, audio.shape)
    audio = audio + noise
    
    # Normalize
    audio = audio / np.max(np.abs(audio))
    
    # Convert to base64
    import soundfile as sf
    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp_file:
        sf.write(temp_file.name, audio, sample_rate)
        with open(temp_file.name, 'rb') as f:
            audio_bytes = f.read()
            audio_base64 = base64.b64encode(audio_bytes).decode('utf-8')
        os.unlink(temp_file.name)
    
    return audio_base64

@pytest.fixture
def mock_emotion_detector():
    """Mock emotion detector for testing."""
    detector = Mock(spec=EmotionDetector)
    detector.detect_emotion_from_base64.return_value = {
        "emotion": "neutral",
        "confidence": 0.85,
        "error": False
    }
    return detector

@pytest.fixture
def mock_reply_generator():
    """Mock reply generator for testing."""
    generator = Mock(spec=ReplyGenerator)
    generator.generate_reply.return_value = "I understand how you're feeling. Let's work through this together."
    return generator

@pytest.fixture
def mock_model_manager():
    """Mock model manager for testing."""
    manager = Mock(spec=ModelManager)
    manager.get_model_status.return_value = {
        "models_loaded": True,
        "available_services": {
            "emotion_detection": True,
            "speech_to_text": True,
            "reply_generation": True,
            "text_to_speech": True
        },
        "loading_status": {
            "emotion_model": True,
            "stt_model": True,
            "reply_model": True,
            "tts_model": True
        }
    }
    manager.is_system_ready.return_value = True
    return manager

@pytest.fixture
def test_audio_request():
    """Sample audio request for testing."""
    return {
        "audio_data": "base64_encoded_audio_data_here",
        "user_id": "test_user_123",
        "session_id": "test_session_456"
    }

@pytest.fixture
def test_mood_request():
    """Sample mood request for testing."""
    return {
        "user_id": "test_user_123",
        "mood_data": {
            "emotion": "anxious",
            "intensity": 7,
            "timestamp": "2024-01-01T12:00:00Z"
        }
    }
