"""
Chat Router - واجهة برمجة التطبيقات للدردشة مع BoAI

هذا الملف يحتوي على endpoints للدردشة مع النموذج،
بما في ذلك الدردشة العادية والدردشة الحية عبر WebSocket
"""

from fastapi import APIRouter, WebSocket, WebSocketDisconnect, HTTPException, Depends
from fastapi.responses import JSONResponse
from typing import List, Optional
import logging
import json
from datetime import datetime

from src.core.nlp.pipeline import NLPPipeline
from src.core.models.model_manager import ModelManager
from src.core.config import settings

# إعداد التسجيل
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# إنشاء router
router = APIRouter(prefix="/chat", tags=["chat"])

# تهيئة خط أنابيب المعالجة اللغوية
nlp_pipeline = NLPPipeline()

# تهيئة مدير النماذج
model_manager = ModelManager(settings.MODELS_DIR)

class ChatRequest:
    """نموذج طلب الدردشة"""
    def __init__(self, message: str, conversation_id: Optional[str] = None, 
                 language: str = "auto", context: Optional[str] = None):
        self.message = message
        self.conversation_id = conversation_id
        self.language = language
        self.context = context

class ChatResponse:
    """نموذج رد الدردشة"""
    def __init__(self, response: str, conversation_id: str, 
                 message_id: str, timestamp: datetime):
        self.response = response
        self.conversation_id = conversation_id
        self.message_id = message_id
        self.timestamp = timestamp

@router.post("/ask", response_model=dict)
async def ask_question(
    message: str,
    conversation_id: Optional[str] = None,
    language: str = "auto",
    context: Optional[str] = None
):
    """
    طرح سؤال على BoAI والحصول على إجابة
    
    Args:
        message: السؤال أو الرسالة
        conversation_id: معرف المحادثة (اختياري)
        language: لغة المحادثة (auto للكشف التلقائي)
        context: سياق إضافي (اختياري)
    
    Returns:
        dict: الإجابة ومعلومات إضافية
    """
    try:
        # تحميل النموذج الافتراضي إذا لم يكن محملاً
        if not model_manager.get_model(settings.DEFAULT_MODEL):
            model_manager.load_model(settings.DEFAULT_MODEL, settings.DEFAULT_MODEL_VERSION)
        
        # معالجة الرسالة وتوليد الرد
        response = nlp_pipeline.generate_response(
            prompt=message,
            context=context,
            language=language
        )
        
        # إنشاء معرفات فريدة إذا لم تكن موجودة
        if not conversation_id:
            conversation_id = f"conv_{datetime.now().timestamp()}"
        
        message_id = f"msg_{datetime.now().timestamp()}"
        
        # تسجيل المحادثة (سيتم تخزينها في قاعدة البيانات لاحقاً)
        logger.info(f"المحادثة {conversation_id}: تم استقبال سؤال ومعالجته")
        
        return {
            "success": True,
            "response": response,
            "conversation_id": conversation_id,
            "message_id": message_id,
            "timestamp": datetime.now().isoformat(),
            "language": nlp_pipeline.detect_language(response) if language == "auto" else language,
            "model_used": settings.DEFAULT_MODEL,
            "model_version": settings.DEFAULT_MODEL_VERSION
        }
        
    except Exception as e:
        logger.error(f"خطأ في معالجة السؤال: {e}")
        raise HTTPException(status_code=500, detail=f"خطأ في المعالجة: {str(e)}")

@router.websocket("/ws")
async def websocket_chat(websocket: WebSocket):
    """
    دعم الدردشة الحية عبر WebSocket
    
    Args:
        websocket: اتصال WebSocket
    """
    await websocket.accept()
    conversation_id = f"ws_conv_{datetime.now().timestamp()}"
    
    try:
        while True:
            # استقبال البيانات من العميل
            data = await websocket.receive_text()
            message_data = json.loads(data)
            
            message = message_data.get("message", "")
            language = message_data.get("language", "auto")
            context = message_data.get("context", None)
            
            if not message:
                await websocket.send_json({
                    "error": "الرسالة فارغة",
                    "type": "error"
                })
                continue
            
            # معالجة الرسالة
            response = nlp_pipeline.generate_response(
                prompt=message,
                context=context,
                language=language
            )
            
            # إرسال الرد
            await websocket.send_json({
                "type": "response",
                "response": response,
                "conversation_id": conversation_id,
                "timestamp": datetime.now().isoformat(),
                "language": language
            })
            
    except WebSocketDisconnect:
        logger.info(f"تم قطع اتصال WebSocket للمحادثة {conversation_id}")
    except Exception as e:
        logger.error(f"خطأ في WebSocket: {e}")
        await websocket.send_json({
            "error": f"خطأ في المعالجة: {str(e)}",
            "type": "error"
        })

@router.get("/conversations", response_model=dict)
async def get_conversations(limit: int = 10, offset: int = 0):
    """
    الحصول على قائمة بالمحادثات (وهمي حالياً - سيتم ربطه بقاعدة البيانات)
    
    Args:
        limit: عدد المحادثات
        offset: الإزاحة للتصفح
    
    Returns:
        dict: قائمة المحادثات
    """
    # هذه دالة وهمية - سيتم استبدالها ببيانات حقيقية من قاعدة البيانات
    conversations = [
        {
            "id": f"conv_{i}",
            "title": f"محادثة نموذجية {i}",
            "message_count": 5,
            "created_at": "2025-08-24T10:00:00Z",
            "updated_at": "2025-08-24T10:05:00Z"
        }
        for i in range(offset, offset + min(limit, 5))
    ]
    
    return {
        "success": True,
        "conversations": conversations,
        "total_count": 25,  # رقم وهمي
        "limit": limit,
        "offset": offset
    }

@router.get("/conversations/{conversation_id}", response_model=dict)
async def get_conversation(conversation_id: str):
    """
    الحصول على محادثة محددة (وهمي حالياً)
    
    Args:
        conversation_id: معرف المحادثة
    
    Returns:
        dict: تفاصيل المحادثة
    """
    # هذه دالة وهمية - سيتم استبدالها ببيانات حقيقية
    return {
        "success": True,
        "conversation": {
            "id": conversation_id,
            "title": "محادثة حول تعلم البرمجة",
            "messages": [
                {
                    "id": "msg_1",
                    "sender": "user",
                    "content": "كيف أبدأ في تعلم Python؟",
                    "timestamp": "2025-08-24T10:00:00Z"
                },
                {
                    "id": "msg_2", 
                    "sender": "assistant",
                    "content": "يمكنك البدء بتركيب Python ثم تعلم الأساسيات مثل المتغيرات، الجمل الشرطية، والحلقات.",
                    "timestamp": "2025-08-24T10:00:05Z"
                }
            ],
            "created_at": "2025-08-24T10:00:00Z",
            "updated_at": "2025-08-24T10:05:00Z"
        }
    }

@router.delete("/conversations/{conversation_id}", response_model=dict)
async def delete_conversation(conversation_id: str):
    """
    حذف محادثة (وهمي حالياً)
    
    Args:
        conversation_id: معرف المحادثة
    
    Returns:
        dict: نتيجة العملية
    """
    # هذه دالة وهمية - سيتم تنفيذ الحذف الفعلي لاحقاً
    logger.info(f"تم طلب حذف المحادثة {conversation_id} (وهمي)")
    
    return {
        "success": True,
        "message": f"تم حذف المحادثة {conversation_id}",
        "deleted_id": conversation_id
    }

# endpoint للصحة
@router.get("/health", response_model=dict)
async def chat_health():
    """فحص صحة خدمة الدردشة"""
    return {
        "status": "healthy",
        "service": "chat",
        "timestamp": datetime.now().isoformat(),
        "model_loaded": model_manager.get_model(settings.DEFAULT_MODEL) is not None
    }
