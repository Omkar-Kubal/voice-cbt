"""
Custom exceptions and error handling for Voice CBT application.
"""

from typing import Optional, Dict, Any
import traceback
from .logging import get_logger

logger = get_logger('voice-cbt.exceptions')

class VoiceCBTException(Exception):
    """Base exception for Voice CBT application."""
    
    def __init__(self, message: str, error_code: str = None, details: Dict[str, Any] = None):
        super().__init__(message)
        self.message = message
        self.error_code = error_code or "UNKNOWN_ERROR"
        self.details = details or {}
        self.traceback = traceback.format_exc()
        
        # Log the exception
        logger.error(f"VoiceCBTException: {message}", extra={
            'error_code': error_code,
            'details': details,
            'traceback': self.traceback
        })

class AuthenticationError(VoiceCBTException):
    """Authentication related errors."""
    
    def __init__(self, message: str = "Authentication failed", details: Dict[str, Any] = None):
        super().__init__(message, "AUTH_ERROR", details)

class AuthorizationError(VoiceCBTException):
    """Authorization related errors."""
    
    def __init__(self, message: str = "Access denied", details: Dict[str, Any] = None):
        super().__init__(message, "AUTHZ_ERROR", details)

class ValidationError(VoiceCBTException):
    """Data validation errors."""
    
    def __init__(self, message: str = "Validation failed", details: Dict[str, Any] = None):
        super().__init__(message, "VALIDATION_ERROR", details)

class DatabaseError(VoiceCBTException):
    """Database related errors."""
    
    def __init__(self, message: str = "Database operation failed", details: Dict[str, Any] = None):
        super().__init__(message, "DATABASE_ERROR", details)

class AIServiceError(VoiceCBTException):
    """AI service related errors."""
    
    def __init__(self, message: str = "AI service error", details: Dict[str, Any] = None):
        super().__init__(message, "AI_SERVICE_ERROR", details)

class TTSError(VoiceCBTException):
    """Text-to-Speech related errors."""
    
    def __init__(self, message: str = "TTS service error", details: Dict[str, Any] = None):
        super().__init__(message, "TTS_ERROR", details)

class STTError(VoiceCBTException):
    """Speech-to-Text related errors."""
    
    def __init__(self, message: str = "STT service error", details: Dict[str, Any] = None):
        super().__init__(message, "STT_ERROR", details)

class EmotionDetectionError(VoiceCBTException):
    """Emotion detection related errors."""
    
    def __init__(self, message: str = "Emotion detection error", details: Dict[str, Any] = None):
        super().__init__(message, "EMOTION_DETECTION_ERROR", details)

class SessionError(VoiceCBTException):
    """Session related errors."""
    
    def __init__(self, message: str = "Session error", details: Dict[str, Any] = None):
        super().__init__(message, "SESSION_ERROR", details)

class RateLimitError(VoiceCBTException):
    """Rate limiting errors."""
    
    def __init__(self, message: str = "Rate limit exceeded", details: Dict[str, Any] = None):
        super().__init__(message, "RATE_LIMIT_ERROR", details)

class ConfigurationError(VoiceCBTException):
    """Configuration related errors."""
    
    def __init__(self, message: str = "Configuration error", details: Dict[str, Any] = None):
        super().__init__(message, "CONFIG_ERROR", details)

def handle_exception(exc: Exception, context: Dict[str, Any] = None) -> Dict[str, Any]:
    """
    Handle exceptions and return structured error response.
    
    Args:
        exc: The exception to handle
        context: Additional context information
    
    Returns:
        Structured error response
    """
    context = context or {}
    
    if isinstance(exc, VoiceCBTException):
        return {
            'error': True,
            'error_code': exc.error_code,
            'message': exc.message,
            'details': exc.details,
            'context': context
        }
    else:
        # Handle unexpected exceptions
        logger.error(f"Unexpected exception: {exc}", extra={
            'exception_type': type(exc).__name__,
            'context': context,
            'traceback': traceback.format_exc()
        })
        
        return {
            'error': True,
            'error_code': 'UNEXPECTED_ERROR',
            'message': 'An unexpected error occurred',
            'details': {
                'exception_type': type(exc).__name__,
                'original_message': str(exc)
            },
            'context': context
        }
