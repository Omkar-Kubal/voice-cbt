"""
Advanced logging configuration for Voice CBT application.
Provides structured logging with different levels and handlers.
"""

import logging
import logging.handlers
import os
import sys
from datetime import datetime
from pathlib import Path
from typing import Optional, Dict, Any
import json
import traceback

class VoiceCBTFormatter(logging.Formatter):
    """Custom formatter for Voice CBT logs."""
    
    def format(self, record):
        # Add timestamp
        record.timestamp = datetime.now().isoformat()
        
        # Add service context
        if not hasattr(record, 'service'):
            record.service = 'voice-cbt'
        
        # Format the message
        if record.levelno >= logging.ERROR:
            # Include stack trace for errors
            record.stack_trace = traceback.format_exc()
            return super().format(record)
        else:
            return super().format(record)

class JSONFormatter(logging.Formatter):
    """JSON formatter for structured logging."""
    
    def format(self, record):
        log_entry = {
            'timestamp': datetime.now().isoformat(),
            'level': record.levelname,
            'service': getattr(record, 'service', 'voice-cbt'),
            'message': record.getMessage(),
            'module': record.module,
            'function': record.funcName,
            'line': record.lineno
        }
        
        # Add extra fields
        if hasattr(record, 'user_id'):
            log_entry['user_id'] = record.user_id
        if hasattr(record, 'session_id'):
            log_entry['session_id'] = record.session_id
        if hasattr(record, 'request_id'):
            log_entry['request_id'] = record.request_id
        
        # Add stack trace for errors
        if record.levelno >= logging.ERROR:
            log_entry['stack_trace'] = traceback.format_exc()
        
        return json.dumps(log_entry)

def setup_logging(
    log_level: str = "INFO",
    log_file: Optional[str] = None,
    enable_console: bool = True,
    enable_json: bool = False
) -> logging.Logger:
    """
    Set up comprehensive logging for Voice CBT application.
    
    Args:
        log_level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        log_file: Path to log file (optional)
        enable_console: Enable console logging
        enable_json: Use JSON formatting for structured logs
    
    Returns:
        Configured logger instance
    """
    
    # Create logs directory
    logs_dir = Path("logs")
    logs_dir.mkdir(exist_ok=True)
    
    # Configure root logger
    logger = logging.getLogger('voice-cbt')
    logger.setLevel(getattr(logging, log_level.upper()))
    
    # Clear existing handlers
    logger.handlers.clear()
    
    # Console handler
    if enable_console:
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(logging.INFO)
        
        if enable_json:
            console_formatter = JSONFormatter()
        else:
            console_formatter = VoiceCBTFormatter(
                '%(timestamp)s | %(levelname)-8s | %(service)s | %(message)s'
            )
        
        console_handler.setFormatter(console_formatter)
        logger.addHandler(console_handler)
    
    # File handler
    if log_file:
        file_handler = logging.handlers.RotatingFileHandler(
            log_file,
            maxBytes=10*1024*1024,  # 10MB
            backupCount=5
        )
        file_handler.setLevel(logging.DEBUG)
        
        if enable_json:
            file_formatter = JSONFormatter()
        else:
            file_formatter = VoiceCBTFormatter(
                '%(timestamp)s | %(levelname)-8s | %(service)s | %(module)s:%(funcName)s:%(lineno)d | %(message)s'
            )
        
        file_handler.setFormatter(file_formatter)
        logger.addHandler(file_handler)
    
    # Error handler (separate file for errors)
    error_handler = logging.handlers.RotatingFileHandler(
        logs_dir / "errors.log",
        maxBytes=5*1024*1024,  # 5MB
        backupCount=3
    )
    error_handler.setLevel(logging.ERROR)
    error_handler.setFormatter(VoiceCBTFormatter(
        '%(timestamp)s | %(levelname)-8s | %(service)s | %(module)s:%(funcName)s:%(lineno)d | %(message)s\n%(stack_trace)s'
    ))
    logger.addHandler(error_handler)
    
    return logger

def get_logger(name: str = 'voice-cbt') -> logging.Logger:
    """Get a logger instance."""
    return logging.getLogger(name)

class LogContext:
    """Context manager for adding structured logging context."""
    
    def __init__(self, logger: logging.Logger, **context):
        self.logger = logger
        self.context = context
        self.old_factory = None
    
    def __enter__(self):
        # Store old record factory
        self.old_factory = logging.getLogRecordFactory()
        
        # Create new factory with context
        def record_factory(*args, **kwargs):
            record = self.old_factory(*args, **kwargs)
            for key, value in self.context.items():
                setattr(record, key, value)
            return record
        
        logging.setLogRecordFactory(record_factory)
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        # Restore old factory
        logging.setLogRecordFactory(self.old_factory)

# Global logger instance
logger = setup_logging(
    log_level=os.getenv("LOG_LEVEL", "INFO"),
    log_file="logs/voice-cbt.log",
    enable_console=True,
    enable_json=os.getenv("LOG_JSON", "false").lower() == "true"
)
