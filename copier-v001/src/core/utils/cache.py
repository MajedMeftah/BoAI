"""
نظام التخزين المؤقت لـ BoAI - إدارة الذاكرة المؤقتة

هذا الملف يحتوي على نظام التخزين المؤقت باستخدام Redis
مع دعم للتخزين المحلي كبديل عند عدم توفر Redis
"""

import logging
import json
import time
from typing import Any, Optional, Dict, Union
from datetime import datetime, timedelta
import redis
from functools import wraps

from src.core.config import settings
from src.core.utils.helpers import generate_uuid, get_timestamp

# إعداد التسجيل
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class CacheManager:
    """
    مدير التخزين المؤقت - يدعم Redis والتخزين المحلي
    """
    
    def __init__(self):
        """تهيئة مدير التخزين المؤقت"""
        self.redis_client = None
        self.local_cache = {}
        self.use_redis = False
        
        self._init_redis()
    
    def _init_redis(self) -> bool:
        """
        تهيئة اتصال Redis
        
        Returns:
            bool: True إذا تم الاتصال بنجاح
        """
        try:
            self.redis_client = redis.Redis.from_url(
                settings.REDIS_URL,
                decode_responses=True,
                socket_timeout=5,
                socket_connect_timeout=5,
                retry_on_timeout=True
            )
            
            # اختبار الاتصال
            self.redis_client.ping()
            self.use_redis = True
            logger.info("تم الاتصال بـ Redis بنجاح")
            return True
            
        except (redis.ConnectionError, redis.TimeoutError) as e:
            logger.warning(f"فشل الاتصال بـ Redis: {e}. استخدام التخزين المحلي.")
            self.use_redis = False
            return False
        except Exception as e:
            logger.error(f"خطأ غير متوقع في تهيئة Redis: {e}")
            self.use_redis = False
            return False
    
    def set(self, key: str, value: Any, ttl: Optional[int] = None) -> bool:
        """
        تخزين قيمة في الذاكرة المؤقتة
        
        Args:
            key: المفتاح
            value: القيمة (يمكن أن تكون أي نوع قابل للتسلسل)
            ttl: وقت الانتهاء بالثواني (اختياري)
        
        Returns:
            bool: True إذا تم التخزين بنجاح
        """
        try:
            serialized_value = json.dumps(value, ensure_ascii=False)
            
            if self.use_redis and self.redis_client:
                if ttl:
                    self.redis_client.setex(key, ttl, serialized_value)
                else:
                    self.redis_client.set(key, serialized_value)
            else:
                # التخزين المحلي
                expire_time = time.time() + ttl if ttl else None
                self.local_cache[key] = {
                    'value': serialized_value,
                    'expire_time': expire_time
                }
            
            logger.debug(f"تم تخزين المفتاح: {key} (TTL: {ttl}s)")
            return True
            
        except Exception as e:
            logger.error(f"خطأ في تخزين القيمة: {e}")
            return False
    
    def get(self, key: str, default: Any = None) -> Any:
        """
        استرجاع قيمة من الذاكرة المؤقتة
        
        Args:
            key: المفتاح
            default: القيمة الافتراضية إذا لم يوجد المفتاح
        
        Returns:
            Any: القيمة المسترجعة أو القيمة الافتراضية
        """
        try:
            if self.use_redis and self.redis_client:
                serialized_value = self.redis_client.get(key)
                if serialized_value is None:
                    return default
            else:
                # الاسترجاع من التخزين المحلي
                if key not in self.local_cache:
                    return default
                
                cache_item = self.local_cache[key]
                
                # التحقق من انتهاء الصلاحية
                if (cache_item['expire_time'] and 
                    time.time() > cache_item['expire_time']):
                    del self.local_cache[key]
                    return default
                
                serialized_value = cache_item['value']
            
            # إعادة القيمة إلى نوعها الأصلي
            return json.loads(serialized_value)
            
        except Exception as e:
            logger.error(f"خطأ في استرجاع القيمة: {e}")
            return default
    
    def delete(self, key: str) -> bool:
        """
        حذف مفتاح من الذاكرة المؤقتة
        
        Args:
            key: المفتاح المراد حذفه
        
        Returns:
            bool: True إذا تم الحذف بنجاح
        """
        try:
            if self.use_redis and self.redis_client:
                deleted = self.redis_client.delete(key) > 0
            else:
                deleted = key in self.local_cache
                if deleted:
                    del self.local_cache[key]
            
            if deleted:
                logger.debug(f"تم حذف المفتاح: {key}")
            else:
                logger.debug(f"المفتاح غير موجود: {key}")
            
            return deleted
            
        except Exception as e:
            logger.error(f"خطأ في حذف المفتاح: {e}")
            return False
    
    def exists(self, key: str) -> bool:
        """
        التحقق من وجود مفتاح في الذاكرة المؤقتة
        
        Args:
            key: المفتاح المراد التحقق منه
        
        Returns:
            bool: True إذا كان المفتاح موجوداً
        """
        try:
            if self.use_redis and self.redis_client:
                return self.redis_client.exists(key) > 0
            else:
                if key not in self.local_cache:
                    return False
                
                # التحقق من انتهاء الصلاحية
                cache_item = self.local_cache[key]
                if (cache_item['expire_time'] and 
                    time.time() > cache_item['expire_time']):
                    del self.local_cache[key]
                    return False
                
                return True
                
        except Exception as e:
            logger.error(f"خطأ في التحقق من المفتاح: {e}")
            return False
    
    def increment(self, key: str, amount: int = 1) -> Optional[int]:
        """
        زيادة قيمة رقمية في الذاكرة المؤقتة
        
        Args:
            key: المفتاح
            amount: المقدار المراد زيادته
        
        Returns:
            Optional[int]: القيمة الجديدة أو None إذا فشلت
        """
        try:
            if self.use_redis and self.redis_client:
                return self.redis_client.incrby(key, amount)
            else:
                current = self.get(key, 0)
                if not isinstance(current, (int, float)):
                    return None
                
                new_value = current + amount
                self.set(key, new_value)
                return new_value
                
        except Exception as e:
            logger.error(f"خطأ في زيادة القيمة: {e}")
            return None
    
    def get_ttl(self, key: str) -> Optional[int]:
        """
        الحصول على الوقت المتبقي للمفتاح بالثواني
        
        Args:
            key: المفتاح
        
        Returns:
            Optional[int]: الوقت المتبقي بالثواني أو None إذا لم يكن له وقت انتهاء
        """
        try:
            if self.use_redis and self.redis_client:
                ttl = self.redis_client.ttl(key)
                return ttl if ttl >= 0 else None
            else:
                if key not in self.local_cache:
                    return None
                
                cache_item = self.local_cache[key]
                if not cache_item['expire_time']:
                    return None
                
                remaining = cache_item['expire_time'] - time.time()
                return int(remaining) if remaining > 0 else None
                
        except Exception as e:
            logger.error(f"خطأ في الحصول على TTL: {e}")
            return None
    
    def clear_expired(self) -> int:
        """
        مسح العناصر المنتهية الصلاحية من التخزين المحلي
        
        Returns:
            int: عدد العناصر التي تم مسحها
        """
        if self.use_redis:
            return 0  # Redis يدير انتهاء الصلاحية تلقائياً
        
        expired_keys = []
        current_time = time.time()
        
        for key, item in self.local_cache.items():
            if item['expire_time'] and current_time > item['expire_time']:
                expired_keys.append(key)
        
        for key in expired_keys:
            del self.local_cache[key]
        
        logger.info(f"تم مسح {len(expired_keys)} عنصر منتهي الصلاحية")
        return len(expired_keys)
    
    def get_stats(self) -> Dict[str, Any]:
        """
        الحصول على إحصائيات التخزين المؤقت
        
        Returns:
            Dict[str, Any]: الإحصائيات
        """
        try:
            if self.use_redis and self.redis_client:
                # إحصائيات Redis
                info = self.redis_client.info()
                return {
                    'type': 'redis',
                    'connected': True,
                    'keys_count': info['db0']['keys'] if 'db0' in info else 0,
                    'memory_used': info['used_memory_human'],
                    'uptime': info['uptime_in_seconds']
                }
            else:
                # إحصائيات التخزين المحلي
                expired_count = sum(
                    1 for item in self.local_cache.values() 
                    if item['expire_time'] and time.time() > item['expire_time']
                )
                
                return {
                    'type': 'local',
                    'connected': False,
                    'keys_count': len(self.local_cache),
                    'expired_keys': expired_count,
                    'memory_usage': 'N/A'
                }
                
        except Exception as e:
            logger.error(f"خطأ في الحصول على الإحصائيات: {e}")
            return {'error': str(e)}

# إنشاء instance عالمي
cache_manager = CacheManager()

# ديكورator للتخزين المؤقت
def cached(ttl: int = 300, key_prefix: str = "cache"):
    """
    ديكورator لتخزين نتائج الدالة مؤقتاً
    
    Args:
        ttl: وقت الانتهاء بالثواني
        key_prefix: بادئة المفتاح
    
    Returns:
        function: الدالة المزينة
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # إنشاء مفتاح فريد بناء على الدالة ومدخلاتها
            func_name = func.__name__
            args_str = str(args)
            kwargs_str = str(sorted(kwargs.items()))
            cache_key = f"{key_prefix}:{func_name}:{hash(args_str + kwargs_str)}"
            
            # محاولة الاسترجاع من الذاكرة المؤقتة
            cached_result = cache_manager.get(cache_key)
            if cached_result is not None:
                logger.debug(f"تم استرجاع النتيجة من الذاكرة المؤقتة: {cache_key}")
                return cached_result
            
            # تنفيذ الدالة الأصلية
            result = func(*args, **kwargs)
            
            # تخزين النتيجة في الذاكرة المؤقتة
            cache_manager.set(cache_key, result, ttl)
            logger.debug(f"تم تخزين النتيجة في الذاكرة المؤقتة: {cache_key}")
            
            return result
        return wrapper
    return decorator

# مثال للاستخدام
if __name__ == "__main__":
    # اختبار مدير التخزين المؤقت
    cache = CacheManager()
    
    # تخزين قيمة
    cache.set("test_key", {"message": "Hello, World!", "timestamp": get_timestamp()}, ttl=60)
    
    # استرجاع قيمة
    result = cache.get("test_key")
    print("القيمة المسترجعة:", result)
    
    # التحقق من الوجود
    exists = cache.exists("test_key")
    print("المفتاح موجود:", exists)
    
    # الحصول على الإحصائيات
    stats = cache.get_stats()
    print("الإحصائيات:", stats)
