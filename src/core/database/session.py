"""
مدير جلسات قاعدة البيانات لـ BoAI

هذا الملف يحتوي على إدارة اتصالات قاعدة البيانات باستخدام SQLAlchemy
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.ext.declarative import declarative_base
from contextlib import contextmanager
import logging
from typing import Generator

from src.core.config import settings
from .models import Base

# إعداد التسجيل
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# إنشاء محرك قاعدة البيانات
def create_engine_from_settings():
    """إنشاء محرك قاعدة البيانات من الإعدادات"""
    database_url = settings.DATABASE_URL
    
    if database_url.startswith("sqlite"):
        # SQLite - للتطوير والاختبار
        engine = create_engine(
            database_url,
            connect_args={"check_same_thread": False},
            echo=settings.DEBUG
        )
    else:
        # PostgreSQL أو غيره - للإنتاج
        engine = create_engine(
            database_url,
            pool_size=settings.DB_POOL_SIZE,
            max_overflow=settings.DB_MAX_OVERFLOW,
            pool_timeout=settings.DB_POOL_TIMEOUT,
            pool_recycle=settings.DB_POOL_RECYCLE,
            echo=settings.DEBUG
        )
    
    return engine

# إنشاء المحرك وجلسة المصنع
engine = create_engine_from_settings()
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
ScopedSession = scoped_session(SessionLocal)

def init_db():
    """تهيئة قاعدة البيانات وإنشاء الجداول"""
    try:
        Base.metadata.create_all(bind=engine)
        logger.info("تم تهيئة قاعدة البيانات بنجاح")
    except Exception as e:
        logger.error(f"خطأ في تهيئة قاعدة البيانات: {e}")
        raise

def get_db() -> Generator:
    """
    الحصول على جلسة قاعدة البيانات للاعتماد عليها
    
    Yields:
        Generator: جلسة قاعدة البيانات
    """
    db = ScopedSession()
    try:
        yield db
    finally:
        db.close()

@contextmanager
def db_session():
    """
    مدير سياق لجلسة قاعدة البيانات للاستخدام اليدوي
    
    Yields:
        Session: جلسة قاعدة البيانات
    """
    session = ScopedSession()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()

def get_db_session():
    """
    الحصول على جلسة قاعدة البيانات مباشرة
    
    Returns:
        Session: جلسة قاعدة البيانات
    """
    return ScopedSession()

# تهيئة قاعدة البيانات عند الاستيراد
init_db()
