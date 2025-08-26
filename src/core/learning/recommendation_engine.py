"""
محرك التوصيات الذكية - نظام توليد توصيات تعلم مخصصة

هذا الملف يحتوي على النظام الأساسي لتوليد توصيات تعلم ذكية
بناءً على تحليل سلوك المستخدم وتفضيلاته التعليمية
"""

import logging
from typing import Dict, List, Optional, Any
import json
from datetime import datetime
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import sqlalchemy as sa
from sqlalchemy.orm import Session

from src.core.database.session import get_db
from src.core.database.models import User, Conversation, Message, Feedback
from src.core.utils.cache import cache_manager

# إعداد التسجيل
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class RecommendationEngine:
    """
    محرك التوصيات الذكية - توليد توصيات تعلم مخصصة
    """
    
    def __init__(self):
        """
        تهيئة محرك التوصيات
        """
        self.vectorizer = TfidfVectorizer(
            max_features=1000,
            stop_words=None,  # سندعم تعدد اللغات لاحقاً
            ngram_range=(1, 2)
        )
        self.user_profiles = {}
        self.content_db = self._load_content_database()
        self.cache = cache_manager
        
        logger.info("تم تهيئة RecommendationEngine بنجاح")
    
    def _load_content_database(self) -> List[Dict]:
        """
        تحميل قاعدة بيانات المحتوى التعليمي
        """
        # سيتم تحميل هذا من قاعدة البيانات الفعلية لاحقاً
        return [
            {
                "id": 1,
                "title": "مقدمة في البرمجة بلغة Python",
                "description": "تعلم أساسيات البرمجة باستخدام Python",
                "difficulty": "مبتدئ",
                "tags": ["python", "برمجة", "مبتدئ"],
                "language": "ar",
                "estimated_time": 120,
                "prerequisites": []
            },
            {
                "id": 2,
                "title": "هياكل البيانات في Python",
                "description": "تعلم القوائم، القواميس، والمجموعات في Python",
                "difficulty": "متوسط",
                "tags": ["python", "هياكل بيانات", "متوسط"],
                "language": "ar",
                "estimated_time": 180,
                "prerequisites": ["python"]
            },
            {
                "id": 3,
                "title": "البرمجة الكائنية في Python",
                "description": "تعلم مفاهيم OOP في Python",
                "difficulty": "متوسط",
                "tags": ["python", "oop", "كائنية"],
                "language": "ar",
                "estimated_time": 240,
                "prerequisites": ["python", "هياكل بيانات"]
            }
        ]
    
    def analyze_user_behavior(self, user_id: str) -> Dict[str, Any]:
        """
        تحليل سلوك المستخدم وتفضيلاته التعليمية
        
        Args:
            user_id: معرف المستخدم
            
        Returns:
            Dict: ملف تعريف المستخدم مع التفضيلات والأنماط
        """
        try:
            db = next(get_db())
            
            # جمع بيانات المستخدم
            user = db.query(User).filter(User.id == user_id).first()
            if not user:
                return self._create_default_profile(user_id)
            
            # تحليل المحادثات السابقة
            conversations = db.query(Conversation).filter(
                Conversation.user_id == user_id
            ).all()
            
            # تحليل التقييمات
            feedbacks = db.query(Feedback).filter(
                Feedback.user_id == user_id
            ).all()
            
            profile = {
                "user_id": user_id,
                "preferred_language": user.preferred_language or "ar",
                "learning_style": self._detect_learning_style(conversations),
                "knowledge_gaps": self._identify_knowledge_gaps(conversations, feedbacks),
                "strengths": self._identify_strengths(conversations, feedbacks),
                "preferred_topics": self._extract_preferred_topics(conversations),
                "learning_pace": self._calculate_learning_pace(conversations),
                "last_analysis": datetime.now().isoformat()
            }
            
            self.user_profiles[user_id] = profile
            return profile
            
        except Exception as e:
            logger.error(f"خطأ في تحليل سلوك المستخدم {user_id}: {e}")
            return self._create_default_profile(user_id)
    
    def _detect_learning_style(self, conversations: List[Conversation]) -> str:
        """
        كشف نمط التعلم للمستخدم
        """
        # تحليل بسيط لأنماط المحادثة
        # يمكن تطوير هذا لاحقاً باستخدام ML متقدم
        return "متوازن"  # سيعود هذا لاحقاً بأنماط حقيقية
    
    def _identify_knowledge_gaps(self, conversations: List[Conversation], 
                               feedbacks: List[Feedback]) -> List[str]:
        """
        تحديد الفجوات المعرفية للمستخدم
        """
        gaps = []
        
        # تحليل الأسئلة التي لم يتم الإجابة عليها بشكل جيد
        for feedback in feedbacks:
            if feedback.rating and feedback.rating < 3:
                # إضافة الموضوع إلى الفجوات المعرفية
                gaps.append(feedback.message.topic or "عام")
        
        return list(set(gaps))
    
    def _identify_strengths(self, conversations: List[Conversation],
                          feedbacks: List[Feedback]) -> List[str]:
        """
        تحديد نقاط القوة للمستخدم
        """
        strengths = []
        
        # تحليل الأسئلة التي تمت الإجابة عليها بشكل جيد
        for feedback in feedbacks:
            if feedback.rating and feedback.rating >= 4:
                strengths.append(feedback.message.topic or "عام")
        
        return list(set(strengths))
    
    def _extract_preferred_topics(self, conversations: List[Conversation]) -> List[str]:
        """
        استخراج المواضيع المفضلة للمستخدم
        """
        topics = []
        
        for conv in conversations:
            if conv.topic and conv.topic not in topics:
                topics.append(conv.topic)
        
        return topics
    
    def _calculate_learning_pace(self, conversations: List[Conversation]) -> str:
        """
        حساب سرعة التعلم للمستخدم
        """
        if not conversations:
            return "متوسط"
        
        # تحليل تردد المحادثات ومدة الجلسات
        return "متوسط"  # سيعود هذا لاحقاً بتحليل حقيقي
    
    def _create_default_profile(self, user_id: str) -> Dict[str, Any]:
        """
        إنشاء ملف تعريف افتراضي للمستخدم
        """
        return {
            "user_id": user_id,
            "preferred_language": "ar",
            "learning_style": "متوازن",
            "knowledge_gaps": [],
            "strengths": [],
            "preferred_topics": ["برمجة", "python"],
            "learning_pace": "متوسط",
            "last_analysis": datetime.now().isoformat()
        }
    
    def generate_recommendations(self, user_id: str, max_recommendations: int = 5) -> List[Dict]:
        """
        توليد توصيات تعلم مخصصة للمستخدم
        
        Args:
            user_id: معرف المستخدم
            max_recommendations: الحد الأقصى للتوصيات
            
        Returns:
            List[Dict]: قائمة بالتوصيات المخصصة
        """
        try:
            # تحميل أو إنشاء ملف تعريف المستخدم
            if user_id not in self.user_profiles:
                self.analyze_user_behavior(user_id)
            
            user_profile = self.user_profiles[user_id]
            
            # تطبيق خوارزميات التوصيات
            recommendations = []
            
            # 1. التوصيات بناءً على الفجوات المعرفية
            if user_profile["knowledge_gaps"]:
                gap_recommendations = self._recommend_for_gaps(
                    user_profile["knowledge_gaps"],
                    max_recommendations // 2
                )
                recommendations.extend(gap_recommendations)
            
            # 2. التوصيات بناءً على المواضيع المفضلة
            topic_recommendations = self._recommend_for_topics(
                user_profile["preferred_topics"],
                max_recommendations - len(recommendations)
            )
            recommendations.extend(topic_recommendations)
            
            # 3. إذا لم تكن هناك توصيات كافية، إضافة توصيات شائعة
            if len(recommendations) < max_recommendations:
                popular_recommendations = self._recommend_popular(
                    max_recommendations - len(recommendations)
                )
                recommendations.extend(popular_recommendations)
            
            # إزالة التكرارات وترتيب التوصيات
            unique_recommendations = self._remove_duplicates(recommendations)
            sorted_recommendations = self._sort_recommendations(
                unique_recommendations, 
                user_profile
            )
            
            return sorted_recommendations[:max_recommendations]
            
        except Exception as e:
            logger.error(f"خطأ في توليد التوصيات للمستخدم {user_id}: {e}")
            return self._get_fallback_recommendations(max_recommendations)
    
    def _recommend_for_gaps(self, knowledge_gaps: List[str], count: int) -> List[Dict]:
        """
        توليد توصيات لسد الفجوات المعرفية
        """
        recommendations = []
        
        for gap in knowledge_gaps:
            for content in self.content_db:
                if (gap.lower() in [tag.lower() for tag in content.get("tags", [])] or
                    gap.lower() in content.get("title", "").lower() or
                    gap.lower() in content.get("description", "").lower()):
                    
                    if content not in recommendations:
                        recommendations.append(content)
                    
                    if len(recommendations) >= count:
                        return recommendations
        
        return recommendations
    
    def _recommend_for_topics(self, preferred_topics: List[str], count: int) -> List[Dict]:
        """
        توليد توصيات بناءً على المواضيع المفضلة
        """
        recommendations = []
        
        for topic in preferred_topics:
            for content in self.content_db:
                if (topic.lower() in [tag.lower() for tag in content.get("tags", [])] or
                    topic.lower() in content.get("title", "").lower() or
                    topic.lower() in content.get("description", "").lower()):
                    
                    if content not in recommendations:
                        recommendations.append(content)
                    
                    if len(recommendations) >= count:
                        return recommendations
        
        return recommendations
    
    def _recommend_popular(self, count: int) -> List[Dict]:
        """
        توليد توصيات شائعة (سيتم تحسين هذا لاحقاً)
        """
        return self.content_db[:count]
    
    def _remove_duplicates(self, recommendations: List[Dict]) -> List[Dict]:
        """
        إزالة التوصيات المكررة
        """
        seen_ids = set()
        unique_recommendations = []
        
        for rec in recommendations:
            if rec["id"] not in seen_ids:
                seen_ids.add(rec["id"])
                unique_recommendations.append(rec)
        
        return unique_recommendations
    
    def _sort_recommendations(self, recommendations: List[Dict], 
                            user_profile: Dict) -> List[Dict]:
        """
        ترتيب التوصيات حسب ملاءمتها للمستخدم
        """
        # ترتيب بسيط حالياً (سيتم تحسينه لاحقاً)
        return sorted(recommendations, key=lambda x: x.get("id", 0))
    
    def _get_fallback_recommendations(self, count: int) -> List[Dict]:
        """
        الحصول على توصيات افتراضية في حالة الخطأ
        """
        return self.content_db[:count]
    
    def update_user_feedback(self, user_id: str, content_id: int, 
                           rating: int, feedback_text: str = None):
        """
        تحديث التوصيات بناءً على تغذية راجعة جديدة
        
        Args:
            user_id: معرف المستخدم
            content_id: معرف المحتوى
            rating: التقييم (1-5)
            feedback_text: نص التغذية الراجعة (اختياري)
        """
        try:
            if user_id in self.user_profiles:
                # تحديث ملف المستخدم بناءً على التغذية الراجعة
                profile = self.user_profiles[user_id]
                
                if rating < 3:
                    # إضافة إلى الفجوات المعرفية
                    content = next((c for c in self.content_db if c["id"] == content_id), None)
                    if content:
                        topic = content.get("tags", [""])[0] if content.get("tags") else "عام"
                        if topic not in profile["knowledge_gaps"]:
                            profile["knowledge_gaps"].append(topic)
                
                elif rating >= 4:
                    # إضافة إلى نقاط القوة
                    content = next((c for c in self.content_db if c["id"] == content_id), None)
                    if content:
                        topic = content.get("tags", [""])[0] if content.get("tags") else "عام"
                        if topic not in profile["strengths"]:
                            profile["strengths"].append(topic)
                
                profile["last_analysis"] = datetime.now().isoformat()
                
        except Exception as e:
            logger.error(f"خطأ في تحديث التغذية الراجعة للمستخدم {user_id}: {e}")
    
    def get_learning_path(self, user_id: str, goal: str) -> List[Dict]:
        """
        إنشاء مسار تعلم مخصص لهدف معين
        
        Args:
            user_id: معرف المستخدم
            goal: الهدف التعليمي
            
        Returns:
            List[Dict]: مسار التعلم المكون من خطوات متسلسلة
        """
        try:
            if user_id not in self.user_profiles:
                self.analyze_user_behavior(user_id)
            
            user_profile = self.user_profiles[user_id]
            
            # إنشاء مسار تعلم بسيط (سيتم تطويره لاحقاً)
            learning_path = []
            
            # إضافة محتوى مناسب للمستوى الحالي
            beginner_content = [c for c in self.content_db 
                              if c.get("difficulty") == "مبتدئ"]
            learning_path.extend(beginner_content[:2])
            
            # إضافة محتوى متوسط إذا كان المستخدم جاهزاً
            if not user_profile["knowledge_gaps"]:
                intermediate_content = [c for c in self.content_db 
                                      if c.get("difficulty") == "متوسط"]
                learning_path.extend(intermediate_content[:2])
            
            return learning_path
            
        except Exception as e:
            logger.error(f"خطأ في إنشاء مسار التعلم للمستخدم {user_id}: {e}")
            return self._get_fallback_recommendations(3)

# إنشاء instance عام للمحرك
recommendation_engine = RecommendationEngine()

# مثال للاستخدام
if __name__ == "__main__":
    # اختبار المحرك
    user_id = "test-user-123"
    
    # تحليل سلوك المستخدم
    profile = recommendation_engine.analyze_user_behavior(user_id)
    print("ملف تعريف المستخدم:")
    print(json.dumps(profile, ensure_ascii=False, indent=2))
    
    # توليد التوصيات
    recommendations = recommendation_engine.generate_recommendations(user_id, 3)
    print("\nالتوصيات المخصصة:")
    for i, rec in enumerate(recommendations, 1):
        print(f"{i}. {rec['title']} - {rec['difficulty']}")
    
    # تحديث بناءً على تغذية راجعة
    recommendation_engine.update_user_feedback(user_id, 1, 4, "محتوى رائع!")
    
    # إنشاء مسار تعلم
    learning_path = recommendation_engine.get_learning_path(user_id, "تعلم Python")
    print("\nمسار التعلم المقترح:")
    for i, step in enumerate(learning_path, 1):
        print(f"{i}. {step['title']}")
