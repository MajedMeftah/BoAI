"""
نظام المعالجة اللغوية (NLP Pipeline) - معالجة النص متعدد اللغات

هذا الملف يحتوي على النظام الأساسي لمعالجة اللغة الطبيعية
يدعم كشف اللغة، الترجمة، والتوليد متعدد اللغات
"""

import logging
from typing import Dict, List, Optional, Tuple
import re
from langdetect import detect, DetectorFactory
from googletrans import Translator
import spacy
from transformers import pipeline, AutoTokenizer, AutoModelForSeq2SeqLM
import torch

# ضمان نتائج ثابتة للكشف عن اللغة
DetectorFactory.seed = 0

# إعداد التسجيل
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class NLPPipeline:
    """
    خط أنابيب المعالجة اللغوية - معالجة النص متعدد اللغات
    """
    
    def __init__(self):
        """
        تهيئة خط أنابيب المعالجة اللغوية
        """
        self.supported_languages = ['ar', 'en', 'fr', 'es', 'de', 'it', 'ru']
        self.translator = Translator()
        
        # تحميل نماذج معالجة اللغة الطبيعية
        self._load_models()
        
        logger.info("تم تهيئة NLPPipeline بنجاح")
    
    def _load_models(self):
        """تحميل نماذج المعالجة اللغوية"""
        try:
            # نموذج لكشف الكيانات المسماة (NER)
            self.ner_model = pipeline(
                "ner",
                aggregation_strategy="simple",
                device=0 if torch.cuda.is_available() else -1
            )
            
            # نموذج للتلخيص
            self.summarization_model = pipeline(
                "summarization",
                model="facebook/bart-large-cnn",
                device=0 if torch.cuda.is_available() else -1
            )
            
            # نموذج للترجمة (سيتم تحميله عند الحاجة)
            self.translation_models = {}
            
            logger.info("تم تحميل نماذج المعالجة اللغوية بنجاح")
            
        except Exception as e:
            logger.error(f"خطأ في تحميل النماذج: {e}")
            # نماذج بديلة في حالة الخطأ
            self.ner_model = None
            self.summarization_model = None
            self.translation_models = {}
    
    def detect_language(self, text: str) -> str:
        """
        كشف لغة النص
        
        Args:
            text: النص المدخل
            
        Returns:
            str: كود اللغة (مثل 'ar', 'en', إلخ)
        """
        try:
            if not text or len(text.strip()) < 3:
                return 'unknown'
            
            # استخدام langdetect للكشف عن اللغة
            detected_lang = detect(text)
            
            # التأكد من أن اللغة مدعومة
            if detected_lang in self.supported_languages:
                return detected_lang
            else:
                # افتراض الإنجليزية إذا كانت اللغة غير مدعومة
                return 'en'
                
        except Exception as e:
            logger.error(f"خطأ في كشف اللغة: {e}")
            return 'en'  # افتراض الإنجليزية في حالة الخطأ
    
    def translate_text(self, text: str, target_lang: str = 'en', 
                      source_lang: str = 'auto') -> str:
        """
        ترجمة النص إلى اللغة المستهدفة
        
        Args:
            text: النص المترجم
            target_lang: اللغة المستهدفة
            source_lang: اللغة المصدر (auto للكشف التلقائي)
            
        Returns:
            str: النص المترجم
        """
        try:
            if source_lang == 'auto':
                source_lang = self.detect_language(text)
            
            if source_lang == target_lang:
                return text  # لا حاجة للترجمة إذا كانت اللغة نفسها
            
            # استخدام googletrans للترجمة
            translation = self.translator.translate(
                text, 
                src=source_lang, 
                dest=target_lang
            )
            
            return translation.text
            
        except Exception as e:
            logger.error(f"خطأ في الترجمة: {e}")
            return text  # إرجاع النص الأصلي في حالة الخطأ
    
    def process_text(self, text: str, language: str = 'auto', 
                    operations: List[str] = None) -> Dict:
        """
        معالجة النص عبر multiple processors
        
        Args:
            text: النص المدخل
            language: لغة النص (auto للكشف التلقائي)
            operations: قائمة العمليات المطلوبة
            
        Returns:
            Dict: نتائج المعالجة
        """
        if operations is None:
            operations = ['detect_language', 'tokenize', 'ner']
        
        results = {
            'original_text': text,
            'processed_text': text,
            'language': language,
            'operations': {},
            'entities': [],
            'tokens': []
        }
        
        try:
            # كشف اللغة إذا كان تلقائي
            if language == 'auto':
                detected_lang = self.detect_language(text)
                results['language'] = detected_lang
                results['operations']['language_detection'] = {
                    'detected_language': detected_lang,
                    'confidence': 'high'  # يمكن إضافة ثقة فعلية لاحقاً
                }
            
            # تطبيق العمليات المطلوبة
            for operation in operations:
                if operation == 'tokenize':
                    tokens = self._tokenize_text(text, results['language'])
                    results['tokens'] = tokens
                    results['operations']['tokenization'] = {
                        'token_count': len(tokens),
                        'tokens': tokens[:10]  # أول 10 tokens فقط للعرض
                    }
                
                elif operation == 'ner' and self.ner_model:
                    entities = self._extract_entities(text, results['language'])
                    results['entities'] = entities
                    results['operations']['ner'] = {
                        'entity_count': len(entities),
                        'entities': entities
                    }
                
                elif operation == 'summarize' and self.summarization_model:
                    summary = self._summarize_text(text, results['language'])
                    results['operations']['summarization'] = {
                        'summary': summary,
                        'original_length': len(text),
                        'summary_length': len(summary)
                    }
                    results['processed_text'] = summary
            
            return results
            
        except Exception as e:
            logger.error(f"خطأ في معالجة النص: {e}")
            results['error'] = str(e)
            return results
    
    def _tokenize_text(self, text: str, language: str) -> List[str]:
        """
        تقسيم النص إلى tokens
        
        Args:
            text: النص المدخل
            language: لغة النص
            
        Returns:
            List[str]: قائمة الـ tokens
        """
        try:
            # تقسيم أساسي حسب المسافات وعلامات الترقيم
            tokens = re.findall(r'\w+|[^\w\s]', text, re.UNICODE)
            return tokens
            
        except Exception as e:
            logger.error(f"خطأ في تقسيم النص: {e}")
            return text.split()  # Fallback إلى تقسيم المسافات
    
    def _extract_entities(self, text: str, language: str) -> List[Dict]:
        """
        استخراج الكيانات المسماة من النص
        
        Args:
            text: النص المدخل
            language: لغة النص
            
        Returns:
            List[Dict]: قائمة الكيانات المستخرجة
        """
        try:
            if not self.ner_model:
                return []
            
            # الترجم إلى الإنجليزية للـ NER (النماذج الإنجليزية أفضل عادة)
            if language != 'en':
                translated_text = self.translate_text(text, 'en', language)
            else:
                translated_text = text
            
            # استخراج الكيانات
            entities = self.ner_model(translated_text)
            
            # معالجة النتائج
            processed_entities = []
            for entity in entities:
                processed_entities.append({
                    'entity': entity['entity_group'],
                    'word': entity['word'],
                    'score': float(entity['score']),
                    'start': entity['start'],
                    'end': entity['end']
                })
            
            return processed_entities
            
        except Exception as e:
            logger.error(f"خطأ في استخراج الكيانات: {e}")
            return []
    
    def _summarize_text(self, text: str, language: str) -> str:
        """
        تلخيص النص
        
        Args:
            text: النص المدخل
            language: لغة النص
            
        Returns:
            str: النص المختصر
        """
        try:
            if not self.summarization_model:
                return text
            
            # الترجم إلى الإنجليزية للتلخيص
            if language != 'en':
                translated_text = self.translate_text(text, 'en', language)
            else:
                translated_text = text
            
            # التلخيص
            summary = self.summarization_model(
                translated_text,
                max_length=150,
                min_length=30,
                do_sample=False
            )
            
            # الترجم مرة أخرى إلى اللغة الأصلية إذا لزم الأمر
            if language != 'en':
                translated_summary = self.translate_text(summary[0]['summary_text'], language, 'en')
                return translated_summary
            else:
                return summary[0]['summary_text']
            
        except Exception as e:
            logger.error(f"خطأ في التلخيص: {e}")
            return text
    
    def generate_response(self, prompt: str, context: str = None, 
                         language: str = 'auto') -> str:
        """
        توليد رد بناء على prompt وسياق
        
        Args:
            prompt: المطالبة المدخلة
            context: السياق (اختياري)
            language: لغة الرد
            
        Returns:
            str: الرد المولد
        """
        try:
            # كشف اللغة إذا كان تلقائي
            if language == 'auto':
                language = self.detect_language(prompt)
            
            # بناء prompt كامل مع السياق
            full_prompt = prompt
            if context:
                full_prompt = f"Context: {context}\nQuestion: {prompt}"
            
            # محاكاة توليد الرد (سيتم استبدالها بنموذج حقيقي)
            responses = {
                'ar': {
                    'hello': 'مرحباً! كيف يمكنني مساعدتك اليوم؟',
                    'help': 'أنا هنا لمساعدتك في تعلم البرمجة والمفاهيم التقنية.',
                    'default': 'شكراً على سؤالك. سأحاول مساعدتك في هذا الموضوع.'
                },
                'en': {
                    'hello': 'Hello! How can I help you today?',
                    'help': 'I\'m here to help you learn programming and technical concepts.',
                    'default': 'Thank you for your question. I\'ll try to help you with this topic.'
                }
            }
            
            # البحث عن رد مناسب
            prompt_lower = prompt.lower()
            lang_responses = responses.get(language, responses['en'])
            
            if 'hello' in prompt_lower or 'مرحب' in prompt_lower:
                return lang_responses.get('hello', lang_responses['default'])
            elif 'help' in prompt_lower or 'مساعد' in prompt_lower:
                return lang_responses.get('help', lang_responses['default'])
            else:
                return lang_responses['default']
                
        except Exception as e:
            logger.error(f"خطأ في توليد الرد: {e}")
            return "عذراً، حدث خطأ في المعالجة. يرجى المحاولة مرة أخرى."
    
    def low_confidence(self, text: str, threshold: float = 0.3) -> bool:
        """
        التحقق إذا كان النص منخفض الثقة
        
        Args:
            text: النص المدخل
            threshold: عتبة الثقة
            
        Returns:
            bool: True إذا كان النص منخفض الثقة
        """
        try:
            # تحليل بسيط للثقة (يمكن تحسينه)
            words = text.split()
            
            # النصوص القصيرة جداً تعتبر منخفضة الثقة
            if len(words) < 3:
                return True
            
            # النصوص العامة جداً
            general_phrases = [
                'i don\'t know', 'لا أعرف', 'maybe', 'ربما',
                'not sure', 'لست متأكد', 'could be', 'قد يكون'
            ]
            
            text_lower = text.lower()
            for phrase in general_phrases:
                if phrase in text_lower:
                    return True
            
            return False
            
        except Exception as e:
            logger.error(f"خطأ في التحقق من الثقة: {e}")
            return True  # افتراض منخفض الثقة في حالة الخطأ

# مثال للاستخدام
if __name__ == "__main__":
    # إنشاء خط أنابيب المعالجة اللغوية
    nlp_pipeline = NLPPipeline()
    
    # مثال للنص العربي
    arabic_text = "مرحباً، أنا مهتم بتعلم البرمجة بلغة Python"
    
    # معالجة النص
    result = nlp_pipeline.process_text(
        arabic_text,
        language='auto',
        operations=['detect_language', 'tokenize', 'ner']
    )
    
    print("نتائج المعالجة:")
    print(f"اللغة: {result['language']}")
    print(f"عدد Tokens: {len(result['tokens'])}")
    print(f"عدد الكيانات: {len(result['entities'])}")
    
    # توليد رد
    response = nlp_pipeline.generate_response("كيف أبدأ في تعلم Python؟")
    print(f"الرد: {response}")
