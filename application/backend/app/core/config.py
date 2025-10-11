"""
Application configuration management using Pydantic Settings
"""
from typing import List, Optional
from pydantic import Field, field_validator
from pydantic_settings import BaseSettings
import secrets


class Settings(BaseSettings):
    """Application settings with environment variable support"""
    
    # Application
    APP_NAME: str = "Stylic AI"
    APP_VERSION: str = "1.0.0"
    APP_ENV: str = "development"
    DEBUG: bool = True
    API_V1_PREFIX: str = "/api/v1"
    
    # Server
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    WORKERS: int = 4
    
    # Security
    SECRET_KEY: str = Field(default_factory=lambda: secrets.token_urlsafe(32))
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    
    # Database
    MONGO_URL: str
    MONGO_DB_NAME: str = "stylic"
    MONGO_MAX_POOL_SIZE: int = 10
    MONGO_MIN_POOL_SIZE: int = 1
    
    # Email
    SMTP_SERVER: str
    SMTP_PORT: int = 587
    SMTP_USERNAME: str
    SMTP_PASSWORD: str
    EMAIL_FROM: str
    EMAIL_FROM_NAME: str = "Stylic AI"
    
    # URLs
    FRONTEND_URL: str = "http://localhost:3000"
    DOMAIN_URL: str = "https://app.stylic.ai"
    
    # Razorpay
    RAZORPAY_KEY_ID: str
    RAZORPAY_KEY_SECRET: str
    
    # AI APIs
    OPENAI_API_KEY: Optional[str] = None
    GOOGLE_AI_API_KEY: Optional[str] = None
    ANTHROPIC_API_KEY: Optional[str] = None
    
    # File Upload
    MAX_UPLOAD_SIZE: int = 10485760  # 10MB
    ALLOWED_IMAGE_EXTENSIONS: str = "png,jpg,jpeg,gif,bmp,webp"
    UPLOAD_DIR: str = "uploads"

    # Logging
    LOG_LEVEL: str = "INFO"
    LOG_FILE: str = "logs/app.log"
    LOG_MAX_BYTES: int = 10485760  # 10MB
    LOG_BACKUP_COUNT: int = 5

    # CORS
    CORS_ORIGINS: str = "http://localhost:3000,http://localhost:19006"
    CORS_ALLOW_CREDENTIALS: bool = True
    CORS_ALLOW_METHODS: str = "*"
    CORS_ALLOW_HEADERS: str = "*"
    
    # Rate Limiting
    RATE_LIMIT_PER_MINUTE: int = 60
    
    # Credits
    DEFAULT_SIGNUP_CREDITS: int = 5
    
    # Temp Email Domains (for validation)
    TEMP_EMAIL_DOMAINS: List[str] = [
        '10minutemail.com', 'guerrillamail.com', 'mailinator.com',
        'tempmail.org', 'yopmail.com', 'throwaway.email',
        'temp-mail.org', 'dispostable.com', 'fakemailgenerator.com'
    ]
    
    # Coupon Codes
    COUPONS: dict = {
        "SAVE15": 15,
        "SAVE10": 10,
        "SAVE5": 5,
        "SAVE20": 20,
        "SAVE25": 25,
        "SAVE30": 30,
        "SAVE35": 35,
        "SAVE40": 40,
        "SAVE45": 45,
        "SAVE50": 50
    }
    
    def get_cors_origins_list(self) -> List[str]:
        """Parse CORS origins from comma-separated string"""
        if isinstance(self.CORS_ORIGINS, str):
            return [origin.strip() for origin in self.CORS_ORIGINS.split(",")]
        return self.CORS_ORIGINS

    def get_allowed_extensions_list(self) -> List[str]:
        """Parse allowed extensions from comma-separated string"""
        if isinstance(self.ALLOWED_IMAGE_EXTENSIONS, str):
            return [ext.strip() for ext in self.ALLOWED_IMAGE_EXTENSIONS.split(",")]
        return self.ALLOWED_IMAGE_EXTENSIONS

    class Config:
        env_file = ".env"
        case_sensitive = True


# Create global settings instance
settings = Settings()

