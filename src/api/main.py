"""
BoAI API الرئيسي - نقطة الدخول الرئيسية للتطبيق

هذا الملف يحتوي على تطبيق FastAPI الرئيسي وتهيئة جميع routers
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
import logging
from typing import List

from src.core.config import settings
from src.api.routers import chat

# إعداد التسجيل
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def create_app() -> FastAPI:
    """
    إنشاء وتهيئة تطبيق FastAPI
    """
    app = FastAPI(
        title="BoAI API",
        description="منصة الذكاء الاصطناعي التعليمي المفتوحة المصدر",
        version="1.0.0",
        docs_url="/docs",
        redoc_url="/redoc",
        openapi_url="/openapi.json"
    )
    
    # إضافة middleware للأمان
    app.add_middleware(
        TrustedHostMiddleware,
        allowed_hosts=settings.ALLOWED_HOSTS
    )
    
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # تسجيل event handlers
    @app.on_event("startup")
    async def startup_event():
        logger.info("BoAI API يبدأ التشغيل...")
        # تهيئة الاتصال بقاعدة البيانات هنا لاحقاً
        # await database.connect()
    
    @app.on_event("shutdown")
    async def shutdown_event():
        logger.info("BoAI API يتوقف...")
        # إغلاق الاتصال بقاعدة البيانات هنا لاحقاً
        # await database.disconnect()
    
    # تضمين routers
    app.include_router(chat.router, prefix="/api/v1")
    
    # سيتم إضافة routers أخرى لاحقاً
    # from src.api.routers import models, users
    # app.include_router(models.router, prefix="/api/v1")
    # app.include_router(users.router, prefix="/api/v1")
    
    # Route أساسي للصحة
    @app.get("/")
    async def root():
        return {
            "message": "مرحباً بكم في BoAI API",
            "version": "1.0.0",
            "status": "يعمل"
        }
    
    @app.get("/health")
    async def health_check():
        return {
            "status": "healthy",
            "timestamp": "2025-08-24T22:45:00Z"
        }
    
    return app

# إنشاء التطبيق
app = create_app()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "src.api.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG
    )
