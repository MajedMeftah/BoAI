# BoAI - منصة التعلم الذكي بالذكاء الاصطناعي 🤖📚

![BoAI Logo](https://img.shields.io/badge/BoAI-Intelligent%20Learning-blue?style=for-the-badge)
![Version](https://img.shields.io/badge/version-1.0.0-green?style=for-the-badge)
![License](https://img.shields.io/badge/license-MIT-blue?style=for-the-badge)

منصة تعليمية ذكية تستخدم الذكاء الاصطناعي لتقديم تجربة تعلم مخصصة وتفاعلية للمستخدمين العرب.

## ✨ المميزات الرئيسية

- **💬 دردشة ذكية تفاعلية** - محادثات طبيعية مع مساعد AI متقدم
- **🎯 تعلم مخصص** - مسارات تعلم تكيفية بناءً على مستوى المستخدم
- **📊 تتبع التقدم** - نظام متابعة وتحليل لأداء التعلم
- **🌙 واجهة حديثة** - تصميم عصري يدعم الوضع المظلم والفاتح
- **📱 متجاوب** - يعمل على جميع الأجهزة والشاشات
- **💾 حفظ المحادثات** - تخزين وتصدير تاريخ المحادثات

## 🚀 البدء السريع

### المتطلبات المسبقة

- Node.js 16+ 
- npm أو yarn
- Python 3.8+ (للباكند)
- PostgreSQL (اختياري)

### التثبيت

1. **استنساخ المستودع**
```bash
git clone https://github.com/your-username/BoAI.git
cd BoAI
```

2. **تثبيت الاعتماديات**
```bash
# Frontend dependencies
cd src/frontend
npm install

# Backend dependencies
cd ../..
pip install -r requirements.txt
```

3. **إعداد البيئة**
```bash
cp .env.example .env
# تعديل ملف .env بإضافة المتغيرات الخاصة بك
```

4. **تشغيل التطبيق**
```bash
# تشغيل الباكند
python -m src.api.main

# تشغيل الفرونتند (في terminal آخر)
cd src/frontend
npm run dev
```

## 🛠️ البنية التقنية

### Frontend
- **React 18** - واجهة المستخدم
- **Tailwind CSS** - التصميم والتنسيق
- **Font Awesome** - الأيقونات
- **LocalStorage** - تخزين المحادثات محلياً

### Backend
- **Python 3.8+** - لغة البرمجة الرئيسية
- **FastAPI** - إطار عمل الويب
- **PostgreSQL** - قاعدة البيانات (اختياري)
- **Redis** - التخزين المؤقت
- **Docker** - حاويات التطبيق

### الذكاء الاصطناعي
- **نماذج ML متقدمة** - معالجة اللغة الطبيعية
- **نظام تعلم ذاتي** - تحسين الإجابات باستمرار
- **محرك توصيات** - محتوى مخصص لكل مستخدم

## 📁 هيكل المشروع

```
BoAI/
├── src/
│   ├── frontend/          # واجهة المستخدم
│   │   ├── components/    # مكونات React
│   │   ├── pages/         # صفحات التطبيق
│   │   └── styles/        # ملفات التنسيق
│   ├── api/               # واجهات برمجة التطبيقات
│   │   ├── main.py        # التطبيق الرئيسي
│   │   └── routers/       # مسارات API
│   └── core/              # النواة الأساسية
│       ├── models/        # إدارة النماذج
│       ├── nlp/           # معالجة اللغة
│       ├── learning/      # نظام التعلم
│       └── database/      # إدارة قواعد البيانات
├── docs/                  # التوثيق
├── docker/                # تكوين Docker
└── tests/                 # الاختبارات
```

## 🔧 الإعداد المتقدم

### إعداد قاعدة البيانات

1. **تثبيت PostgreSQL**
```bash
# Ubuntu/Debian
sudo apt-get install postgresql postgresql-contrib

# macOS
brew install postgresql
```

2. **إنشاء قاعدة البيانات**
```sql
CREATE DATABASE boai_db;
CREATE USER boai_user WITH PASSWORD 'your_password';
GRANT ALL PRIVILEGES ON DATABASE boai_db TO boai_user;
```

3. **تكوين الاتصال**
```env
DATABASE_URL=postgresql://boai_user:your_password@localhost:5432/boai_db
```

### إعداد الذكاء الاصطناعي

1. **الحصول على مفتاح API**
```bash
# تسجيل في منصة الذكاء الاصطناعي المفضلة
# إضافة المفتاح إلى .env
AI_API_KEY=your_api_key_here
```

2. **تكوين النماذج**
```python
# في src/core/config.py
MODEL_CONFIG = {
    "default_model": "gpt-3.5-turbo",
    "fallback_model": "text-davinci-003",
    "max_tokens": 2000,
    "temperature": 0.7
}
```

## 🎯 كيفية الاستخدام

### المحادثة الأساسية

1. **فتح التطبيق** في المتصفح (`http://localhost:3000`)
2. **بدء محادثة** جديدة بالضغط على "جلسة جديدة"
3. **كتابة الرسالة** في حقل الإدخال
4. **استلام الرد** من المساعد الذكي

### ميزات متقدمة

- **📋 تصدير المحادثات** - حفظ المحادثات كنص أو PDF
- **🔍 البحث** - البحث في المحادثات السابقة
- **📊 الإحصائيات** - عرض تقارير التقدم
- **⚙️ الإعدادات** - تخصيص تجربة المستخدم

## 🧪 الاختبار

### اختبارات الوحدة
```bash
# Frontend tests
cd src/frontend
npm test

# Backend tests
python -m pytest tests/unit/
```

### اختبارات التكامل
```bash
python -m pytest tests/integration/
```

### اختبارات الأداء
```bash
python -m pytest tests/performance/
```

## 🚀 النشر

### النشر باستخدام Docker

1. **بناء الصورة**
```bash
docker build -t boai-app .
```

2. **تشغيل الحاوية**
```bash
docker run -p 8000:8000 -p 3000:3000 boai-app
```

### النشر على Kubernetes

```bash
kubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/service.yaml
```

## 🤝 المساهمة

نرحب بمساهماتكم! يرجى اتباع الخطوات التالية:

1. عمل Fork للمشروع
2. إنشاء فرع للميزة (`git checkout -b feature/AmazingFeature`)
3. عمل Commit للتغييرات (`git commit -m 'Add some AmazingFeature'`)
4. Push إلى الفرع (`git push origin feature/AmazingFeature`)
5. فتح Pull Request

## 📄 الرخصة

هذا المشروع مرخص تحت رخصة MIT - انظر ملف [LICENSE](LICENSE) للتفاصيل.

## 👥 فريق التطوير

- **المطور الرئيسي** - [اسمك]
- **المصمم** - [اسم المصمم]
- **مدير المشروع** - [اسم المدير]

## 📞 الدعم

- 📧 البريد الإلكتروني: support@boai.com
- 🐛 الإبلاغ عن أخطاء: [GitHub Issues](https://github.com/your-username/BoAI/issues)
- 💬 الدردشة: [Discord Server](https://discord.gg/boai)

## 🔄 التحديثات المستمرة

لمشاهدة آخر التحديثات والتطويرات، تفضل بزيارة [ملف التحديثات](docs/CONTINUOUS_UPDATES.md).

---

**ملاحظة**: هذا المشروع قيد التطوير النشط. قد تتغير بعض الميزات والإعدادات مع التحديثات المستقبلية.
