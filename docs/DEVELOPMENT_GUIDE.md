# دليل تطوير BoAI

## 📋 نظرة عامة

هذا الدليل يشرح كيفية تطوير وإضافة ميزات جديدة لمشروع BoAI، مع التركيز على أفضل الممارسات وهيكلية المشروع.

## 🏗️ هيكلية المشروع

### الهيكلية العامة
```
BoAI/
├── src/
│   ├── api/                 # واجهات برمجة التطبيقات
│   │   ├── routers/         # مسارات API
│   │   ├── schemas/         # مخططات Pydantic
│   │   └── main.py          # التطبيق الرئيسي
│   ├── core/                # النواة الأساسية
│   │   ├── models/          # إدارة النماذج
│   │   ├── nlp/             # معالجة اللغة
│   │   ├── learning/        # نظام التعلم الذاتي
│   │   ├── database/        # قواعد البيانات
│   │   └── utils/           # أدوات مساعدة
│   ├── frontend/            # الواجهة الأمامية
│   │   ├── components/      # مكونات React
│   │   ├── pages/           # صفحات التطبيق
│   │   └── styles/          # التنسيقات
│   └── tests/               # الاختبارات
├── docker/                  # تكوين Docker
├── docs/                    # التوثيق
└── data/                    # البيانات
```

## 🛠️ إعداد بيئة التطوير

### 1. المتطلبات الأساسية
```bash
# تثبيت Python 3.11+
python --version

# تثبيت Node.js 18+
node --version

# تثبيت Docker و Docker Compose
docker --version
docker-compose --version
```

### 2. استنساخ المشروع
```bash
git clone https://github.com/your-username/BoAI.git
cd BoAI
```

### 3. إعداد البيئة الافتراضية
```bash
# إنشاء بيئة افتراضية
python -m venv venv

# تفعيل البيئة
# Linux/Mac:
source venv/bin/activate

# Windows:
venv\Scripts\activate
```

### 4. تثبيت المتطلبات
```bash
# تثبيت متطلبات Python
pip install -r requirements.txt

# تثبيت متطلبات الواجهة الأمامية
cd src/frontend
npm install
cd ../..
```

### 5. تكوين البيئة
```bash
# نسخ ملف البيئة
cp .env.example .env

# تعديل الإعدادات في .env
nano .env  # أو استخدام أي محرر
```

## 🔧 تطوير الميزات الجديدة

### 1. إنشاء فرع جديد
```bash
git checkout develop
git pull origin develop
git checkout -b feature/your-feature-name
```

### 2. هيكلية الميزة الجديدة

#### لإضافة ميزة في الخلفية:
```python
# في src/core/feature_name/
# - service.py       # المنطق الرئيسي
# - models.py        # النماذج (إذا لزم الأمر)
# - schemas.py       # مخططات Pydantic
# - router.py        # مسارات API
```

#### مثال لإضافة خدمة جديدة:
```python
# src/core/learning/advanced_service.py
from typing import List, Optional
from pydantic import BaseModel

class AdvancedLearningRequest(BaseModel):
    user_id: str
    question: str
    context: Optional[str] = None

class AdvancedLearningService:
    def __init__(self):
        self.model = None
        
    async def process_request(self, request: AdvancedLearningRequest):
        """معالجة طلب التعلم المتقدم"""
        # تنفيذ المنطق هنا
        pass
```

#### لإضافة مسار API:
```python
# src/api/routers/advanced_learning.py
from fastapi import APIRouter, HTTPException
from src.core.learning.advanced_service import AdvancedLearningService, AdvancedLearningRequest

router = APIRouter(prefix="/advanced-learning", tags=["Advanced Learning"])
service = AdvancedLearningService()

@router.post("/process")
async def process_learning_request(request: AdvancedLearningRequest):
    try:
        result = await service.process_request(request)
        return {"success": True, "result": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
```

### 3. تسجيل المسار في التطبيق الرئيسي
```python
# src/api/main.py
from .routers import advanced_learning

app.include_router(advanced_learning.router)
```

## 🧪 كتابة الاختبارات

### اختبارات الوحدة
```python
# tests/core/test_advanced_learning.py
import pytest
from src.core.learning.advanced_service import AdvancedLearningService, AdvancedLearningRequest

@pytest.mark.asyncio
async def test_advanced_learning_process():
    service = AdvancedLearningService()
    request = AdvancedLearningRequest(
        user_id="test-user",
        question="كيف يمكنني تحسين أداء الكود؟"
    )
    
    result = await service.process_request(request)
    assert result is not None
    assert "improvement" in result
```

### اختبارات التكامل
```python
# tests/api/test_advanced_learning.py
import pytest
from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)

def test_advanced_learning_endpoint():
    response = client.post("/advanced-learning/process", json={
        "user_id": "test-user",
        "question": "كيف يمكنني تحسين الأداء؟"
    })
    
    assert response.status_code == 200
    assert response.json()["success"] == True
```

## 🎨 تطوير الواجهة الأمامية

### إضافة مكون جديد
```jsx
// src/frontend/components/AdvancedLearning.jsx
import React, { useState } from 'react';

const AdvancedLearning = () => {
    const [input, setInput] = useState('');
    const [response, setResponse] = useState('');

    const handleSubmit = async () => {
        try {
            const res = await fetch('/api/advanced-learning/process', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ question: input })
            });
            const data = await res.json();
            setResponse(data.result);
        } catch (error) {
            console.error('Error:', error);
        }
    };

    return (
        <div className="advanced-learning">
            <textarea value={input} onChange={(e) => setInput(e.target.value)} />
            <button onClick={handleSubmit}>إرسال</button>
            {response && <div className="response">{response}</div>}
        </div>
    );
};

export default AdvancedLearning;
```

## 📝 التوثيق

### توثيق الميزة الجديدة
```markdown
# الميزة المتقدمة للتعلم

## الوظيفة
تقدم تحليلاً متقدماً لأسئلة التعلم مع توصيات مخصصة.

## الاستخدام
```python
from src.core.learning.advanced_service import AdvancedLearningService

service = AdvancedLearningService()
result = await service.process_request(request)
```

## الإعدادات
- `MAX_RESPONSE_LENGTH`: الط الأقصى للرد
- `LEARNING_RATE`: معدل التعلم
```

## 🔍 فحص الجودة

### فحص الكود
```bash
# فحص التنسيق مع black
black src/ --check

# فحص الجودة مع flake8
flake8 src/

# فحص الأمان مع bandit
bandit -r src/
```

### تشغيل الاختبارات
```bash
# جميع الاختبارات
pytest tests/ -v

# اختبارات محددة
pytest tests/core/test_advanced_learning.py -v

# مع التغطية
pytest tests/ --cov=src --cov-report=html
```

## 🔄 دمج التغييرات

### 1. تحديث الفرع
```bash
git checkout develop
git pull origin develop
git checkout feature/your-feature-name
git rebase develop
```

### 2. حل التعارضات (إذا وجدت)
```bash
# بعد rebase، حل التعارضات يدوياً
git add .
git rebase --continue
```

### 3. push التغييرات
```bash
git push origin feature/your-feature-name
```

### 4. إنشاء Pull Request
- الانتقال إلى GitHub
- إنشاء Pull Request من feature branch إلى develop
- مراجعة الكود
- دمج بعد الموافقة

## 🚀 النشر

### النشر في البيئة التطويرية
```bash
# بناء الصور
docker-compose build

# تشغيل الخدمات
docker-compose up -d

# مشاهدة logs
docker-compose logs -f
```

### النشر في الإنتاج
```bash
# استخدام docker-compose.prod.yml
docker-compose -f docker-compose.prod.yml up -d --build

# التحديث
docker-compose -f docker-compose.prod.yml up -d --build --force-recreate
```

## 📊 المراقبة والتصحيح

### مراقبة logs
```bash
# مشاهدة logs حية
docker-compose logs -f api

# logs محددة
docker-compose logs api | grep "ERROR"
```

### المقاييس والأداء
```bash
# مراقبة استخدام الموارد
docker stats

# فحص صحة الخدمات
curl http://localhost:8000/health
```

## 🆘 استكشاف الأخطاء وإصلاحها

### مشاكل شائعة

#### 1. أخطاء في المصادقة
```bash
# التحقق من متغيرات البيئة
echo $DATABASE_URL

# إعادة إنشاء tokens
rm -f .env
cp .env.example .env
```

#### 2. مشاكل في قاعدة البيانات
```bash
# إعادة تهيئة قاعدة البيانات
docker-compose down -v
docker-compose up -d db
```

#### 3. مشاكل في التبعيات
```bash
# إعادة تثبيت المتطلبات
pip install -r requirements.txt --force-reinstall

# تنظيف cache
pip cache purge
```

## 📞 الدعم

- **الإبلاغ عن الأخطاء**: GitHub Issues
- **الأسئلة التقنية**: GitHub Discussions
- **الاتصال المباشر**: فريق التطوير

---

*آخر تحديث: 25 أغسطس 2025*
