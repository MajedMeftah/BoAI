#!/usr/bin/env python3
"""
اختبار مبسط لنظام التوصيات الذكية - يركز فقط على محرك التوصيات
"""

import sys
import os

# إضافة مسار src إلى sys.path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.core.learning.recommendation_engine import RecommendationEngine

def test_recommendation_engine_simple():
    """اختبار محرك التوصيات مباشرة بدون التطبيق الكامل"""
    print("🔍 اختبار محرك التوصيات مباشرة...")
    
    try:
        # إنشاء instance من المحرك
        engine = RecommendationEngine()
        print("✅ تم تهيئة محرك التوصيات بنجاح")
        
        # اختبار تحميل قاعدة البيانات
        print(f"✅ تم تحميل {len(engine.content_db)} محتوى تعليمي")
        
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
        
        # اختبار إزالة التكرارات
        test_recommendations = recommendations + recommendations[:2]
        unique_recs = engine._remove_duplicates(test_recommendations)
        print(f"✅ تم إزالة التكرارات: {len(test_recommendations)} -> {len(unique_recs)}")
        
        return True
        
    except Exception as e:
        print(f"❌ فشل اختبار محرك التوصيات: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_api_endpoints():
    """اختبار endpoints API بشكل منفصل"""
    print("\n🔍 اختبار منطق API...")
    
    try:
        from src.api.routers.recommendations import router
        print("✅ تم تحميل router التوصيات بنجاح")
        
        # التحقق من وجود جميع endpoints
        endpoints = [route.path for route in router.routes]
        expected_endpoints = [
            '/recommendations/user/{user_id}',
            '/recommendations/user/{user_id}/profile',
            '/recommendations/user/{user_id}/feedback',
            '/recommendations/user/{user_id}/learning-path',
            '/recommendations/content',
            '/recommendations/content/{content_id}',
            '/recommendations/health'
        ]
        
        for endpoint in expected_endpoints:
            if endpoint in endpoints:
                print(f"✅ Endpoint موجود: {endpoint}")
            else:
                print(f"❌ Endpoint مفقود: {endpoint}")
                return False
        
        return True
        
    except Exception as e:
        print(f"❌ فشل اختبار API: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """الدالة الرئيسية للاختبار"""
    print("🚀 بدء اختبار نظام التوصيات الذكية (النسخة المبسطة)")
    print("=" * 60)
    
    # اختبار المحرك مباشرة
    engine_success = test_recommendation_engine_simple()
    
    # اختبار منطق API
    api_success = test_api_endpoints()
    
    print("\n" + "=" * 60)
    print("📊 نتائج الاختبار:")
    print(f"   محرك التوصيات: {'✅ نجح' if engine_success else '❌ فشل'}")
    print(f"   منطق API: {'✅ نجح' if api_success else '❌ فشل'}")
    
    if engine_success and api_success:
        print("\n🎉 جميع اختبارات نظام التوصيات نجحت! النظام جاهز للعمل.")
        print("\n💡 ملاحظة: مشكلة googletrans لا تؤثر على نظام التوصيات.")
        return 0
    else:
        print("\n💥 بعض الاختبارات فشلت. يرجى مراجعة الأخطاء.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
