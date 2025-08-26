"""
خدمة إدارة المحادثات والرسائل

هذا الملف يحتوي على دوال لإدارة المحادثات والرسائل في قاعدة البيانات
"""

from typing import List, Optional, Dict, Any
from datetime import datetime
import logging
from sqlalchemy.orm import Session

from src.core.database.models import Conversation, Message, User
from src.core.database.session import get_db_session

# إعداد التسجيل
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ConversationService:
    """خدمة إدارة المحادثات"""
    
    @staticmethod
    def create_conversation(
        user_id: Optional[str] = None,
        title: Optional[str] = None,
        language: str = "auto"
    ) -> Conversation:
        """
        إنشاء محادثة جديدة
        
        Args:
            user_id: معرف المستخدم (اختياري)
            title: عنوان المحادثة (اختياري)
            language: لغة المحادثة
            
        Returns:
            Conversation: المحادثة المنشأة
        """
        db = get_db_session()
        try:
            conversation = Conversation(
                user_id=user_id,
                title=title,
                language=language
            )
            
            db.add(conversation)
            db.commit()
            db.refresh(conversation)
            
            logger.info(f"تم إنشاء محادثة جديدة: {conversation.id}")
            return conversation
            
        except Exception as e:
            db.rollback()
            logger.error(f"خطأ في إنشاء المحادثة: {e}")
            raise
        finally:
            db.close()
    
    @staticmethod
    def get_conversation(conversation_id: str) -> Optional[Conversation]:
        """
        الحصول على محادثة بواسطة المعرف
        
        Args:
            conversation_id: معرف المحادثة
            
        Returns:
            Optional[Conversation]: المحادثة إذا وجدت، None إذا لم توجد
        """
        db = get_db_session()
        try:
            conversation = db.query(Conversation).filter(Conversation.id == conversation_id).first()
            return conversation
        except Exception as e:
            logger.error(f"خطأ في الحصول على المحادثة {conversation_id}: {e}")
            return None
        finally:
            db.close()
    
    @staticmethod
    def get_user_conversations(
        user_id: str,
        limit: int = 10,
        offset: int = 0,
        archived: bool = False
    ) -> List[Conversation]:
        """
        الحصول على محادثات المستخدم
        
        Args:
            user_id: معرف المستخدم
            limit: عدد المحادثات
            offset: الإزاحة
            archived: تضمين المحادثات المؤرشفة
            
        Returns:
            List[Conversation]: قائمة المحادثات
        """
        db = get_db_session()
        try:
            query = db.query(Conversation).filter(Conversation.user_id == user_id)
            
            if not archived:
                query = query.filter(Conversation.is_archived == False)
            
            conversations = query.order_by(Conversation.updated_at.desc())\
                                .offset(offset)\
                                .limit(limit)\
                                .all()
            
            return conversations
        except Exception as e:
            logger.error(f"خطأ في الحصول على محادثات المستخدم {user_id}: {e}")
            return []
        finally:
            db.close()
    
    @staticmethod
    def update_conversation(
        conversation_id: str,
        title: Optional[str] = None,
        language: Optional[str] = None,
        is_archived: Optional[bool] = None
    ) -> Optional[Conversation]:
        """
        تحديث المحادثة
        
        Args:
            conversation_id: معرف المحادثة
            title: العنوان الجديد (اختياري)
            language: اللغة الجديدة (اختياري)
            is_archived: حالة الأرشفة (اختياري)
            
        Returns:
            Optional[Conversation]: المحادثة المحدثة
        """
        db = get_db_session()
        try:
            conversation = db.query(Conversation).filter(Conversation.id == conversation_id).first()
            if not conversation:
                return None
            
            if title is not None:
                conversation.title = title
            if language is not None:
                conversation.language = language
            if is_archived is not None:
                conversation.is_archived = is_archived
            
            conversation.updated_at = datetime.utcnow()
            
            db.commit()
            db.refresh(conversation)
            
            logger.info(f"تم تحديث المحادثة: {conversation_id}")
            return conversation
            
        except Exception as e:
            db.rollback()
            logger.error(f"خطأ في تحديث المحادثة {conversation_id}: {e}")
            return None
        finally:
            db.close()
    
    @staticmethod
    def delete_conversation(conversation_id: str) -> bool:
        """
        حذف المحادثة
        
        Args:
            conversation_id: معرف المحادثة
            
        Returns:
            bool: True إذا تم الحذف بنجاح، False إذا فشل
        """
        db = get_db_session()
        try:
            conversation = db.query(Conversation).filter(Conversation.id == conversation_id).first()
            if not conversation:
                return False
            
            db.delete(conversation)
            db.commit()
            
            logger.info(f"تم حذف المحادثة: {conversation_id}")
            return True
            
        except Exception as e:
            db.rollback()
            logger.error(f"خطأ في حذف المحادثة {conversation_id}: {e}")
            return False
        finally:
            db.close()

class MessageService:
    """خدمة إدارة الرسائل"""
    
    @staticmethod
    def create_message(
        conversation_id: str,
        sender: str,
        content: str,
        language: str = "auto",
        metadata: Optional[Dict[str, Any]] = None
    ) -> Optional[Message]:
        """
        إنشاء رسالة جديدة
        
        Args:
            conversation_id: معرف المحادثة
            sender: المرسل (user أو assistant)
            content: محتوى الرسالة
            language: لغة الرسالة
            metadata: بيانات إضافية
            
        Returns:
            Optional[Message]: الرسالة المنشأة
        """
        db = get_db_session()
        try:
            # التحقق من وجود المحادثة
            conversation = db.query(Conversation).filter(Conversation.id == conversation_id).first()
            if not conversation:
                return None
            
            message = Message(
                conversation_id=conversation_id,
                sender=sender,
                content=content,
                language=language,
                metadata=metadata or {}
            )
            
            db.add(message)
            
            # تحديث وقت تحديث المحادثة
            conversation.updated_at = datetime.utcnow()
            
            db.commit()
            db.refresh(message)
            
            logger.info(f"تم إنشاء رسالة جديدة في المحادثة {conversation_id}")
            return message
            
        except Exception as e:
            db.rollback()
            logger.error(f"خطأ في إنشاء الرسالة: {e}")
            return None
        finally:
            db.close()
    
    @staticmethod
    def get_conversation_messages(
        conversation_id: str,
        limit: int = 50,
        offset: int = 0
    ) -> List[Message]:
        """
        الحصول على رسائل المحادثة
        
        Args:
            conversation_id: معرف المحادثة
            limit: عدد الرسائل
            offset: الإزاحة
            
        Returns:
            List[Message]: قائمة الرسائل
        """
        db = get_db_session()
        try:
            messages = db.query(Message)\
                        .filter(Message.conversation_id == conversation_id)\
                        .order_by(Message.created_at.asc())\
                        .offset(offset)\
                        .limit(limit)\
                        .all()
            
            return messages
        except Exception as e:
            logger.error(f"خطأ في الحصول على رسائل المحادثة {conversation_id}: {e}")
            return []
        finally:
            db.close()
    
    @staticmethod
    def get_message(message_id: str) -> Optional[Message]:
        """
        الحصول على رسالة بواسطة المعرف
        
        Args:
            message_id: معرف الرسالة
            
        Returns:
            Optional[Message]: الرسالة إذا وجدت، None إذا لم توجد
        """
        db = get_db_session()
        try:
            message = db.query(Message).filter(Message.id == message_id).first()
            return message
        except Exception as e:
            logger.error(f"خطأ في الحصول على الرسالة {message_id}: {e}")
            return None
        finally:
            db.close()
