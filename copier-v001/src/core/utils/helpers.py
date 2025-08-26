"""
أدوات مساعدة لـ BoAI - دوال مساعدة عامة

هذا الملف يحتوي على دوال مساعدة عامة يمكن استخدامها
في جميع أنحاء المشروع لتبسيط المهام الشائعة
"""

import logging
import json
import uuid
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional, Union
import hashlib
import re
from pathlib import Path

# إعداد التسجيل
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def generate_uuid() -> str:
    """
    إنشاء معرف فريد عالمي (UUID)
    
    Returns:
        str: UUID كسلسلة نصية
    """
    return str(uuid.uuid4())

def get_timestamp() -> str:
    """
    الحصول على الطابع الزمني الحالي بصيغة ISO
    
    Returns:
        str: الطابع الزمني بصيغة ISO 8601
    """
    return datetime.now().isoformat()

def format_timestamp(timestamp: Union[str, datetime]) -> str:
    """
    تنسيق الطابع الزمني بصيغة قابلة للقراءة
    
    Args:
        timestamp: الطابع الزمني (سلسلة أو كائن datetime)
    
    Returns:
        str: الطابع الزمني المنسق
    """
    if isinstance(timestamp, str):
        timestamp = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
    
    return timestamp.strftime("%Y-%m-%d %H:%M:%S")

def calculate_hash(data: str, algorithm: str = "sha256") -> str:
    """
    حساب التجزئة للبيانات
    
    Args:
        data: البيانات المراد تجزئتها
        algorithm: خوارزمية التجزئة (md5, sha1, sha256, sha512)
    
    Returns:
        str: قيمة التجزئة
    """
    hash_func = getattr(hashlib, algorithm)()
    hash_func.update(data.encode('utf-8'))
    return hash_func.hexdigest()

def validate_email(email: str) -> bool:
    """
    التحقق من صحة عنوان البريد الإلكتروني
    
    Args:
        email: عنوان البريد الإلكتروني
    
    Returns:
        bool: True إذا كان البريد الإلكتروني صالحاً
    """
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def validate_password(password: str) -> Dict[str, bool]:
    """
    التحقق من قوة كلمة المرور
    
    Args:
        password: كلمة المرور المراد التحقق منها
    
    Returns:
        Dict[str, bool]: نتائج التحقق
    """
    results = {
        'length': len(password) >= 8,
        'has_uppercase': bool(re.search(r'[A-Z]', password)),
        'has_lowercase': bool(re.search(r'[a-z]', password)),
        'has_digit': bool(re.search(r'\d', password)),
        'has_special': bool(re.search(r'[!@#$%^&*(),.?":{}|<>]', password)),
        'no_spaces': ' ' not in password
    }
    
    results['is_valid'] = all(results.values())
    return results

def sanitize_input(input_str: str) -> str:
    """
    تنظيف وإزالة الأحرف الخطرة من المدخلات
    
    Args:
        input_str: السلسلة المدخلة
    
    Returns:
        str: السلسلة النظيفة
    """
    if not input_str:
        return ""
    
    # إزالة علامات HTML/XML
    cleaned = re.sub(r'<[^>]*>', '', input_str)
    
    # إزالة أحرف التحكم
    cleaned = re.sub(r'[\x00-\x1F\x7F]', '', cleaned)
    
    # Trim المسافات الزائدة
    cleaned = cleaned.strip()
    
    return cleaned

def truncate_text(text: str, max_length: int = 100, suffix: str = "...") -> str:
    """
    تقصير النص إذا تجاوز الطول المسموح
    
    Args:
        text: النص الأصلي
        max_length: الطول الأقصى المسموح
        suffix: اللاحقة لإضافتها إذا تم التقصير
    
    Returns:
        str: النص المقصوص
    """
    if len(text) <= max_length:
        return text
    
    return text[:max_length - len(suffix)] + suffix

def parse_json_safe(json_str: str, default: Any = None) -> Any:
    """
    تحليل JSON بشكل آمن مع التعامل مع الأخطاء
    
    Args:
        json_str: سلسلة JSON
        default: القيمة الافتراضية في حالة الخطأ
    
    Returns:
        Any: الكائن المحلل أو القيمة الافتراضية
    """
    try:
        return json.loads(json_str)
    except (json.JSONDecodeError, TypeError):
        return default

def to_json_safe(obj: Any, default: str = "{}") -> str:
    """
    تحويل الكائن إلى JSON بشكل آمن
    
    Args:
        obj: الكائن المراد تحويله
        default: القيمة الافتراضية في حالة الخطأ
    
    Returns:
        str: سلسلة JSON أو القيمة الافتراضية
    """
    try:
        return json.dumps(obj, ensure_ascii=False, default=str)
    except (TypeError, ValueError):
        return default

def deep_merge_dicts(dict1: Dict, dict2: Dict) -> Dict:
    """
    دمج قاموسين بشكل عميق (recursive merge)
    
    Args:
        dict1: القاموس الأول
        dict2: القاموس الثاني
    
    Returns:
        Dict: القاموس المدمج
    """
    result = dict1.copy()
    
    for key, value in dict2.items():
        if (key in result and isinstance(result[key], dict) 
            and isinstance(value, dict)):
            result[key] = deep_merge_dicts(result[key], value)
        else:
            result[key] = value
    
    return result

def get_file_size(file_path: Union[str, Path]) -> str:
    """
    الحصول على حجم الملف بصيغة قابلة للقراءة
    
    Args:
        file_path: مسار الملف
    
    Returns:
        str: حجم الملف بصيغة مقروءة (مثل 2.5 MB)
    """
    path = Path(file_path)
    if not path.exists():
        return "0 B"
    
    size_bytes = path.stat().st_size
    
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if size_bytes < 1024.0:
            return f"{size_bytes:.1f} {unit}"
        size_bytes /= 1024.0
    
    return f"{size_bytes:.1f} PB"

def format_duration(seconds: int) -> str:
    """
    تنسيق المدة الزمنية بصيغة مقروءة
    
    Args:
        seconds: عدد الثواني
    
    Returns:
        str: المدة المنسقة (مثل 2h 30m 15s)
    """
    if seconds < 60:
        return f"{seconds}s"
    
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    days, hours = divmod(hours, 24)
    
    parts = []
    if days > 0:
        parts.append(f"{days}d")
    if hours > 0:
        parts.append(f"{hours}h")
    if minutes > 0:
        parts.append(f"{minutes}m")
    if seconds > 0:
        parts.append(f"{seconds}s")
    
    return " ".join(parts)

def chunk_list(lst: List[Any], chunk_size: int) -> List[List[Any]]:
    """
    تقسيم القائمة إلى قطع أصغر
    
    Args:
        lst: القائمة الأصلية
        chunk_size: حجم كل قطعة
    
    Returns:
        List[List[Any]]: قائمة القطع
    """
    return [lst[i:i + chunk_size] for i in range(0, len(lst), chunk_size)]

def is_valid_url(url: str) -> bool:
    """
    التحقق من صحة عنوان URL
    
    Args:
        url: عنوان URL المراد التحقق منه
    
    Returns:
        bool: True إذا كان العنوان صالحاً
    """
    pattern = r'^(https?|ftp)://[^\s/$.?#].[^\s]*$'
    return re.match(pattern, url) is not None

def generate_random_filename(extension: str = "") -> str:
    """
    إنشاء اسم ملف عشوائي
    
    Args:
        extension: امتداد الملف (اختياري)
    
    Returns:
        str: اسم الملف العشوائي
    """
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    random_str = uuid.uuid4().hex[:8]
    
    filename = f"{timestamp}_{random_str}"
    if extension:
        if not extension.startswith('.'):
            extension = '.' + extension
        filename += extension
    
    return filename

# مثال للاستخدام
if __name__ == "__main__":
    # اختبار الدوال
    print(f"UUID: {generate_uuid()}")
    print(f"Timestamp: {get_timestamp()}")
    print(f"Email validation: {validate_email('test@example.com')}")
    print(f"Password validation: {validate_password('StrongPass123!')}")
    print(f"Truncated text: {truncate_text('This is a very long text that needs to be truncated', 20)}")
