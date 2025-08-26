#!/usr/bin/env python3
"""
اختبار نظام التوصيات الذكية - تأكد من عمل النظام بشكل صحيح
"""

import sys
import os

# إضافة مسار src إلى sys.path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from fastapi.testclient import TestClient
from src.api.main import app
from src.core.learning.recommendation_engine import RecommendationEngine

def test_recommendation_engine():
    """اختبار محرك التوصيات مباشرة"""
    print("🔍 اختبار محرك التوصيات مباشرة...")
    
    try:
        # إنشاء instance من المحرك
        engine = RecommendationEngine()
        print("✅ تم تهيئة محرك التوصيات بنجاح")
        
        # تحليل سلوك مستخدم افتراضي
        user_id = "test-user-001"
        profile = engine.analyze_user_behavior(user_id)
        print(f"✅ تم تحليل ملف تعريف المستخدم: {user_id}")
        print(f"   - اللغة المفضلة: {profile['preferred_language']}")
        print(f"   - نمط التعلم: {profile['learning_style']}")
        print(f"   - سرعة التعلم: {profile['learning_pace']}")
        
        # توليد التوصيات
        recommendations = engine.generate_recommendations(user_id, 3)
        print(f"✅ تم توليد {len(recommendations)} توصية")
        
        for i, rec in enumerate(recommendations, 1):
            print(f"   {i}. {rec['title']} ({rec['difficulty']})")
        
        # تحديث بناءً على تغذية راجعة
        engine.update_user_feedback(user_id, 1, 4, "محتوى رائع!")
        print("✅ تم تحديث التغذية الراجعة بنجاح")
        
        # إنشاء مسار تعلم
        learning_path = engine.get_learning_path(user_id, "تعلم البرمجة")
        print(f"✅ تم إنشاء مسار تعلم مكون من {len(learning_path)} خطوة")
        
        return True
        
    except Exception as e:
        print(f"❌ فشل اختبار محرك التوصيات: {e}")
        return False

def test_recommendations_api():
    """اختبار واجهة برمجة التطبيقات للتوصيات"""
    print("\n🔍 اختبار واجهة برمجة التطبيقات للتوصيات...")
    
    try:
        client = TestClient(app)
        
        # فحص صحة النظام
        response = client.get("/api/v1/recommendations/health")
        assert response.status_code == 200
        print("✅ فحص صحة النظام يعمل")
        
        # الحصول على المحتويات المتاحة
        response = client.get("/api/v1/recommendations/content")
        assert response.status_code == 200
        content = response.json()
        print(f"✅ تم جلب {len(content)} محتوى تعليمي")
        
        # اختبار الحصول على محتوى محدد
        if content:
            content_id = content[0]["id"]
            response = client.get(f"/api/v1/recommendations/content/{content_id}")
            assert response.status_code == 200
            print(f"✅ تم جلب المحتوى {content_id} بنجاح")
        
        print("✅ جميع اختبارات واجهة برمجة التطبيقات نجحت")
        return True
        
    except Exception as e:
        print(f"❌ فشل اختبار واجهة برمجة التطبيقات: {e}")
        return False

def main():
    """الدالة الرئيسية للاختبار"""
    print("🚀 بدء اختبار نظام التوصيات الذكية")
    print("=" * 50)
    
    # اختبار المحرك مباشرة
    engine_success = test_recommendation_engine()
    
    # اختبار واجهة برمجة التطبيقات
    api_success = test_recommendations_api()
    
    print("\n" + "=" * 50)
    print("📊 نتائج الاختبار:")
    print(f"   محرك التوصيات: {'✅ نجح' if engine_success else '❌ فشل'}")
    print(f"   واجهة برمجة التطبيقات: {'✅ نجح' if api_success else '❌ فشل'}")
    
    if engine_success and api_success:
        print("\n🎉 جميع الاختبارات نجحت! نظام التوصيات جاهز للعمل.")
        return 0
    else:
        print("\n💥 بعض الاختبارات فشلت. يرجى مراجعة الأخطاء.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
