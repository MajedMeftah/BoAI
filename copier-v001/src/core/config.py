"""
إعدادات التطبيق الأساسية - إدارة متغيرات البيئة والإعدادات
"""

import os
from typing import List
from pydantic import AnyUrl, validator
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

# تحميل متغيرات البيئة من ملف .env
load_dotenv()

class Settings(BaseSettings):
    """إعدادات التطبيق الأساسية"""
    
    # الإعدادات العامة
    APP_NAME: str = "BoAI"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = os.getenv("DEBUG", "False").lower() == "true"
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")
    
    # إعدادات الخادم
    HOST: str = os.getenv("HOST", "0.0.0.0")
    PORT: int = int(os.getenv("PORT", "8000"))
    
    # إعدادات قاعدة البيانات
    DATABASE_URL: str = os.getenv("DATABASE_URL", "postgresql://boai:boai@localhost:5432/boai")
    REDIS_URL: str = os.getenv("REDIS_URL", "redis://localhost:6379/0")
    DB_POOL_SIZE: int = int(os.getenv("DB_POOL_SIZE", "5"))
    DB_MAX_OVERFLOW: int = int(os.getenv("DB_MAX_OVERFLOW", "10"))
    DB_POOL_TIMEOUT: int = int(os.getenv("DB_POOL_TIMEOUT", "30"))
    DB_POOL_RECYCLE: int = int(os.getenv("DB_POOL_RECYCLE", "3600"))
    
    # إعدادات الأمان
    SECRET_KEY: str = os.getenv("SECRET_KEY", "change-me-in-production")
    ALGORITHM: str = os.getenv("ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))
    
    # إعدادات CORS
    CORS_ORIGINS: List[str] = os.getenv("CORS_ORIGINS", "http://localhost:3000,http://localhost:8000").split(",")
    ALLOWED_HOSTS: List[str] = os.getenv("ALLOWED_HOSTS", "localhost,127.0.0.1,0.0.0.0").split(",")
    
    # إعدادات ML والنماذج
    MODELS_DIR: str = os.getenv("MODELS_DIR", "models")
    DEFAULT_MODEL: str = os.getenv("DEFAULT_MODEL", "programming_tutor")
    DEFAULT_MODEL_VERSION: str = os.getenv("DEFAULT_MODEL_VERSION", "v1.0")
    
    # إعدادات التخزين المؤقت
    CACHE_TTL: int = int(os.getenv("CACHE_TTL", "300"))  # 5 دقائق
    RATE_LIMIT_PER_MINUTE: int = int(os.getenv("RATE_LIMIT_PER_MINUTE", "60"))
    
    # التحقق من صحة الإعدادات
    @validator("DATABASE_URL")
    def validate_database_url(cls, v):
        if not v:
            raise ValueError("DATABASE_URL مطلوب")
        return v
    
    @validator("SECRET_KEY")
    def validate_secret_key(cls, v):
        if v == "change-me-in-production" and os.getenv("ENVIRONMENT") == "production":
            raise ValueError("يجب تغيير SECRET_KEY في بيئة الإنتاج")
        return v
    
    class Config:
        env_file = ".env"
        case_sensitive = False

# إنشاء instance من الإعدادات
settings = Settings()

# إعدادات إضافية بناء على البيئة
if settings.ENVIRONMENT == "production":
    settings.DEBUG = False
    settings.CORS_ORIGINS = ["https://boai.dev", "https://www.boai.dev"]
elif settings.ENVIRONMENT == "staging":
    settings.DEBUG = True
    settings.CORS_ORIGINS = ["https://staging.boai.dev"]
else:  # development
    settings.DEBUG = True
    settings.CORS_ORIGINS = ["http://localhost:3000", "http://localhost:8000"]
