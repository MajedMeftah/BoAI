#!/usr/bin/env python3
"""
اختبار نظام المعالجة اللغوية المحسن
"""

import sys
sys.path.append('src')

from src.core.nlp.pipeline import NLPPipeline

def test_translation():
    """اختبار نظام الترجمة الجديد"""
    print("🔍 اختبار نظام الترجمة المحسن...")
    
    nlp = NLPPipeline()
    
    # اختبار الترجمة من العربية إلى الإنجليزية
    arabic_text = "مرحباً، كيف يمكنني تعلم البرمجة؟"
    translated = nlp.translate_text(arabic_text, 'en', 'ar')
    print(f"العربية: {arabic_text}")
    print(f"الإنجليزية: {translated}")
    print()
    
    # اختبار الترجمة من الإنجليزية إلى العربية
    english_text = "Hello, how can I learn Python programming?"
    translated = nlp.translate_text(english_text, 'ar', 'en')
    print(f"الإنجليزية: {english_text}")
    print(f"العربية: {translated}")
    print()
    
    # اختبار كشف اللغة
    detected = nlp.detect_language(arabic_text)
    print(f"كشف اللغة للنص العربي: {detected}")
    detected = nlp.detect_language(english_text)
    print(f"كشف اللغة للنص الإنجليزي: {detected}")
    print()

def test_response_generation():
    """اختبار نظام توليد الردود الجديد"""
    print("🤖 اختبار نظام توليد الردود المحسن...")
    
    nlp = NLPPipeline()
    
    # اختبار الأسئلة المختلفة
    test_questions = [
        "Hello, how are you?",
        "كيف يمكنني تعلم بايثون؟",
        "What is programming?",
        "ما هي الخوارزميات؟",
        "Explain variables in programming",
        "اشرح لي المتغيرات في البرمجة"
    ]
    
    for question in test_questions:
        response = nlp.generate_response(question)
        lang = nlp.detect_language(question)
        print(f"السؤال ({lang}): {question}")
        print(f"الرد: {response}")
        print("-" * 80)
        print()

def test_multilingual():
    """اختبار دعم اللغات المتعددة"""
    print("🌍 اختبار دعم اللغات المتعددة...")
    
    nlp = NLPPipeline()
    
    # نصوص بلغات مختلفة
    multilingual_texts = [
        ("مرحباً بك في نظام BoAI", "ar"),
        ("Welcome to BoAI system", "en"),
        ("Bienvenue dans le système BoAI", "fr"),
        ("Bienvenido al sistema BoAI", "es")
    ]
    
    for text, expected_lang in multilingual_texts:
        detected_lang = nlp.detect_language(text)
        print(f"النص: {text}")
        print(f"اللغة المتوقعة: {expected_lang}, المكتشفة: {detected_lang}")
        
        if detected_lang == expected_lang:
            print("✅ كشف اللغة ناجح")
        else:
            print("❌ كشف اللغة فشل")
        print()

if __name__ == "__main__":
    print("🧪 بدء اختبار نظام المعالجة اللغوية المحسن")
    print("=" * 60)
    
    try:
        test_translation()
        test_response_generation()
        test_multilingual()
        
        print("🎉 جميع الاختبارات اكتملت بنجاح!")
        
    except Exception as e:
        print(f"❌ حدث خطأ أثناء الاختبار: {e}")
        import traceback
        traceback.print_exc()
