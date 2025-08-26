"""
نظام إعادة التدريب التلقائي - الجزء العملي من Milestone 2.3

هذا الملف يحتوي على النظام الفعلي لإعادة تدريب النماذج تلقائياً
بناءً على التغذية الراجعة وأداء النموذج الحالي
"""

import logging
import json
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
import joblib
import threading
import time
from sqlalchemy.orm import Session

from src.core.database.session import get_db
from src.core.database.models import Feedback, Message
from src.core.utils.cache import cache_manager
from src.core.learning.ml_optimizer import MLOptimizer

# إعداد التسجيل
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AutoRetrainer:
    """
    نظام إعادة التدريب التلقائي للنماذج
    """
    
    def __init__(self):
        """
        تهيئة نظام إعادة التدريب التلقائي
        """
        self.ml_optimizer = MLOptimizer()
        self.retraining_threads = {}
        self.is_running = False
        self.retraining_history = {}
        
        logger.info("تم تهيئة AutoRetrainer بنجاح")
    
    def start_retraining_monitor(self):
        """
        بدء مراقبة وإعادة التدريب التلقائي
        """
        self.is_running = True
        monitor_thread = threading.Thread(target=self._monitor_models)
        monitor_thread.daemon = True
        monitor_thread.start()
        
        logger.info("بدأ مراقبة إعادة التدريب التلقائي")
    
    def stop_retraining_monitor(self):
        """
        إيقاف مراقبة إعادة التدريب التلقائي
        """
        self.is_running = False
        logger.info("تم إيقاف مراقبة إعادة التدريب التلقائي")
    
    def _monitor_models(self):
        """
        مراقبة النماذج وتنفيذ إعادة التدريب عند الحاجة
        """
        while self.is_running:
            try:
                # التحقق من الجدول الزمني لإعادة التدريب
                self._check_retraining_schedule()
                
                # التحقق من أداء النماذج
                self._check_model_performance()
                
                # الانتظار قبل الفحص التالي
                time.sleep(300)  # 5 دقائق
                
            except Exception as e:
                logger.error(f"خطأ في مراقبة النماذج: {e}")
                time.sleep(60)  # الانتظار دقيقة ثم المحاولة مرة أخرى
    
    def _check_retraining_schedule(self):
        """
        التحقق من الجدول الزمني لإعادة التدريب
        """
        current_time = datetime.now()
        
        for schedule_id, schedule in self.ml_optimizer.retraining_schedule.items():
            if schedule['status'] != 'active':
                continue
            
            next_run = datetime.fromisoformat(schedule['next_run'])
            
            if current_time >= next_run:
                # وقت إعادة التدريب
                model_type = schedule['model_type']
                logger.info(f"بدء إعادة التدريب المجدول للنموذج {model_type}")
                
                # تنفيذ إعادة التدريب في thread منفصل
                thread = threading.Thread(
                    target=self._execute_scheduled_retraining,
                    args=(model_type, schedule_id)
                )
                thread.daemon = True
                thread.start()
                
                # تحديث وقت التشغيل التالي
                schedule['next_run'] = self.ml_optimizer._calculate_next_run_time(
                    schedule['schedule_type']
                )
    
    def _check_model_performance(self):
        """
        التحقق من أداء النماذج وإعادة التدريب إذا لزم الأمر
        """
        model_types = ['nlp', 'recommendation', 'translation']
        
        for model_type in model_types:
            try:
                # تحليل أداء النموذج
                performance = self.ml_optimizer.analyze_model_performance(model_type)
                
                # التحقق إذا كان الأداء دون العتبة المطلوبة
                if performance['confidence_score'] < 0.6:
                    logger.warning(f"أداء النموذج {model_type} منخفض: {performance['confidence_score']}")
                    
                    # بدء إعادة التدريب
                    self.trigger_retraining(model_type, 'performance_based')
                
                # التحقق من وجود مشاكل شائعة
                if len(performance['common_issues']) > 5:
                    logger.warning(f"النموذج {model_type} لديه {len(performance['common_issues'])} مشاكل شائعة")
                    
                    # بدء إعادة التدريب
                    self.trigger_retraining(model_type, 'issue_based')
                    
            except Exception as e:
                logger.error(f"خطأ في التحقق من أداء النموذج {model_type}: {e}")
    
    def trigger_retraining(self, model_type: str, trigger_reason: str) -> bool:
        """
        بدء إعادة التدريب للنموذج
        
        Args:
            model_type: نوع النموذج
            trigger_reason: سبب إعادة التدريب
            
        Returns:
            bool: True إذا تم بدء إعادة التدريب بنجاح
        """
        try:
            # التحقق إذا كان هناك إعادة تدريب جارية بالفعل
            if model_type in self.retraining_threads and self.retraining_threads[model_type].is_alive():
                logger.info(f"إعادة التدريب للنموذج {model_type} جارية بالفعل")
                return False
            
            # بدء إعادة التدريب في thread منفصل
            thread = threading.Thread(
                target=self._execute_retraining,
                args=(model_type, trigger_reason)
            )
            thread.daemon = True
            thread.start()
            
            self.retraining_threads[model_type] = thread
            
            logger.info(f"بدأت إعادة التدريب للنموذج {model_type} بسبب: {trigger_reason}")
            return True
            
        except Exception as e:
            logger.error(f"خطأ في بدء إعادة التدريب للنموذج {model_type}: {e}")
            return False
    
    def _execute_scheduled_retraining(self, model_type: str, schedule_id: str):
        """
        تنفيذ إعادة التدريب المجدولة
        """
        try:
            result = self.ml_optimizer.execute_automatic_retraining(model_type)
            
            # تسجيل نتائج إعادة التدريب
            self._log_retraining_result(model_type, 'scheduled', result)
            
            # إرسال إشعار بنتائج إعادة التدريب
            self._send_retraining_notification(model_type, result)
            
        except Exception as e:
            logger.error(f"خطأ في إعادة التدريب المجدولة للنموذج {model_type}: {e}")
    
    def _execute_retraining(self, model_type: str, trigger_reason: str):
        """
        تنفيذ إعادة التدريب الفعلية
        """
        try:
            result = self.ml_optimizer.execute_automatic_retraining(model_type)
            
            # تسجيل نتائج إعادة التدريب
            self._log_retraining_result(model_type, trigger_reason, result)
            
            # إرسال إشعار بنتائج إعادة التدريب
            self._send_retraining_notification(model_type, result)
            
        except Exception as e:
            logger.error(f"خطأ في إعادة التدريب للنموذج {model_type}: {e}")
            
            # تسجيل الفشل
            self._log_retraining_result(
                model_type, 
                trigger_reason, 
                {'success': False, 'error': str(e)}
            )
    
    def _log_retraining_result(self, model_type: str, trigger_reason: str, result: Dict):
        """
        تسجيل نتائج إعادة التدريب
        """
        retraining_id = f"{model_type}_{datetime.now().timestamp()}"
        
        retraining_record = {
            'id': retraining_id,
            'model_type': model_type,
            'trigger_reason': trigger_reason,
            'result': result,
            'timestamp': datetime.now().isoformat(),
            'duration': result.get('duration', '00:00:00') if result.get('success') else 'N/A'
        }
        
        # تخزين في السجل
        if model_type not in self.retraining_history:
            self.retraining_history[model_type] = []
        
        self.retraining_history[model_type].append(retraining_record)
        
        # الاحتفاظ بأخر 50 سجل فقط
        if len(self.retraining_history[model_type]) > 50:
            self.retraining_history[model_type] = self.retraining_history[model_type][-50:]
        
        logger.info(f"تم تسجيل نتائج إعادة التدريب للنموذج {model_type}")
    
    def _send_retraining_notification(self, model_type: str, result: Dict):
        """
        إرسال إشعار بنتائج إعادة التدريب
        """
        try:
            # في التنفيذ الحقيقي، سيتم إرسال إشعارات عبر البريد الإلكتروني أو نظام الإشعارات
            if result.get('success'):
                message = f"تم إعادة تدريب النموذج {model_type} بنجاح. التحسن: {result.get('improvement', 'غير محدد')}"
                logger.info(message)
            else:
                message = f"فشل إعادة تدريب النموذج {model_type}: {result.get('error', 'سبب غير معروف')}"
                logger.error(message)
                
        except Exception as e:
            logger.error(f"خطأ في إرسال إشعار إعادة التدريب: {e}")
    
    def get_retraining_status(self, model_type: str = None) -> Dict[str, Any]:
        """
        الحصول على حالة إعادة التدريب الحالية
        
        Args:
            model_type: نوع النموذج (اختياري)
            
        Returns:
            Dict: حالة إعادة التدريب
        """
        status = {
            'is_running': self.is_running,
            'active_threads': {},
            'retraining_history': {}
        }
        
        # معلومات Threads النشطة
        for model_type, thread in self.retraining_threads.items():
            status['active_threads'][model_type] = {
                'is_alive': thread.is_alive(),
                'ident': thread.ident
            }
        
        # سجل إعادة التدريب
        if model_type:
            if model_type in self.retraining_history:
                status['retraining_history'][model_type] = self.retraining_history[model_type]
        else:
            status['retraining_history'] = self.retraining_history
        
        return status
    
    def cleanup_old_models(self, days_to_keep: int = 30):
        """
        تنظيف النماذج القديمة
        
        Args:
            days_to_keep: عدد الأيام للاحتفاظ بالنماذج
        """
        try:
            # هذا مثال مبسط، في التنفيذ الحقيقي سيتم حذف ملفات النماذج القديمة
            cutoff_date = datetime.now() - timedelta(days=days_to_keep)
            
            logger.info(f"بدء تنظيف النماذج الأقدم من {cutoff_date.date()}")
            
            # هنا سيتم تنفيذ عملية التنظيف الفعلية
            # cleanup_count = self._delete_old_model_files(cutoff_date)
            
            logger.info(f"تم تنظيف النماذج القديمة")
            
        except Exception as e:
            logger.error(f"خطأ في تنظيف النماذج القديمة: {e}")
    
    def export_training_data(self, model_type: str, file_path: str) -> bool:
        """
        تصدير بيانات التدريب لاستخدامها خارجياً
        
        Args:
            model_type: نوع النموذج
            file_path: مسار ملف التصدير
            
        Returns:
            bool: True إذا تم التصدير بنجاح
        """
        try:
            # جمع بيانات التدريب
            training_data = self.ml_optimizer._collect_training_data(model_type)
            
            if not training_data:
                logger.warning(f"لا توجد بيانات تدريب للنموذج {model_type} للتصدير")
                return False
            
            # تحويل إلى DataFrame وحفظ
            df = pd.DataFrame(training_data)
            df.to_csv(file_path, index=False, encoding='utf-8')
            
            logger.info(f"تم تصدير {len(training_data)} عينة تدريب إلى {file_path}")
            return True
            
        except Exception as e:
            logger.error(f"خطأ في تصدير بيانات التدريب: {e}")
            return False

# إنشاء instance عام لنظام إعادة التدريب التلقائي
auto_retrainer = AutoRetrainer()

# بدء المراقبة التلقائية عند التحميل
auto_retrainer.start_retraining_monitor()

# مثال للاستخدام
if __name__ == "__main__":
    # اختبار نظام إعادة التدريب
    model_type = "nlp"
    
    # الحصول على حالة النظام
    status = auto_retrainer.get_retraining_status()
    print("حالة نظام إعادة التدريب:")
    print(json.dumps(status, ensure_ascii=False, indent=2))
    
    # بدء إعادة التدريب يدوياً
    triggered = auto_retrainer.trigger_retraining(model_type, "manual_test")
    print(f"\nتم بدء إعادة التدريب: {triggered}")
    
    # الانتظار قليلاً ثم التحقق من الحالة
    import time
    time.sleep(2)
    
    status = auto_retrainer.get_retraining_status(model_type)
    print(f"\nحالة إعادة التدريب للنموذج {model_type}:")
    print(json.dumps(status, ensure_ascii=False, indent=2))
