# 📚 توثيق واجهات برمجة التطبيقات (API) - BoAI

## 🔌 نظرة عامة

واجهات برمجة التطبيقات في BoAI مبنية باستخدام FastAPI وتدعم RESTful APIs وWebSocket للتواصل في الوقت الحقيقي.

## 🚀 نقاط النهاية الأساسية

### 1. واجهة الدردشة (Chat API)

#### إرسال رسالة جديدة
```http
POST /api/v1/chat/send
```

**المعاملات:**
```json
{
  "message": "string",
  "session_id": "string (optional)",
  "user_id": "string (optional)"
}
```

**الرد:**
```json
{
  "response": "string",
  "session_id": "string",
  "timestamp": "2024-01-01T00:00:00Z",
  "message_id": "string"
}
```

#### الحصول على تاريخ المحادثة
```http
GET /api/v1/chat/history?session_id={session_id}
```

**الرد:**
```json
{
  "session_id": "string",
  "messages": [
    {
      "message": "string",
      "sender": "user|assistant",
      "timestamp": "2024-01-01T00:00:00Z"
    }
  ]
}
```

### 2. واجهة التعلم (Learning API)

#### الحصول على توصيات التعلم
```http
GET /api/v1/learning/recommendations?user_id={user_id}
```

**الرد:**
```json
{
  "recommendations": [
    {
      "topic": "string",
      "difficulty": "beginner|intermediate|advanced",
      "resources": [
        {
          "type": "article|video|exercise",
          "title": "string",
          "url": "string",
          "duration": "number (minutes)"
        }
      ]
    }
  ]
}
```

#### تحديث تقدم التعلم
```http
POST /api/v1/learning/progress
```

**المعاملات:**
```json
{
  "user_id": "string",
  "topic": "string",
  "progress": 0.75,
  "completed": false
}
```

### 3. واجهة التقييم (Evaluation API)

#### تقييم جودة الإجابة
```http
POST /api/v1/evaluation/quality
```

**المعاملات:**
```json
{
  "question": "string",
  "answer": "string",
  "model_used": "string"
}
```

**الرد:**
```json
{
  "score": 0.85,
  "feedback": "string",
  "improvement_suggestions": ["string"]
}
```

## 🔐 المصادقة والأمان

### مصادقة Bearer Token
```http
Authorization: Bearer {api_key}
```

### توليد API Key
```http
POST /api/v1/auth/generate-key
```

**المعاملات:**
```json
{
  "user_id": "string",
  "permissions": ["chat", "learning", "evaluation"]
}
```

**الرد:**
```json
{
  "api_key": "string",
  "expires_at": "2024-12-31T23:59:59Z"
}
```

## 🌐 WebSocket للدردشة المباشرة

### الاتصال
```javascript
const ws = new WebSocket('ws://localhost:8000/ws/chat');

ws.onmessage = (event) => {
  const data = JSON.parse(event.data);
  console.log('Received:', data);
};
```

### إرسال رسالة
```javascript
ws.send(JSON.stringify({
  type: 'message',
  content: 'Hello BoAI',
  session_id: 'current-session-id'
}));
```

### أنواع الرسائل المدعومة
- `message` - رسالة نصية
- `typing` - مؤشر الكتابة
- `session_start` - بدء جلسة جديدة
- `session_end` - إنهاء الجلسة

## 📊 إحصائيات واستخدام API

### الحصول على إحصائيات الاستخدام
```http
GET /api/v1/stats/usage?period=7d
```

**الرد:**
```json
{
  "total_requests": 1500,
  "successful_requests": 1450,
  "failed_requests": 50,
  "average_response_time": 120,
  "endpoint_usage": {
    "/api/v1/chat/send": 800,
    "/api/v1/learning/recommendations": 400,
    "/api/v1/evaluation/quality": 300
  }
}
```

## 🛠️ أمثلة الاستخدام

### مثال باستخدام Python
```python
import requests
import json

BASE_URL = "http://localhost:8000"

def send_message(message, api_key):
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "message": message,
        "session_id": "user-123-session"
    }
    
    response = requests.post(
        f"{BASE_URL}/api/v1/chat/send",
        headers=headers,
        json=payload
    )
    
    return response.json()

# استخدام الدالة
result = send_message("كيف يمكنني تعلم Python؟", "your_api_key_here")
print(result["response"])
```

### مثال باستخدام JavaScript
```javascript
async function getLearningRecommendations(userId, apiKey) {
  const response = await fetch(
    `http://localhost:8000/api/v1/learning/recommendations?user_id=${userId}`,
    {
      headers: {
        'Authorization': `Bearer ${apiKey}`
      }
    }
  );
  
  return await response.json();
}

// استخدام الدالة
const recommendations = await getLearningRecommendations('user-123', 'your_api_key');
console.log(recommendations);
```

## ⚠️ حدود الاستخدام ونظام الحصص

- **معدل الطلبات**: 100 طلب/دقيقة لكل مستخدم
- **حجم الرسالة**: 4000 حرف كحد أقصى
- **جلسات متزامنة**: 5 جلسات متزامنة لكل مستخدم
- **تخزين المحادثات**: 30 يوم حفظ تلقائي

## 🔧 إدارة الأخطاء

### رموز الحالة الشائعة

- `200 OK` - الطلب ناجح
- `400 Bad Request` - معاملات غير صحيحة
- `401 Unauthorized` - مصادقة فاشلة
- `403 Forbidden` - صلاحيات غير كافية
- `429 Too Many Requests` - تجاوز حد الطلبات
- `500 Internal Server Error` - خطأ في الخادم

### هيكل رسالة الخطأ
```json
{
  "error": {
    "code": "error_code",
    "message": "وصف الخطأ",
    "details": "معلومات إضافية (اختياري)"
  }
}
```

## 🚀 أفضل الممارسات

1. **التخزين المؤقت**: خزن الردود محلياً لتقليل الطلبات
2. **معالجة الأخطاء**: استخدم try-catch حول جميع استدعاءات API
3. **إعادة المحاولة**: أعد المحاولة تلقائياً للأخطاء المؤقتة
4. **التحقق من الصحة**: تحقق من صحة المعاملات قبل الإرسال
5. **التسجيل**: سجل جميع عمليات API لأغراض التصحيح

## 📈 مراقبة الأداء

### مقاييس الأداء الموصى بها
- وقت استجابة أقل من 200ms
- معدل نجاح أعلى من 99%
- استخدام ذاكرة أقل من 512MB
- وقت تشغيل مستمر 99.9%

### أدوات المراقبة
- **Prometheus** - جمع المقاييس
- **Grafana** - لوحات التحكم
- **Sentry** - تتبع الأخطاء
- **Logstash** - معالجة السجلات

---

**ملاحظة**: هذه الواجهات قيد التطوير النشط وقد تخضع لتغييرات. يرجى مراجعة هذا المستند بانتظام للتحديثات.
