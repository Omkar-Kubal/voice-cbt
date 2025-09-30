"""
Integration tests for the complete Voice CBT pipeline.
"""

import pytest
import asyncio
from unittest.mock import patch, Mock
import tempfile
import os

class TestCompletePipeline:
    """Test the complete voice CBT pipeline from audio input to therapeutic response."""
    
    @pytest.mark.asyncio
    async def test_complete_session_flow(self, client, sample_audio_data):
        """Test complete session flow from audio input to response."""
        with patch('app.services.emotion_detector.emotion_detector') as mock_emotion, \
             patch('app.services.reply_generator.reply_generator') as mock_reply, \
             patch('app.services.speech_to_text_config.transcribe_audio') as mock_stt, \
             patch('app.services.tts.text_to_speech') as mock_tts:
            
            # Mock all services
            mock_emotion.detect_emotion_from_base64.return_value = {
                "emotion": "anxious",
                "confidence": 0.85,
                "error": False
            }
            mock_reply.generate_reply.return_value = "I understand you're feeling anxious. Let's work through some breathing exercises together."
            mock_stt.return_value = "I'm feeling really anxious about my presentation tomorrow"
            mock_tts.return_value = "base64_encoded_audio_response"
            
            # Make the API call
            response = client.post("/api/v1/session/start", json={
                "audio_data": sample_audio_data,
                "user_id": "test_user",
                "session_id": "test_session"
            })
            
            assert response.status_code == 200
            data = response.json()
            
            # Verify all components were called
            mock_stt.assert_called_once()
            mock_emotion.detect_emotion_from_base64.assert_called_once()
            mock_reply.generate_reply.assert_called_once()
            mock_tts.assert_called_once()
            
            # Verify response structure
            assert "therapeutic_response" in data
            assert "emotion" in data
            assert "transcribed_text" in data
            assert "audio_response" in data
    
    @pytest.mark.asyncio
    async def test_pipeline_with_fallback_services(self, client, sample_audio_data):
        """Test pipeline when some services fail and fallbacks are used."""
        with patch('app.services.emotion_detector.emotion_detector') as mock_emotion, \
             patch('app.services.reply_generator.reply_generator') as mock_reply, \
             patch('app.services.speech_to_text_config.transcribe_audio') as mock_stt, \
             patch('app.services.tts.text_to_speech') as mock_tts:
            
            # Mock services with some failures
            mock_emotion.detect_emotion_from_base64.return_value = {
                "emotion": "neutral",
                "confidence": 0.5,
                "error": True,
                "fallback": True
            }
            mock_reply.generate_reply.return_value = "I'm here to help you work through your feelings."
            mock_stt.return_value = "Error: Could not process audio"
            mock_tts.return_value = "base64_encoded_audio_response"
            
            response = client.post("/api/v1/session/start", json={
                "audio_data": sample_audio_data,
                "user_id": "test_user",
                "session_id": "test_session"
            })
            
            # Should still return 200 even with some service failures
            assert response.status_code == 200
            data = response.json()
            
            # Should have fallback responses
            assert "therapeutic_response" in data
            assert data["emotion"] == "neutral"  # Fallback emotion
    
    @pytest.mark.asyncio
    async def test_concurrent_sessions(self, client, sample_audio_data):
        """Test handling multiple concurrent sessions."""
        import asyncio
        
        async def make_request():
            return client.post("/api/v1/session/start", json={
                "audio_data": sample_audio_data,
                "user_id": f"user_{asyncio.current_task().get_name()}",
                "session_id": f"session_{asyncio.current_task().get_name()}"
            })
        
        # Create multiple concurrent requests
        tasks = [make_request() for _ in range(3)]
        responses = await asyncio.gather(*tasks)
        
        # All requests should succeed
        for response in responses:
            assert response.status_code == 200
    
    def test_mood_tracking_integration(self, client):
        """Test mood tracking integration with the system."""
        # Log a mood
        mood_response = client.post("/api/v1/mood/log", json={
            "user_id": "test_user",
            "mood_data": {
                "emotion": "anxious",
                "intensity": 7,
                "timestamp": "2024-01-01T12:00:00Z"
            }
        })
        assert mood_response.status_code == 200
        
        # Get mood trends
        trends_response = client.get("/api/v1/mood/trends/test_user")
        assert trends_response.status_code == 200
        trends_data = trends_response.json()
        assert "trends" in trends_data

class TestErrorHandling:
    """Test error handling across the system."""
    
    def test_invalid_audio_format(self, client):
        """Test handling of invalid audio format."""
        response = client.post("/api/v1/session/start", json={
            "audio_data": "invalid_base64_data",
            "user_id": "test_user",
            "session_id": "test_session"
        })
        
        # Should handle gracefully
        assert response.status_code == 200
    
    def test_malformed_request(self, client):
        """Test handling of malformed requests."""
        response = client.post("/api/v1/session/start", json={
            "invalid_field": "invalid_value"
        })
        
        assert response.status_code == 422  # Validation error
    
    def test_service_timeout_handling(self, client, sample_audio_data):
        """Test handling of service timeouts."""
        with patch('app.services.speech_to_text_config.transcribe_audio') as mock_stt:
            # Simulate timeout
            import asyncio
            async def timeout_simulation():
                await asyncio.sleep(10)  # Simulate long processing
                return "timeout"
            
            mock_stt.side_effect = asyncio.TimeoutError("Service timeout")
            
            response = client.post("/api/v1/session/start", json={
                "audio_data": sample_audio_data,
                "user_id": "test_user",
                "session_id": "test_session"
            })
            
            # Should handle timeout gracefully
            assert response.status_code == 200

class TestPerformance:
    """Test performance characteristics."""
    
    def test_response_time(self, client, sample_audio_data):
        """Test that responses are returned within acceptable time."""
        import time
        
        start_time = time.time()
        response = client.post("/api/v1/session/start", json={
            "audio_data": sample_audio_data,
            "user_id": "test_user",
            "session_id": "test_session"
        })
        end_time = time.time()
        
        response_time = end_time - start_time
        assert response.status_code == 200
        assert response_time < 10.0  # Should respond within 10 seconds
    
    def test_memory_usage(self, client, sample_audio_data):
        """Test memory usage during processing."""
        import psutil
        import os
        
        process = psutil.Process(os.getpid())
        initial_memory = process.memory_info().rss
        
        # Make several requests
        for _ in range(5):
            response = client.post("/api/v1/session/start", json={
                "audio_data": sample_audio_data,
                "user_id": "test_user",
                "session_id": "test_session"
            })
            assert response.status_code == 200
        
        final_memory = process.memory_info().rss
        memory_increase = final_memory - initial_memory
        
        # Memory increase should be reasonable (less than 100MB)
        assert memory_increase < 100 * 1024 * 1024
