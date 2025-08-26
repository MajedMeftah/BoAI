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
from src.core.services.conversation_service import ConversationService, MessageService

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
        
        # TODO: الحصول على معرف المستخدم من المصادقة
        user_id = "test_user_id"
        
        # إنشاء محادثة جديدة إذا لم تكن موجودة
        if not conversation_id:
            conversation = ConversationService.create_conversation(
                user_id=user_id,
                title=f"محادثة حول: {message[:30]}..." if len(message) > 30 else message,
                language=language
            )
            conversation_id = conversation.id
        else:
            # التحقق من وجود المحادثة
            conversation = ConversationService.get_conversation(conversation_id)
            if not conversation:
                raise HTTPException(status_code=404, detail="المحادثة غير موجودة")
        
        # حفظ رسالة المستخدم في قاعدة البيانات
        user_message = MessageService.create_message(
            conversation_id=conversation_id,
            sender="user",
            content=message,
            language=language,
            metadata={
                "model_used": settings.DEFAULT_MODEL,
                "model_version": settings.DEFAULT_MODEL_VERSION,
                "context": context
            }
        )
        
        # حفظ رد المساعد في قاعدة البيانات
        assistant_message = MessageService.create_message(
            conversation_id=conversation_id,
            sender="assistant",
            content=response,
            language=nlp_pipeline.detect_language(response) if language == "auto" else language,
            metadata={
                "model_used": settings.DEFAULT_MODEL,
                "model_version": settings.DEFAULT_MODEL_VERSION,
                "context_used": context is not None
            }
        )
        
        if not user_message or not assistant_message:
            raise HTTPException(status_code=500, detail="خطأ في حفظ المحادثة")
        
        logger.info(f"المحادثة {conversation_id}: تم حفظ الرسائل في قاعدة البيانات")
        
        return {
            "success": True,
            "response": response,
            "conversation_id": conversation_id,
            "message_id": assistant_message.id,
            "timestamp": datetime.now().isoformat(),
            "language": nlp_pipeline.detect_language(response) if language == "auto" else language,
            "model_used": settings.DEFAULT_MODEL,
            "model_version": settings.DEFAULT_MODEL_VERSION
        }
        
    except HTTPException:
        raise
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
    
    # TODO: الحصول على معرف المستخدم من المصادقة
    user_id = "test_user_id"
    
    # إنشاء محادثة جديدة للويب سوكيت
    conversation = ConversationService.create_conversation(
        user_id=user_id,
        title="محادثة ويب سوكيت",
        language="auto"
    )
    conversation_id = conversation.id
    
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
            
            # حفظ رسالة المستخدم في قاعدة البيانات
            user_message = MessageService.create_message(
                conversation_id=conversation_id,
                sender="user",
                content=message,
                language=language,
                metadata={
                    "model_used": settings.DEFAULT_MODEL,
                    "model_version": settings.DEFAULT_MODEL_VERSION,
                    "context": context
                }
            )
            
            if not user_message:
                await websocket.send_json({
                    "error": "خطأ في حفظ الرسالة",
                    "type": "error"
                })
                continue
            
            # معالجة الرسالة
            response = nlp_pipeline.generate_response(
                prompt=message,
                context=context,
                language=language
            )
            
            # حفظ رد المساعد في قاعدة البيانات
            assistant_message = MessageService.create_message(
                conversation_id=conversation_id,
                sender="assistant",
                content=response,
                language=nlp_pipeline.detect_language(response) if language == "auto" else language,
                metadata={
                    "model_used": settings.DEFAULT_MODEL,
                    "model_version": settings.DEFAULT_MODEL_VERSION,
                    "context_used": context is not None
                }
            )
            
            # إرسال الرد
            await websocket.send_json({
                "type": "response",
                "response": response,
                "conversation_id": conversation_id,
                "message_id": assistant_message.id if assistant_message else None,
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
    الحصول على قائمة بالمحادثات
    
    Args:
        limit: عدد المحادثات
        offset: الإزاحة للتصفح
    
    Returns:
        dict: قائمة المحادثات
    """
    try:
        # TODO: الحصول على معرف المستخدم من المصادقة
        # حالياً نستخدم مستخدم وهمي للاختبار
        user_id = "test_user_id"
        
        # الحصول على محادثات المستخدم
        conversations = ConversationService.get_user_conversations(
            user_id=user_id,
            limit=limit,
            offset=offset
        )
        
        # تحويل المحادثات إلى تنسيق JSON
        conversations_data = []
        for conv in conversations:
            # الحصول على عدد الرسائل
            messages = MessageService.get_conversation_messages(conv.id)
            
            conversations_data.append({
                "id": conv.id,
                "title": conv.title or f"محادثة {conv.id[:8]}",
                "message_count": len(messages),
                "language": conv.language,
                "created_at": conv.created_at.isoformat(),
                "updated_at": conv.updated_at.isoformat(),
                "is_archived": conv.is_archived
            })
        
        # TODO: حساب العدد الإجمالي الحقيقي
        total_count = len(conversations_data) + offset
        
        return {
            "success": True,
            "conversations": conversations_data,
            "total_count": total_count,
            "limit": limit,
            "offset": offset
        }
        
    except Exception as e:
        logger.error(f"خطأ في الحصول على المحادثات: {e}")
        raise HTTPException(status_code=500, detail=f"خطأ في الحصول على المحادثات: {str(e)}")

@router.get("/conversations/{conversation_id}", response_model=dict)
async def get_conversation(conversation_id: str):
    """
    الحصول على محادثة محددة
    
    Args:
        conversation_id: معرف المحادثة
    
    Returns:
        dict: تفاصيل المحادثة
    """
    try:
        # الحصول على المحادثة من قاعدة البيانات
        conversation = ConversationService.get_conversation(conversation_id)
        if not conversation:
            raise HTTPException(status_code=404, detail="المحادثة غير موجودة")
        
        # الحصول على رسائل المحادثة
        messages = MessageService.get_conversation_messages(conversation_id)
        
        # تحويل الرسائل إلى تنسيق JSON
        messages_data = []
        for msg in messages:
            messages_data.append({
                "id": msg.id,
                "sender": msg.sender,
                "content": msg.content,
                "language": msg.language,
                "timestamp": msg.created_at.isoformat(),
                "metadata": msg.metadata
            })
        
        return {
            "success": True,
            "conversation": {
                "id": conversation.id,
                "title": conversation.title or f"محادثة {conversation.id[:8]}",
                "language": conversation.language,
                "message_count": len(messages),
                "messages": messages_data,
                "created_at": conversation.created_at.isoformat(),
                "updated_at": conversation.updated_at.isoformat(),
                "is_archived": conversation.is_archived
            }
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"خطأ في الحصول على المحادثة {conversation_id}: {e}")
        raise HTTPException(status_code=500, detail=f"خطأ في الحصول على المحادثة: {str(e)}")

@router.delete("/conversations/{conversation_id}", response_model=dict)
async def delete_conversation(conversation_id: str):
    """
    حذف محادثة
    
    Args:
        conversation_id: معرف المحادثة
    
    Returns:
        dict: نتيجة العملية
    """
    try:
        # حذف المحادثة من قاعدة البيانات
        success = ConversationService.delete_conversation(conversation_id)
        
        if not success:
            raise HTTPException(status_code=404, detail="المحادثة غير موجودة")
        
        logger.info(f"تم حذف المحادثة: {conversation_id}")
        
        return {
            "success": True,
            "message": f"تم حذف المحادثة {conversation_id}",
            "deleted_id": conversation_id
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"خطأ في حذف المحادثة {conversation_id}: {e}")
        raise HTTPException(status_code=500, detail=f"خطأ في حذف المحادثة: {str(e)}")

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
