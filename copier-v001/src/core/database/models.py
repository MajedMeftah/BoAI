"""
نماذج قاعدة البيانات لـ BoAI

هذا الملف يحتوي على نماذج SQLAlchemy للبيانات الأساسية
"""

from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, ForeignKey, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid

Base = declarative_base()

def generate_uuid():
    """توليد معرف فريد عالمي"""
    return str(uuid.uuid4())

class User(Base):
    """نموذج المستخدم"""
    __tablename__ = "users"

    id = Column(String, primary_key=True, default=generate_uuid)
    email = Column(String, unique=True, nullable=False, index=True)
    hashed_password = Column(String, nullable=False)
    full_name = Column(String, nullable=True)
    role = Column(String, default="user")  # user, admin, tutor
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # العلاقات
    conversations = relationship("Conversation", back_populates="user", cascade="all, delete-orphan")

class Conversation(Base):
    """نموذج المحادثة"""
    __tablename__ = "conversations"

    id = Column(String, primary_key=True, default=generate_uuid)
    user_id = Column(String, ForeignKey("users.id"), nullable=True)  # يمكن أن تكون محادثة بدون مستخدم
    title = Column(String, nullable=True)
    language = Column(String, default="auto")
    is_archived = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # العلاقات
    user = relationship("User", back_populates="conversations")
    messages = relationship("Message", back_populates="conversation", cascade="all, delete-orphan")

class Message(Base):
    """نموذج الرسالة"""
    __tablename__ = "messages"

    id = Column(String, primary_key=True, default=generate_uuid)
    conversation_id = Column(String, ForeignKey("conversations.id"), nullable=False)
    sender = Column(String, nullable=False)  # user أو assistant
    content = Column(Text, nullable=False)
    language = Column(String, default="auto")
    message_metadata = Column(JSON, default=dict)  # بيانات إضافية مثل model_used, tokens, etc.
    created_at = Column(DateTime, default=datetime.utcnow)

    # العلاقات
    conversation = relationship("Conversation", back_populates="messages")

class Feedback(Base):
    """نموذج التقييم"""
    __tablename__ = "feedback"

    id = Column(String, primary_key=True, default=generate_uuid)
    message_id = Column(String, ForeignKey("messages.id"), nullable=False)
    rating = Column(Integer, nullable=False)  # 1-5
    comment = Column(Text, nullable=True)
    user_id = Column(String, ForeignKey("users.id"), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    # العلاقات
    message = relationship("Message")
    user = relationship("User")

class SystemSettings(Base):
    """نموذج إعدادات النظام"""
    __tablename__ = "system_settings"

    id = Column(String, primary_key=True, default=generate_uuid)
    key = Column(String, unique=True, nullable=False, index=True)
    value = Column(JSON, nullable=False)
    description = Column(Text, nullable=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
