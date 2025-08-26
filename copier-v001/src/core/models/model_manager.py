"""
نظام إدارة النماذج (Model Manager) - القلب النابض لـ BoAI

هذا الملف يحتوي على النظام الأساسي لإدارة نماذج الذكاء الاصطناعي
يدعم تحميل، تفريغ، وإدارة إصدارات متعددة من النماذج
"""

import logging
from typing import Dict, Optional, List
from pathlib import Path
import json
from datetime import datetime

# إعداد التسجيل
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ModelManager:
    """
    مدير النماذج الرئيسي - مسؤول عن إدارة دورة حياة النماذج
    """
    
    def __init__(self, models_dir: str = "models"):
        """
        تهيئة مدير النماذج
        
        Args:
            models_dir: مسجل مجلد النماذج
        """
        self.models_dir = Path(models_dir)
        self.models: Dict[str, dict] = {}  # النماذج المحملة
        self.model_versions: Dict[str, List[str]] = {}  # إصدارات النماذج
        self.model_metadata: Dict[str, dict] = {}  # بيانات وصفية للنماذج
        
        # إنشاء مجلد النماذج إذا لم يكن موجوداً
        self.models_dir.mkdir(exist_ok=True)
        
        logger.info(f"تم تهيئة ModelManager مع مجلد النماذج: {self.models_dir}")
    
    def load_model(self, model_name: str, version: str = "latest") -> bool:
        """
        تحميل نموذج من المسار
        
        Args:
            model_name: اسم النموذج
            version: إصدار النموذج (default: "latest")
            
        Returns:
            bool: True إذا تم التحميل بنجاح، False إذا فشل
        """
        try:
            model_path = self._get_model_path(model_name, version)
            
            if not model_path.exists():
                logger.error(f"مسار النموذج غير موجود: {model_path}")
                return False
            
            # محاكاة تحميل النموذج (سيتم استبدالها بتحميل حقيقي)
            model_data = {
                'name': model_name,
                'version': version,
                'path': str(model_path),
                'loaded_at': datetime.now().isoformat(),
                'status': 'loaded'
            }
            
            self.models[model_name] = model_data
            
            # تحديث بيانات الإصدارات
            if model_name not in self.model_versions:
                self.model_versions[model_name] = []
            if version not in self.model_versions[model_name]:
                self.model_versions[model_name].append(version)
            
            logger.info(f"تم تحميل النموذج: {model_name} v{version}")
            return True
            
        except Exception as e:
            logger.error(f"خطأ في تحميل النموذج {model_name}: {e}")
            return False
    
    def unload_model(self, model_name: str) -> bool:
        """
        إلغاء تحميل النموذج من الذاكرة
        
        Args:
            model_name: اسم النموذج
            
        Returns:
            bool: True إذا تم الإلغاء بنجاح، False إذا فشل
        """
        if model_name not in self.models:
            logger.warning(f"النموذج غير محمل: {model_name}")
            return False
        
        try:
            # محاكاة إلغاء تحميل النموذج
            del self.models[model_name]
            logger.info(f"تم إلغاء تحميل النموذج: {model_name}")
            return True
            
        except Exception as e:
            logger.error(f"خطأ في إلغاء تحميل النموذج {model_name}: {e}")
            return False
    
    def get_model(self, model_name: str) -> Optional[dict]:
        """
        الحصول على بيانات النموذج
        
        Args:
            model_name: اسم النموذج
            
        Returns:
            Optional[dict]: بيانات النموذج أو None إذا لم يكن محملاً
        """
        return self.models.get(model_name)
    
    def list_models(self) -> List[str]:
        """
        قائمة بأسماء النماذج المحملة
        
        Returns:
            List[str]: قائمة بأسماء النماذج
        """
        return list(self.models.keys())
    
    def list_versions(self, model_name: str) -> List[str]:
        """
        قائمة بإصدارات النموذج المتاحة
        
        Args:
            model_name: اسم النموذج
            
        Returns:
            List[str]: قائمة بالإصدارات المتاحة
        """
        return self.model_versions.get(model_name, [])
    
    def get_model_info(self, model_name: str) -> Optional[dict]:
        """
        الحصول على معلومات مفصلة عن النموذج
        
        Args:
            model_name: اسم النموذج
            
        Returns:
            Optional[dict]: معلومات النموذج أو None
        """
        if model_name not in self.models:
            return None
        
        model_info = self.models[model_name].copy()
        
        # إضافة معلومات إضافية
        model_info['available_versions'] = self.list_versions(model_name)
        model_info['memory_usage'] = self._estimate_memory_usage(model_name)
        
        return model_info
    
    def _get_model_path(self, model_name: str, version: str) -> Path:
        """
        الحصول على مسار النموذج
        
        Args:
            model_name: اسم النموذج
            version: إصدار النموذج
            
        Returns:
            Path: مسار النموذج
        """
        if version == "latest":
            # البحث عن أحدث إصدار
            versions = self._discover_versions(model_name)
            if not versions:
                raise FileNotFoundError(f"لا توجد إصدارات للنموذج {model_name}")
            version = max(versions)
        
        return self.models_dir / model_name / version / "model"
    
    def _discover_versions(self, model_name: str) -> List[str]:
        """
        اكتشاف الإصدارات المتاحة للنموذج
        
        Args:
            model_name: اسم النموذج
            
        Returns:
            List[str]: قائمة بالإصدارات المتاحة
        """
        model_dir = self.models_dir / model_name
        if not model_dir.exists():
            return []
        
        versions = []
        for item in model_dir.iterdir():
            if item.is_dir():
                versions.append(item.name)
        
        return sorted(versions)
    
    def _estimate_memory_usage(self, model_name: str) -> str:
        """
        تقدير استخدام الذاكرة للنموذج (وهمي حالياً)
        
        Args:
            model_name: اسم النموذج
            
        Returns:
            str: تقدير استخدام الذاكرة
        """
        # هذه دالة وهمية - سيتم استبدالها بحساب حقيقي
        sizes = {
            'small': '~100MB',
            'medium': '~500MB', 
            'large': '~1GB',
            'xlarge': '~2GB+'
        }
        
        # تقدير مبني على اسم النموذج
        if 'small' in model_name.lower():
            return sizes['small']
        elif 'large' in model_name.lower():
            return sizes['large']
        elif 'xlarge' in model_name.lower():
            return sizes['xlarge']
        else:
            return sizes['medium']
    
    def save_model_metadata(self, model_name: str, metadata: dict) -> bool:
        """
        حفظ البيانات الوصفية للنموذج
        
        Args:
            model_name: اسم النموذج
            metadata: البيانات الوصفية
            
        Returns:
            bool: True إذا تم الحفظ بنجاح
        """
        try:
            self.model_metadata[model_name] = metadata
            
            # حفظ في ملف
            metadata_path = self.models_dir / model_name / "metadata.json"
            metadata_path.parent.mkdir(parents=True, exist_ok=True)
            
            with open(metadata_path, 'w', encoding='utf-8') as f:
                json.dump(metadata, f, ensure_ascii=False, indent=2)
            
            logger.info(f"تم حفظ البيانات الوصفية للنموذج: {model_name}")
            return True
            
        except Exception as e:
            logger.error(f"خطأ في حفظ البيانات الوصفية: {e}")
            return False
    
    def load_model_metadata(self, model_name: str) -> Optional[dict]:
        """
        تحميل البيانات الوصفية للنموذج
        
        Args:
            model_name: اسم النموذج
            
        Returns:
            Optional[dict]: البيانات الوصفية أو None
        """
        if model_name in self.model_metadata:
            return self.model_metadata[model_name]
        
        try:
            metadata_path = self.models_dir / model_name / "metadata.json"
            if metadata_path.exists():
                with open(metadata_path, 'r', encoding='utf-8') as f:
                    metadata = json.load(f)
                
                self.model_metadata[model_name] = metadata
                return metadata
            
        except Exception as e:
            logger.error(f"خطأ في تحميل البيانات الوصفية: {e}")
        
        return None

# مثال للاستخدام
if __name__ == "__main__":
    # إنشاء مدير النماذج
    manager = ModelManager()
    
    # تحميل نموذج تجريبي
    manager.load_model("programming_tutor", "v1.0")
    
    # الحصول على معلومات النموذج
    info = manager.get_model_info("programming_tutor")
    print("معلومات النموذج:", info)
    
    # قائمة النماذج المحملة
    print("النماذج المحملة:", manager.list_models())
