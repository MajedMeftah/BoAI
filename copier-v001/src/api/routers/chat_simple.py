"""
Chat Router المبسط - واجهة برمجة التطبيقات للدردشة مع BoAI (نسخة مبسطة)

هذا الملف يحتوي على endpoints مبسطة للدردشة تعمل بدون نماذج ML
"""

from fastapi import APIRouter, HTTPException
from datetime import datetime
import logging

# إعداد التسجيل
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# إنشاء router
router = APIRouter(prefix="/chat", tags=["chat"])

# ردود افتراضية للدردشة
DEFAULT_RESPONSES = {
    "ar": {
        "greeting": "مرحباً! أنا BoAI، مساعدك الذكي لتعلم البرمجة. كيف يمكنني مساعدتك اليوم؟",
        "help": "يمكنني مساعدتك في تعلم البرمجة، الإجابة على الأسئلة التقنية، وشرح المفاهيم البرمجية.",
        "programming": "لتعلم البرمجة، أنصحك بالبدء بلغة Python لأنها سهلة للمبتدئين وقوية في نفس الوقت.",
        "default": "شكراً لسؤالك. أنا حالياً في وضع التطوير وسأكون قريباً قادراً على مساعدتك بشكل أفضل."
    },
    "en": {
        "greeting": "Hello! I'm BoAI, your smart programming learning assistant. How can I help you today?",
        "help": "I can help you learn programming, answer technical questions, and explain programming concepts.",
        "programming": "To learn programming, I recommend starting with Python as it's easy for beginners and powerful at the same time.",
        "default": "Thank you for your question. I'm currently in development mode and will soon be able to help you better."
    }
}

def detect_language_simple(text: str) -> str:
    """كشف اللغة بشكل مبسط"""
    arabic_chars = set('ابتثجحخدذرزسشصضطظعغفقكلمنهوي')
    if any(char in arabic_chars for char in text):
        return "ar"
    else:
        return "en"

def generate_simple_response(message: str, language: str = "auto") -> str:
    """توليد رد مبسط بدون نماذج ML"""
    if language == "auto":
        language = detect_language_simple(message)
    
    message_lower = message.lower()
    
    # ردود للعربية
    if language == "ar":
        if any(word in message_lower for word in ["مرحبا", "اهلا", "السلام", "hello", "hi"]):
            return DEFAULT_RESPONSES["ar"]["greeting"]
        elif any(word in message_lower for word in ["مساعدة", "help", "مساعده"]):
            return DEFAULT_RESPONSES["ar"]["help"]
        elif any(word in message_lower for word in ["برمجة", "برمجه", "programming", "كود"]):
            return DEFAULT_RESPONSES["ar"]["programming"]
        else:
            return DEFAULT_RESPONSES["ar"]["default"]
    
    # ردود للإنجليزية
    else:
        if any(word in message_lower for word in ["hello", "hi", "hey"]):
            return DEFAULT_RESPONSES["en"]["greeting"]
        elif any(word in message_lower for word in ["help", "assist", "support"]):
            return DEFAULT_RESPONSES["en"]["help"]
        elif any(word in message_lower for word in ["programming", "code", "python", "java"]):
            return DEFAULT_RESPONSES["en"]["programming"]
        else:
            return DEFAULT_RESPONSES["en"]["default"]

@router.post("/ask", response_model=dict)
async def ask_question_simple(
    message: str,
    conversation_id: str = None,
    language: str = "auto",
    context: str = None
):
    """
    طرح سؤال على BoAI والحصول على إجابة مبسطة
    """
    try:
        if not message:
            raise HTTPException(status_code=400, detail="الرسالة لا يمكن أن تكون فارغة")
        
        # توليد رد مبسط
        response = generate_simple_response(message, language)
        
        # إنشاء معرفات فريدة إذا لم تكن موجودة
        if not conversation_id:
            conversation_id = f"conv_{datetime.now().timestamp()}"
        
        message_id = f"msg_{datetime.now().timestamp()}"
        
        logger.info(f"المحادثة {conversation_id}: تم استقبال سؤال ومعالجته")
        
        return {
            "success": True,
            "response": response,
            "conversation_id": conversation_id,
            "message_id": message_id,
            "timestamp": datetime.now().isoformat(),
            "language": detect_language_simple(response) if language == "auto" else language,
            "model_used": "simple_chat",
            "model_version": "1.0"
        }
        
    except Exception as e:
        logger.error(f"خطأ في معالجة السؤال: {e}")
        raise HTTPException(status_code=500, detail=f"خطأ في المعالجة: {str(e)}")

@router.get("/health", response_model=dict)
async def chat_health_simple():
    """فحص صحة خدمة الدردشة المبسطة"""
    return {
        "status": "healthy",
        "service": "simple_chat",
        "timestamp": datetime.now().isoformat(),
        "message": "خدمة الدردشة المبسطة تعمل بشكل صحيح"
    }

@router.get("/test", response_model=dict)
async def test_chat():
    """نقطة نهاية للاختبار"""
    return {
        "message": "BoAI Chat API is working!",
        "version": "1.0.0",
        "status": "active"
    }
