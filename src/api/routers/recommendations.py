"""
واجهة برمجة التطبيقات للتوصيات الذكية - توصيات تعلم مخصصة

هذا الملف يحتوي على endpoints لتوليد توصيات تعلم مخصصة
بناءً على تحليل سلوك المستخدم وتفضيلاته
"""

from fastapi import APIRouter, Depends, HTTPException, status
from typing import List, Optional
import logging

from src.core.learning.recommendation_engine import recommendation_engine
from src.core.database.session import get_db
from src.core.database.models import User
from src.core.config import settings

# إعداد التسجيل
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/recommendations",
    tags=["recommendations"],
    responses={
        404: {"description": "Not found"},
        500: {"description": "Internal server error"}
    }
)

@router.get("/user/{user_id}", response_model=List[dict])
async def get_user_recommendations(
    user_id: str,
    max_recommendations: int = 5,
    db = Depends(get_db)
):
    """
    الحصول على توصيات تعلم مخصصة للمستخدم
    
    Args:
        user_id: معرف المستخدم
        max_recommendations: الحد الأقصى لعدد التوصيات (1-10)
        
    Returns:
        List[dict]: قائمة بالتوصيات المخصصة
    """
    try:
        # التحقق من وجود المستخدم
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="المستخدم غير موجود"
            )
        
        # التحقق من صحة عدد التوصيات
        if not 1 <= max_recommendations <= 10:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="عدد التوصيات يجب أن يكون بين 1 و 10"
            )
        
        # توليد التوصيات
        recommendations = recommendation_engine.generate_recommendations(
            user_id, max_recommendations
        )
        
        logger.info(f"تم توليد {len(recommendations)} توصية للمستخدم {user_id}")
        return recommendations
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"خطأ في توليد التوصيات للمستخدم {user_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="حدث خطأ أثناء توليد التوصيات"
        )

@router.get("/user/{user_id}/profile", response_model=dict)
async def get_user_profile(user_id: str, db = Depends(get_db)):
    """
    الحصول على ملف تعريف المستخدم مع التفضيلات والأنماط
    
    Args:
        user_id: معرف المستخدم
        
    Returns:
        dict: ملف تعريف المستخدم
    """
    try:
        # التحقق من وجود المستخدم
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="المستخدم غير موجود"
            )
        
        # تحليل سلوك المستخدم
        profile = recommendation_engine.analyze_user_behavior(user_id)
        
        logger.info(f"تم تحليل ملف تعريف المستخدم {user_id}")
        return profile
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"خطأ في تحليل ملف تعريف المستخدم {user_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="حدث خطأ أثناء تحليل ملف التعريف"
        )

@router.post("/user/{user_id}/feedback")
async def submit_user_feedback(
    user_id: str,
    content_id: int,
    rating: int,
    feedback_text: Optional[str] = None,
    db = Depends(get_db)
):
    """
    إرسال تغذية راجعة لتحديث التوصيات
    
    Args:
        user_id: معرف المستخدم
        content_id: معرف المحتوى
        rating: التقييم (1-5)
        feedback_text: نص التغذية الراجعة (اختياري)
        
    Returns:
        dict: رسالة نجاح
    """
    try:
        # التحقق من وجود المستخدم
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="المستخدم غير موجود"
            )
        
        # التحقق من صحة التقييم
        if not 1 <= rating <= 5:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="التقييم يجب أن يكون بين 1 و 5"
            )
        
        # تحديث التوصيات بناءً على التغذية الراجعة
        recommendation_engine.update_user_feedback(
            user_id, content_id, rating, feedback_text
        )
        
        logger.info(f"تم تحديث التغذية الراجعة للمستخدم {user_id} على المحتوى {content_id}")
        return {
            "message": "تم تسجيل التغذية الراجعة بنجاح",
            "user_id": user_id,
            "content_id": content_id,
            "rating": rating
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"خطأ في تسجيل التغذية الراجعة للمستخدم {user_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="حدث خطأ أثناء تسجيل التغذية الراجعة"
        )

@router.get("/user/{user_id}/learning-path", response_model=List[dict])
async def get_learning_path(
    user_id: str,
    goal: str,
    db = Depends(get_db)
):
    """
    الحصول على مسار تعلم مخصص لهدف معين
    
    Args:
        user_id: معرف المستخدم
        goal: الهدف التعليمي
        
    Returns:
        List[dict]: مسار التعلم المكون من خطوات متسلسلة
    """
    try:
        # التحقق من وجود المستخدم
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="المستخدم غير موجود"
            )
        
        # التحقق من وجود الهدف
        if not goal or len(goal.strip()) < 3:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="الهدف التعليمي مطلوب ويجب أن يكون على الأقل 3 أحرف"
            )
        
        # إنشاء مسار التعلم
        learning_path = recommendation_engine.get_learning_path(user_id, goal.strip())
        
        logger.info(f"تم إنشاء مسار تعلم للمستخدم {user_id} للهدف '{goal}'")
        return learning_path
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"خطأ في إنشاء مسار التعلم للمستخدم {user_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="حدث خطأ أثناء إنشاء مسار التعلم"
        )

@router.get("/content", response_model=List[dict])
async def get_all_content():
    """
    الحصول على جميع المحتويات التعليمية المتاحة
    
    Returns:
        List[dict]: قائمة بجميع المحتويات التعليمية
    """
    try:
        # في الإصدار الحالي، نستخدم قاعدة البيانات المحلية
        # سيتم تحسين هذا لاحقاً للاتصال بقاعدة بيانات حقيقية
        content = recommendation_engine.content_db
        
        logger.info(f"تم جلب {len(content)} محتوى تعليمي")
        return content
        
    except Exception as e:
        logger.error(f"خطأ في جلب المحتويات التعليمية: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="حدث خطأ أثناء جلب المحتويات التعليمية"
        )

@router.get("/content/{content_id}", response_model=dict)
async def get_content_by_id(content_id: int):
    """
    الحصول على محتوى تعليمي محدد
    
    Args:
        content_id: معرف المحتوى
        
    Returns:
        dict: تفاصيل المحتوى التعليمي
    """
    try:
        # البحث عن المحتوى
        content = next(
            (c for c in recommendation_engine.content_db if c["id"] == content_id),
            None
        )
        
        if not content:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="المحتوى غير موجود"
            )
        
        logger.info(f"تم جلب المحتوى التعليمي {content_id}")
        return content
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"خطأ في جلب المحتوى التعليمي {content_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="حدث خطأ أثناء جلب المحتوى التعليمي"
        )

@router.get("/health")
async def recommendations_health():
    """
    فحص صحة نظام التوصيات
    
    Returns:
        dict: حالة النظام
    """
    try:
        # فحص بسيط للنظام
        test_recommendations = recommendation_engine.generate_recommendations(
            "test-user", 2
        )
        
        return {
            "status": "healthy",
            "engine_initialized": True,
            "test_recommendations_generated": len(test_recommendations) > 0,
            "content_items": len(recommendation_engine.content_db),
            "cached_profiles": len(recommendation_engine.user_profiles)
        }
        
    except Exception as e:
        logger.error(f"فحص صحة نظام التوصيات فشل: {e}")
        return {
            "status": "unhealthy",
            "error": str(e),
            "engine_initialized": False
        }

# مثال للاستخدام في التطبيق الرئيسي
if __name__ == "__main__":
    import uvicorn
    from fastapi import FastAPI
    
    app = FastAPI()
    app.include_router(router)
    
    uvicorn.run(app, host="0.0.0.0", port=8001)
