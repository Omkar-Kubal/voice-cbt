"""
Production configuration management for Voice CBT application.
"""

import os
import secrets
import string
from typing import Optional, List
from pydantic_settings import BaseSettings
from pydantic import Field, validator

class ProductionSettings(BaseSettings):
    """Production settings with validation and security."""
    
    # Database Configuration
    DATABASE_URL: str = Field(..., description="Database connection URL")
    DB_HOST: str = Field(default="localhost", description="Database host")
    DB_PASSWORD: str = Field(..., description="Database password")
    DB_NAME: str = Field(default="voicecbt_prod", description="Database name")
    
    # ClickHouse Configuration
    CLICKHOUSE_HOST: str = Field(default="localhost", description="ClickHouse host")
    CLICKHOUSE_PORT: int = Field(default=8123, description="ClickHouse port")
    CLICKHOUSE_USER: str = Field(default="default", description="ClickHouse user")
    CLICKHOUSE_PASSWORD: str = Field(default="", description="ClickHouse password")
    CLICKHOUSE_DB: str = Field(default="voice_cbt_prod", description="ClickHouse database")
    
    # Model Configuration
    MODEL_PATH: str = Field(default="/app/trained_models/", description="Path to trained models")
    CUDA_VISIBLE_DEVICES: str = Field(default="0", description="CUDA device IDs")
    MODEL_CACHE_SIZE: int = Field(default=2, description="Model cache size")
    
    # Speech-to-Text Configuration
    STT_SERVICE: str = Field(default="whisper", description="STT service to use")
    WHISPER_MODEL: str = Field(default="base", description="Whisper model size")
    STT_TIMEOUT: int = Field(default=30, description="STT timeout in seconds")
    
    # Audio Processing
    AUDIO_SAMPLE_RATE: int = Field(default=16000, description="Audio sample rate")
    AUDIO_CHANNELS: int = Field(default=1, description="Audio channels")
    AUDIO_MAX_DURATION: int = Field(default=300, description="Max audio duration in seconds")
    AUDIO_MAX_SIZE_MB: int = Field(default=50, description="Max audio file size in MB")
    
    # RAG Configuration
    RAG_ENABLED: bool = Field(default=True, description="Enable RAG system")
    CHROMA_DB_PATH: str = Field(default="/app/chroma_db", description="ChromaDB path")
    RAG_TOP_K: int = Field(default=5, description="Number of top documents to retrieve")
    RAG_SIMILARITY_THRESHOLD: float = Field(default=0.7, description="Similarity threshold for RAG")
    
    # API Configuration
    API_HOST: str = Field(default="0.0.0.0", description="API host")
    API_PORT: int = Field(default=8000, description="API port")
    DEBUG: bool = Field(default=False, description="Debug mode")
    LOG_LEVEL: str = Field(default="INFO", description="Log level")
    LOG_FILE: str = Field(default="/app/logs/voice_cbt.log", description="Log file path")
    
    # Security Configuration
    JWT_SECRET_KEY: str = Field(..., description="JWT secret key")
    JWT_ALGORITHM: str = Field(default="HS256", description="JWT algorithm")
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(default=30, description="JWT token expiry")
    ENCRYPTION_KEY: str = Field(..., description="Encryption key for sensitive data")
    CORS_ORIGINS: List[str] = Field(default=["*"], description="CORS allowed origins")
    
    # Rate Limiting
    RATE_LIMIT_REQUESTS: int = Field(default=100, description="Rate limit requests per window")
    RATE_LIMIT_WINDOW: int = Field(default=3600, description="Rate limit window in seconds")
    
    # Monitoring & Analytics
    ENABLE_METRICS: bool = Field(default=True, description="Enable metrics collection")
    METRICS_RETENTION_DAYS: int = Field(default=90, description="Metrics retention period")
    HEALTH_CHECK_INTERVAL: int = Field(default=60, description="Health check interval")
    
    # External Services
    OPENAI_API_KEY: Optional[str] = Field(default=None, description="OpenAI API key")
    AZURE_SPEECH_KEY: Optional[str] = Field(default=None, description="Azure Speech key")
    AZURE_SPEECH_REGION: Optional[str] = Field(default=None, description="Azure Speech region")
    
    # Performance Tuning
    MAX_WORKERS: int = Field(default=4, description="Maximum number of workers")
    WORKER_TIMEOUT: int = Field(default=300, description="Worker timeout in seconds")
    KEEPALIVE_TIMEOUT: int = Field(default=5, description="Keepalive timeout")
    
    # Backup Configuration
    BACKUP_ENABLED: bool = Field(default=True, description="Enable backups")
    BACKUP_SCHEDULE: str = Field(default="0 2 * * *", description="Backup schedule (cron)")
    BACKUP_RETENTION_DAYS: int = Field(default=30, description="Backup retention period")
    BACKUP_S3_BUCKET: Optional[str] = Field(default=None, description="S3 bucket for backups")
    
    # Email Configuration
    SMTP_HOST: Optional[str] = Field(default=None, description="SMTP host")
    SMTP_PORT: int = Field(default=587, description="SMTP port")
    SMTP_USERNAME: Optional[str] = Field(default=None, description="SMTP username")
    SMTP_PASSWORD: Optional[str] = Field(default=None, description="SMTP password")
    EMAIL_FROM: Optional[str] = Field(default=None, description="From email address")
    
    # Redis Configuration
    REDIS_HOST: Optional[str] = Field(default=None, description="Redis host")
    REDIS_PORT: int = Field(default=6379, description="Redis port")
    REDIS_PASSWORD: Optional[str] = Field(default=None, description="Redis password")
    REDIS_DB: int = Field(default=0, description="Redis database number")
    
    # File Storage
    UPLOAD_MAX_SIZE_MB: int = Field(default=100, description="Max upload size in MB")
    STORAGE_TYPE: str = Field(default="local", description="Storage type (local, s3)")
    S3_BUCKET: Optional[str] = Field(default=None, description="S3 bucket name")
    S3_REGION: Optional[str] = Field(default=None, description="S3 region")
    S3_ACCESS_KEY: Optional[str] = Field(default=None, description="S3 access key")
    S3_SECRET_KEY: Optional[str] = Field(default=None, description="S3 secret key")
    
    @validator('JWT_SECRET_KEY')
    def validate_jwt_secret(cls, v):
        if len(v) < 32:
            raise ValueError('JWT_SECRET_KEY must be at least 32 characters long')
        return v
    
    @validator('ENCRYPTION_KEY')
    def validate_encryption_key(cls, v):
        if len(v) < 32:
            raise ValueError('ENCRYPTION_KEY must be at least 32 characters long')
        return v
    
    @validator('CORS_ORIGINS')
    def validate_cors_origins(cls, v):
        if isinstance(v, str):
            return [origin.strip() for origin in v.split(',')]
        return v
    
    @validator('LOG_LEVEL')
    def validate_log_level(cls, v):
        valid_levels = ['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']
        if v.upper() not in valid_levels:
            raise ValueError(f'LOG_LEVEL must be one of {valid_levels}')
        return v.upper()
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True

def generate_secret_key(length: int = 32) -> str:
    """Generate a secure random secret key."""
    alphabet = string.ascii_letters + string.digits + "!@#$%^&*"
    return ''.join(secrets.choice(alphabet) for _ in range(length))

def create_production_env_file(env_file_path: str = "config.production.env"):
    """Create a production environment file with secure defaults."""
    
    # Generate secure keys
    jwt_secret = generate_secret_key(64)
    encryption_key = generate_secret_key(64)
    db_password = generate_secret_key(32)
    
    env_content = f"""# Voice CBT Production Environment Configuration
# Generated on {os.popen('date').read().strip()}

# Database Configuration
DATABASE_URL=postgresql+asyncpg://voicecbt_user:{db_password}@${{DB_HOST}}:5432/voicecbt_prod
DB_HOST=localhost
DB_PASSWORD={db_password}
DB_NAME=voicecbt_prod

# ClickHouse Configuration
CLICKHOUSE_HOST=${{CLICKHOUSE_HOST}}
CLICKHOUSE_PORT=8123
CLICKHOUSE_USER=default
CLICKHOUSE_PASSWORD=${{CLICKHOUSE_PASSWORD}}
CLICKHOUSE_DB=voice_cbt_prod

# Model Configuration
MODEL_PATH=/app/trained_models/
CUDA_VISIBLE_DEVICES=0
MODEL_CACHE_SIZE=2

# Speech-to-Text Configuration
STT_SERVICE=whisper
WHISPER_MODEL=base
STT_TIMEOUT=30

# Audio Processing
AUDIO_SAMPLE_RATE=16000
AUDIO_CHANNELS=1
AUDIO_MAX_DURATION=300
AUDIO_MAX_SIZE_MB=50

# RAG Configuration
RAG_ENABLED=true
CHROMA_DB_PATH=/app/chroma_db
RAG_TOP_K=5
RAG_SIMILARITY_THRESHOLD=0.7

# API Configuration
API_HOST=0.0.0.0
API_PORT=8000
DEBUG=false
LOG_LEVEL=INFO
LOG_FILE=/app/logs/voice_cbt.log

# Security Configuration
JWT_SECRET_KEY={jwt_secret}
JWT_ALGORITHM=HS256
JWT_ACCESS_TOKEN_EXPIRE_MINUTES=30
ENCRYPTION_KEY={encryption_key}
CORS_ORIGINS=https://yourdomain.com,https://www.yourdomain.com

# Rate Limiting
RATE_LIMIT_REQUESTS=100
RATE_LIMIT_WINDOW=3600

# Monitoring & Analytics
ENABLE_METRICS=true
METRICS_RETENTION_DAYS=90
HEALTH_CHECK_INTERVAL=60

# External Services (Set these in your deployment)
OPENAI_API_KEY=${{OPENAI_API_KEY}}
AZURE_SPEECH_KEY=${{AZURE_SPEECH_KEY}}
AZURE_SPEECH_REGION=${{AZURE_SPEECH_REGION}}

# Performance Tuning
MAX_WORKERS=4
WORKER_TIMEOUT=300
KEEPALIVE_TIMEOUT=5

# Backup Configuration
BACKUP_ENABLED=true
BACKUP_SCHEDULE=0 2 * * *
BACKUP_RETENTION_DAYS=30
BACKUP_S3_BUCKET=${{BACKUP_S3_BUCKET}}

# Email Configuration
SMTP_HOST=${{SMTP_HOST}}
SMTP_PORT=587
SMTP_USERNAME=${{SMTP_USERNAME}}
SMTP_PASSWORD=${{SMTP_PASSWORD}}
EMAIL_FROM=${{EMAIL_FROM}}

# Redis Configuration
REDIS_HOST=${{REDIS_HOST}}
REDIS_PORT=6379
REDIS_PASSWORD=${{REDIS_PASSWORD}}
REDIS_DB=0

# File Storage
UPLOAD_MAX_SIZE_MB=100
STORAGE_TYPE=s3
S3_BUCKET=${{S3_BUCKET}}
S3_REGION=${{S3_REGION}}
S3_ACCESS_KEY=${{S3_ACCESS_KEY}}
S3_SECRET_KEY=${{S3_SECRET_KEY}}
"""
    
    with open(env_file_path, 'w') as f:
        f.write(env_content)
    
    print(f"✅ Production environment file created: {env_file_path}")
    print(f"🔐 Generated secure keys for JWT and encryption")
    print(f"⚠️  Please update the CORS_ORIGINS and other environment-specific values")

def validate_production_config() -> bool:
    """Validate production configuration."""
    try:
        settings = ProductionSettings()
        print("✅ Production configuration is valid")
        return True
    except Exception as e:
        print(f"❌ Production configuration validation failed: {e}")
        return False

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "generate":
        create_production_env_file()
    elif len(sys.argv) > 1 and sys.argv[1] == "validate":
        validate_production_config()
    else:
        print("Usage:")
        print("  python production_config.py generate  # Generate production env file")
        print("  python production_config.py validate   # Validate configuration")
