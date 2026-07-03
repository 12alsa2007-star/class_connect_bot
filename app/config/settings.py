from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """Основные настройки приложения"""
    
    # Bot
    BOT_TOKEN: str
    ADMINS: str = "1255498346"
    
    # Database
    DB_USER: str = "postgres"
    DB_PASSWORD: str = "postgres"
    DB_HOST: str = "localhost"
    DB_PORT: int = 5432
    DB_NAME: str = "class_connect_db"
    
    # SQLAlchemy
    DATABASE_URL: str
    
    # App
    TIMEZONE: str = "Europe/Moscow"
    DEBUG: bool = True
    LOG_LEVEL: str = "INFO"
    
    class Config:
        env_file = ".env"
        case_sensitive = False


settings = Settings()