"""
نظام المعالجة اللغوية (NLP Pipeline) - معالجة النص متعدد اللغات

هذا الملف يحتوي على النظام الأساسي لمعالجة اللغة الطبيعية
يدعم كشف اللغة، الترجمة، والتوليد متعدد اللغات
"""

import logging
from typing import Dict, List, Optional, Tuple
import re
from langdetect import detect, DetectorFactory
import spacy
from transformers import pipeline, AutoTokenizer, AutoModelForSeq2SeqLM
from deep_translator import GoogleTranslator
import torch
import httpx
from functools import lru_cache
import requests
from urllib.parse import quote
import openai

# Import settings
from src.core.config import settings

# ضمان نتائج ثابتة للكشف عن اللغة
DetectorFactory.seed = 0

# إعداد التسجيل
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# تعيين HTTP client للترجمة
translation_client = httpx.AsyncClient(timeout=30.0)

class NLPPipeline:
    """
    خط أنابيب المعالجة اللغوية - معالجة النص متعدد اللغات
    """
    
    def __init__(self):
        """
        تهيئة خط أنابيب المعالجة اللغوية
        """
        self.supported_languages = ['ar', 'en', 'fr', 'es', 'de', 'it', 'ru']
        
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
            
            # تهيئة OpenAI إذا كان المفتاح متوفراً
            if settings.OPENAI_API_KEY:
                openai.api_key = settings.OPENAI_API_KEY
            
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
    
    @lru_cache(maxsize=1000)
    def translate_text(self, text: str, target_lang: str = 'en', 
                      source_lang: str = 'auto') -> str:
        """
        ترجمة النص إلى اللغة المستهدفة باستخدام Google Translate API
        
        Args:
            text: النص المترجم
            target_lang: اللغة المستهدفة
            source_lang: اللغة المصدر (auto للكشف التلقائي)
            
        Returns:
            str: النص المترجم
        """
        try:
            if not text or len(text.strip()) == 0:
                return text
            
            if source_lang == 'auto':
                source_lang = self.detect_language(text)
            
            if source_lang == target_lang:
                return text  # لا حاجة للترجمة إذا كانت اللغة نفسها
            
            # محاولة استخدام Google Translate API الرسمي إذا كان المفتاح متوفراً
            if settings.GOOGLE_TRANSLATE_API_KEY:
                try:
                    translation = self._translate_with_google_api(text, source_lang, target_lang)
                    if translation:
                        return translation
                except Exception as e:
                    logger.warning(f"Google Translate API فشل: {e}")
            
            # استخدام deep-translator كبديل
            try:
                translator = GoogleTranslator(source=source_lang, target=target_lang)
                translation = translator.translate(text)
                if translation:
                    return translation
            except Exception as e:
                logger.warning(f"deep-translator فشل: {e}")
            
            # Fallback إلى الترجمة البسيطة إذا فشلت جميع APIs
            return self._simple_translation_fallback(text, source_lang, target_lang)
            
        except Exception as e:
            logger.error(f"خطأ في الترجمة: {e}")
            return self._simple_translation_fallback(text, source_lang, target_lang)
    
    def _translate_with_google_api(self, text: str, source_lang: str, target_lang: str) -> str:
        """
        استخدام Google Translate API الرسمي للترجمة
        
        Args:
            text: النص المترجم
            source_lang: اللغة المصدر
            target_lang: اللغة المستهدفة
            
        Returns:
            str: النص المترجم
        """
        try:
            # بناء URL لـ Google Translate API
            base_url = "https://translation.googleapis.com/language/translate/v2"
            params = {
                'q': text,
                'source': source_lang,
                'target': target_lang,
                'format': 'text',
                'key': settings.GOOGLE_TRANSLATE_API_KEY
            }
            
            # إرسال الطلب
            response = requests.post(base_url, data=params, timeout=10)
            response.raise_for_status()
            
            # معالجة الاستجابة
            data = response.json()
            if 'data' in data and 'translations' in data['data']:
                translations = data['data']['translations']
                if translations and len(translations) > 0:
                    return translations[0]['translatedText']
            
            return None
            
        except requests.exceptions.RequestException as e:
            logger.error(f"خطأ في اتصال Google Translate API: {e}")
            raise
        except Exception as e:
            logger.error(f"خطأ في معالجة استجابة Google Translate API: {e}")
            raise
    
    def _simple_translation_fallback(self, text: str, source_lang: str, target_lang: str) -> str:
        """
        ترجمة بسيطة كبديل عند فشل APIs الخارجية
        """
        translations = {
            'ar': {
                'hello': 'مرحباً',
                'help': 'مساعدة',
                'python': 'بايثون',
                'programming': 'برمجة',
                'code': 'كود',
                'learn': 'تعلم',
                'teach': 'علم',
                'explain': 'اشرح',
                'how': 'كيف',
                'what': 'ما',
                'why': 'لماذا',
                'where': 'أين',
                'when': 'متى'
            },
            'en': {
                'مرحباً': 'hello',
                'مساعدة': 'help',
                'بايثون': 'python',
                'برمجة': 'programming',
                'كود': 'code',
                'تعلم': 'learn',
                'علم': 'teach',
                'اشرح': 'explain',
                'كيف': 'how',
                'ما': 'what',
                'لماذا': 'why',
                'أين': 'where',
                'متى': 'when'
            },
            'fr': {
                'hello': 'bonjour',
                'help': 'aide',
                'python': 'python',
                'programming': 'programmation'
            },
            'es': {
                'hello': 'hola',
                'help': 'ayuda',
                'python': 'python',
                'programming': 'programación'
            }
        }
        
        # ترجمة بسيطة للكلمات الشائعة
        if source_lang in translations and target_lang in translations:
            translated_words = []
            for word in text.split():
                word_lower = word.lower()
                if word_lower in translations[source_lang]:
                    translated_word = translations[target_lang].get(
                        translations[source_lang][word_lower], word
                    )
                    translated_words.append(translated_word)
                else:
                    translated_words.append(word)
            return ' '.join(translated_words)
        
        return text  # إرجاع النص الأصلي إذا لم تكن الترجمة ممكنة
    
    async def translate_text_async(self, text: str, target_lang: str = 'en', 
                                 source_lang: str = 'auto') -> str:
        """
        ترجمة غير متزامنة للنص (للاستخدام في واجهات غير متزامنة)
        """
        # يمكن تنفيذ هذا لاحقاً باستخدام async HTTP clients
        return self.translate_text(text, target_lang, source_lang)
    
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
        توليد رد ذكي بناء على prompt وسياق باستخدام نموذج توليد
        
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
                full_prompt = f"Context: {context}\nQuestion: {prompt}\nAnswer:"
            
            # استخدام نموذج توليد متقدم
            response = self._generate_with_advanced_model(full_prompt, language)
            
            # تنظيف الرد وإزالة التكرارات
            cleaned_response = self._clean_generated_response(response, language)
            
            return cleaned_response
                
        except Exception as e:
            logger.error(f"خطأ في توليد الرد: {e}")
            # Fallback إلى الردود الأساسية في حالة الخطأ
            return self._fallback_response(prompt, language)
    
    def _generate_with_advanced_model(self, prompt: str, language: str) -> str:
        """
        توليد الرد باستخدام نماذج متقدمة (OpenAI, T5, GPT-2)
        
        Args:
            prompt: المطالبة المدخلة
            language: لغة الرد
            
        Returns:
            str: الرد المولد
        """
        try:
            # محاولة استخدام OpenAI API أولاً إذا كان المفتاح متوفراً
            if settings.OPENAI_API_KEY:
                try:
                    return self._generate_with_openai(prompt, language)
                except Exception as e:
                    logger.warning(f"OpenAI API فشل: {e}")
            
            # استخدام نموذج T5 للأسئلة البرمجية (أفضل من GPT-2 للإجابة على الأسئلة)
            try:
                return self._generate_with_t5(prompt, language)
            except Exception as e:
                logger.warning(f"نموذج T5 فشل: {e}")
            
            # Fallback إلى GPT-2
            return self._generate_with_gpt2(prompt, language)
                
        except Exception as e:
            logger.error(f"خطأ في توليد النموذج المتقدم: {e}")
            raise
    
    def _generate_with_openai(self, prompt: str, language: str) -> str:
        """
        توليد الرد باستخدام OpenAI API
        
        Args:
            prompt: المطالبة المدخلة
            language: لغة الرد
            
        Returns:
            str: الرد المولد
        """
        try:
            # بناء رسالة النظام لتوجيه النموذج
            system_message = {
                "role": "system",
                "content": "You are BoAI, a helpful programming tutor assistant. Provide clear, concise, and accurate answers to programming questions. Focus on educational value and practical examples."
            }
            
            # بناء رسالة المستخدم
            user_message = {
                "role": "user", 
                "content": prompt
            }
            
            # استدعاء OpenAI API
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[system_message, user_message],
                max_tokens=300,
                temperature=0.7,
                top_p=0.9
            )
            
            if response and 'choices' in response and len(response.choices) > 0:
                return response.choices[0].message.content.strip()
            else:
                raise Exception("استجابة OpenAI فارغة")
                
        except Exception as e:
            logger.error(f"خطأ في توليد النص مع OpenAI: {e}")
            raise
    
    def _generate_with_t5(self, prompt: str, language: str) -> str:
        """
        توليد الرد باستخدام نموذج T5 (أفضل للإجابة على الأسئلة)
        
        Args:
            prompt: المطالبة المدخلة
            language: لغة الرد
            
        Returns:
            str: الرد المولد
        """
        try:
            # تحميل نموذج T5 إذا لم يكن محملاً
            if not hasattr(self, 't5_model'):
                self.t5_model = pipeline(
                    "text2text-generation",
                    model="t5-small",
                    device=0 if torch.cuda.is_available() else -1,
                    torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32
                )
            
            # صياغة الـ prompt بشكل مناسب لـ T5
            t5_prompt = f"question: {prompt} answer:"
            
            # توليد الرد
            generated_text = self.t5_model(
                t5_prompt,
                max_length=200,
                num_return_sequences=1,
                temperature=0.7,
                do_sample=True,
                repetition_penalty=1.1
            )
            
            if generated_text and len(generated_text) > 0:
                response = generated_text[0]['generated_text'].strip()
                # إزالة البادئة إذا كانت موجودة
                if response.startswith("answer:"):
                    response = response[7:].strip()
                return response
            else:
                return "I'll help you with your programming question."
                
        except Exception as e:
            logger.error(f"خطأ في توليد النص مع T5: {e}")
            raise
    
    def _generate_with_gpt2(self, prompt: str, language: str) -> str:
        """
        توليد الرد باستخدام نموذج GPT-2 (النسخة الاحتياطية)
        
        Args:
            prompt: المطالبة المدخلة
            language: لغة الرد
            
        Returns:
            str: الرد المولد
        """
        try:
            # تحميل نموذج التوليد إذا لم يكن محملاً
            if not hasattr(self, 'text_generation_model'):
                self.text_generation_model = pipeline(
                    "text-generation",
                    model="gpt2",
                    device=0 if torch.cuda.is_available() else -1,
                    torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32
                )
            
            # توليد الرد
            generated_text = self.text_generation_model(
                prompt,
                max_length=150,
                num_return_sequences=1,
                temperature=0.7,
                do_sample=True,
                pad_token_id=50256  # GPT-2 pad token
            )
            
            if generated_text and len(generated_text) > 0:
                # استخراج النص المولد فقط (بعد الـ prompt)
                full_text = generated_text[0]['generated_text']
                response = full_text[len(prompt):].strip()
                return response
            else:
                return "I'm here to help you learn programming and technical concepts."
                
        except Exception as e:
            logger.error(f"خطأ في توليد النص الإنجليزي: {e}")
            return "I'll try to help you with your question about programming."
    
    def _clean_generated_response(self, response: str, language: str) -> str:
        """
        تنظيف الرد المولد وإزالة التكرارات والمشاكل
        """
        if not response:
            return self._fallback_response("", language)
        
        # إزالة التكرارات
        lines = response.split('\n')
        unique_lines = []
        seen_lines = set()
        
        for line in lines:
            clean_line = line.strip()
            if clean_line and clean_line not in seen_lines:
                unique_lines.append(clean_line)
                seen_lines.add(clean_line)
        
        cleaned_response = ' '.join(unique_lines)
        
        # تقصير الرد إذا كان طويلاً جداً
        if len(cleaned_response.split()) > 100:
            sentences = cleaned_response.split('.')
            if len(sentences) > 0:
                cleaned_response = sentences[0] + '.'
        
        return cleaned_response
    
    def _fallback_response(self, prompt: str, language: str) -> str:
        """
        رد بديل في حالة فشل التوليد
        """
        responses = {
            'ar': {
                'hello': 'مرحباً! أنا BoAI، مساعدك لتعلم البرمجة. كيف يمكنني مساعدتك اليوم؟',
                'help': 'أنا هنا لمساعدتك في تعلم البرمجة والمفاهيم التقنية. اسألني أي سؤال عن البرمجة، Python، الخوارزميات، أو أي موضوع تقني.',
                'programming': 'أنا متخصص في مساعدتك في مواضيع البرمجة. يمكنني شرح المفاهيم، المساعدة في حل المشاكل، وتقديم أمثلة عملية.',
                'default': 'شكراً على سؤالك. سأحاول مساعدتك في هذا الموضوع البرمجي.'
            },
            'en': {
                'hello': 'Hello! I\'m BoAI, your programming learning assistant. How can I help you today?',
                'help': 'I\'m here to help you learn programming and technical concepts. Ask me anything about programming, Python, algorithms, or any technical topic.',
                'programming': 'I specialize in helping with programming topics. I can explain concepts, help solve problems, and provide practical examples.',
                'default': 'Thank you for your question. I\'ll try to help you with this programming topic.'
            }
        }
        
        lang_responses = responses.get(language, responses['en'])
        prompt_lower = prompt.lower()
        
        if any(word in prompt_lower for word in ['hello', 'hi', 'مرحب', 'اهلا']):
            return lang_responses['hello']
        elif any(word in prompt_lower for word in ['help', 'مساعده', 'مساعدة', 'ساعد']):
            return lang_responses['help']
        elif any(word in prompt_lower for word in ['programming', 'code', 'برمجه', 'كود']):
            return lang_responses['programming']
        else:
            return lang_responses['default']
    
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
