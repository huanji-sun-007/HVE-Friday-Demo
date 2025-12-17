"""Application configuration settings."""

from typing import List
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings and configuration.
    
    All settings can be overridden via environment variables.
    """
    
    # Application Metadata
    app_name: str = "FastAPI Baseline Server"
    app_version: str = "1.0.0"
    app_description: str = "A production-ready FastAPI baseline server with modern best practices"
    
    # API Configuration
    api_prefix: str = "/api/v1"
    debug: bool = False
    
    # CORS Configuration
    cors_origins: List[str] = ["*"]
    cors_credentials: bool = True
    cors_methods: List[str] = ["*"]
    cors_headers: List[str] = ["*"]
    
    # Security
    secret_key: str = "your-secret-key-here-change-in-production"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    
    class Config:
        env_file = ".env"
        case_sensitive = False


# Global settings instance
settings = Settings()
