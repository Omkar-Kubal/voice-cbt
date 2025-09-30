"""
Test suite for API endpoints.
"""

import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, Mock
import json

class TestAudioEndpoints:
    """Test cases for audio-related API endpoints."""
    
    def test_start_session_success(self, client, sample_audio_data, mock_emotion_detector, mock_reply_generator):
        """Test successful session start with valid audio data."""
        with patch('app.services.emotion_detector.emotion_detector', mock_emotion_detector), \
             patch('app.services.reply_generator.reply_generator', mock_reply_generator), \
             patch('app.services.speech_to_text_config.transcribe_audio') as mock_stt:
            
            mock_stt.return_value = "I'm feeling anxious about my presentation tomorrow"
            
            response = client.post("/api/v1/session/start", json={
                "audio_data": sample_audio_data,
                "user_id": "test_user",
                "session_id": "test_session"
            })
            
            assert response.status_code == 200
            data = response.json()
            assert "therapeutic_response" in data
            assert "emotion" in data
            assert "transcribed_text" in data
    
    def test_start_session_invalid_audio(self, client):
        """Test session start with invalid audio data."""
        response = client.post("/api/v1/session/start", json={
            "audio_data": "invalid_base64_data",
            "user_id": "test_user",
            "session_id": "test_session"
        })
        
        # Should still return 200 but with error handling
        assert response.status_code == 200
    
    def test_start_session_missing_fields(self, client):
        """Test session start with missing required fields."""
        response = client.post("/api/v1/session/start", json={
            "audio_data": "some_data"
            # Missing user_id and session_id
        })
        
        assert response.status_code == 422  # Validation error
    
    def test_health_check(self, client):
        """Test health check endpoint."""
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert "status" in data
        assert "models" in data
        assert "ready" in data
    
    def test_root_endpoint(self, client):
        """Test root endpoint."""
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert "message" in data

class TestMoodEndpoints:
    """Test cases for mood-related API endpoints."""
    
    def test_log_mood_success(self, client, test_mood_request):
        """Test successful mood logging."""
        response = client.post("/api/v1/mood/log", json=test_mood_request)
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
    
    def test_get_mood_trends(self, client):
        """Test getting mood trends."""
        response = client.get("/api/v1/mood/trends/test_user")
        assert response.status_code == 200
        data = response.json()
        assert "trends" in data
    
    def test_log_mood_invalid_data(self, client):
        """Test mood logging with invalid data."""
        response = client.post("/api/v1/mood/log", json={
            "user_id": "test_user",
            "mood_data": {
                "emotion": "invalid_emotion",
                "intensity": 15  # Invalid intensity
            }
        })
        # Should handle gracefully
        assert response.status_code in [200, 422]

class TestCORSHeaders:
    """Test CORS configuration."""
    
    def test_cors_headers(self, client):
        """Test that CORS headers are properly set."""
        response = client.options("/api/v1/session/start")
        assert response.status_code == 200
        # CORS headers should be present
        assert "access-control-allow-origin" in response.headers
