import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # Database settings for ClickHouse
    CLICKHOUSE_HOST: str = os.getenv("CLICKHOUSE_HOST", "localhost")
    CLICKHOUSE_PORT: int = os.getenv("CLICKHOUSE_PORT", 8123)
    CLICKHOUSE_USER: str = os.getenv("CLICKHOUSE_USER", "default")
    CLICKHOUSE_PASSWORD: str = os.getenv("CLICKHOUSE_PASSWORD", "")
    CLICKHOUSE_DB: str = os.getenv("CLICKHOUSE_DB", "voice_cbt")
    
    # Other application settings can go here
    API_V1_STR: str = "/api/v1"
    
    class Config:
        env_file = ".env"
        
settings = Settings()