# BoAI - منصة الذكاء الاصطناعي التعليمي المفتوحة المصدر

![BoAI Logo](https://img.shields.io/badge/BoAI-Educational%20AI-blue)
![Python](https://img.shields.io/badge/Python-3.11%2B-green)
![FastAPI](https://img.shields.io/badge/FastAPI-0.111.0-lightgreen)
![License](https://img.shields.io/badge/License-MIT-yellow)

BoAI (اختصار لـ Binary Owl AI) هو منصة ذكاء اصطناعي مفتوحة المصدر مصممة خصيصاً للأغراض التعليمية، مع تركيز خاص على تعليم البرمجة والمفاهيم التقنية.

## ✨ المميزات

- **دردشة ذكية**: نظام محادثة متقدم يدعم اللغات المتعددة
- **تعلم البرمجة**: مساعد لتعلم لغات البرمجة المختلفة
- **وضع غير متصل**: عمل بدون اتصال بالإنترنت
- **تعدد اللغات**: دعم العربية، الإنجليزية، والفرنسية
- **واجهات متعددة**: Web، CLI، وAPI
- **مفتوح المصدر**: قابل للتطوير والتعديل

## 🚀 البدء السريع

### المتطلبات المسبقة

- Python 3.11+
- PostgreSQL 14+
- Redis 7+
- Docker (اختياري)

### التثبيت

1. استنساخ المشروع:
```bash
git clone https://github.com/your-username/BoAI.git
cd BoAI
```

2. إنشاء بيئة افتراضية:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# أو
venv\Scripts\activate     # Windows
```

3. تثبيت المتطلبات:
```bash
pip install -r requirements.txt
```

4. إعداد قاعدة البيانات:
```bash
docker run --name boai-db -e POSTGRES_PASSWORD=boai -d postgres:14
docker run --name boai-redis -d redis:7
```

5. تشغيل التطبيق:
```bash
uvicorn src.api.main:app --reload
```

## 📁 هيكلية المشروع

```
BoAI/
├── src/                    # الكود المصدري
│   ├── api/               # واجهات برمجة التطبيقات
│   ├── core/              # النواة الأساسية
│   └── frontend/          # الواجهة الأمامية
├── tests/                 # الاختبارات
├── docker/               # تكوينات Docker
├── docs/                 # التوثيق
└── requirements.txt      # متطلبات Python
```

## 🛠️ التقنيات المستخدمة

### Backend
- **FastAPI**: إطار عمل سريع وحديث لبناء APIs
- **PostgreSQL**: قاعدة البيانات العلائقية
- **Redis**: التخزين المؤقت والجلسات
- **SQLAlchemy**: ORM لقواعد البيانات
- **Transformers**: نماذج معالجة اللغة الطبيعية

### Frontend
- **React/Next.js**: واجهة المستخدم
- **Tailwind CSS**: تنسيق وتصميم
- **TypeScript**: كتابة نوعية آمنة

### DevOps
- **Docker**: حاويات التطبيق
- **GitHub Actions**: CI/CD
- **Prometheus/Grafana**: المراقبة

## 📊 حالات الاستخدام

### للطلاب
- تعلم البرمجة عبر الدردشة التفاعلية
- الحصول على إجابات فورية للأسئلة التقنية
- ممارسة كتابة الأكواد مع التصحيح الآلي

### للمعلمين
- إنشاء محتوى تعليمي تفاعلي
- متابعة تقدم الطلاب
- توليد تمارين وأسئلة تلقائية

### للمطورين
- بناء تطبيقات تعليمية مخصصة
- التكامل مع منصات التعلم الإلكتروني
- تطوير نماذج ذكاء اصطناعي متخصصة

## 🤝 المساهمة

نرحب بمساهمات المجتمع! للمساهمة في المشروع:

1. Fork المشروع
2. إنشاء فرع للميزة الجديدة (`git checkout -b feature/AmazingFeature`)
3. Commit التغييرات (`git commit -m 'Add some AmazingFeature'`)
4. Push إلى الفرع (`git push origin feature/AmazingFeature`)
5. فتح Pull Request

راجع [دليل المساهمة](CONTRIBUTING.md) للمزيد من التفاصيل.

## 📄 الرخصة

هذا المشروع مرخص تحت رخصة MIT - راجع ملف [LICENSE](LICENSE) للتفاصيل.

## 📞 التواصل

- 📧 البريد الإلكتروني: info@boai.dev
- 💬 Discord: [انضم إلى مجتمعنا](https://discord.gg/boai)
- 🐛 الإبلاغ عن الأخطاء: [GitHub Issues](https://github.com/your-username/BoAI/issues)

## 🙏 الشكر

شكر خاص لجميع المساهمين الذين يجعلون هذا المشروع ممكناً!

---

**ملاحظة**: هذا المشروع قيد التطوير النشط. الإصدار 1.0 متوقع في يناير 2026.

⭐ إذا أعجبك المشروع، لا تنسى إعطائه نجمة على GitHub!
