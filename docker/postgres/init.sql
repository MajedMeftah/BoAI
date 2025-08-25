-- ملف تهيئة قاعدة بيانات BoAI
-- يتم تنفيذ هذا الملف تلقائياً عند أول تشغيل لـ PostgreSQL

-- إنشاء جداول المستخدمين
CREATE TABLE IF NOT EXISTS users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(255) UNIQUE NOT NULL,
    username VARCHAR(100) UNIQUE NOT NULL,
    hashed_password VARCHAR(255) NOT NULL,
    full_name VARCHAR(255),
    role VARCHAR(50) NOT NULL DEFAULT 'learner' CHECK (role IN ('admin', 'tutor', 'learner')),
    is_active BOOLEAN DEFAULT TRUE,
    is_verified BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    last_login TIMESTAMP WITH TIME ZONE
);

-- إنشاء جداول المحادثات
CREATE TABLE IF NOT EXISTS conversations (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    title VARCHAR(500),
    language VARCHAR(10) DEFAULT 'ar',
    model_used VARCHAR(100),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- إنشاء جداول الرسائل
CREATE TABLE IF NOT EXISTS messages (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    conversation_id UUID REFERENCES conversations(id) ON DELETE CASCADE,
    sender_type VARCHAR(20) CHECK (sender_type IN ('user', 'assistant')),
    content TEXT NOT NULL,
    language VARCHAR(10) DEFAULT 'ar',
    tokens_used INTEGER DEFAULT 0,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- إنشاء جداول التقييمات
CREATE TABLE IF NOT EXISTS feedback (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id) ON DELETE SET NULL,
    message_id UUID REFERENCES messages(id) ON DELETE SET NULL,
    rating SMALLINT CHECK (rating BETWEEN 1 AND 5),
    feedback_text TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- إنشاء جداول قاعدة المعرفة (للعمل غير المتصل)
CREATE TABLE IF NOT EXISTS knowledge_base (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    subject VARCHAR(100) NOT NULL,
    language VARCHAR(10) NOT NULL DEFAULT 'ar',
    question TEXT NOT NULL,
    answer TEXT NOT NULL,
    tags TEXT[] DEFAULT '{}',
    usage_count INTEGER DEFAULT 0,
    confidence_score FLOAT DEFAULT 1.0,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- إنشاء جداول إحصائيات الاستخدام
CREATE TABLE IF NOT EXISTS usage_stats (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id) ON DELETE SET NULL,
    endpoint VARCHAR(100) NOT NULL,
    method VARCHAR(10) NOT NULL,
    response_time INTEGER,
    status_code INTEGER,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- إنشاء indexes لتحسين الأداء
CREATE INDEX IF NOT EXISTS idx_users_email ON users(email);
CREATE INDEX IF NOT EXISTS idx_users_username ON users(username);
CREATE INDEX IF NOT EXISTS idx_conversations_user_id ON conversations(user_id);
CREATE INDEX IF NOT EXISTS idx_messages_conversation_id ON messages(conversation_id);
CREATE INDEX IF NOT EXISTS idx_messages_created_at ON messages(created_at);
CREATE INDEX IF NOT EXISTS idx_feedback_user_id ON feedback(user_id);
CREATE INDEX IF NOT EXISTS idx_knowledge_base_subject ON knowledge_base(subject);
CREATE INDEX IF NOT EXISTS idx_knowledge_base_language ON knowledge_base(language);
CREATE INDEX IF NOT EXISTS idx_usage_stats_created_at ON usage_stats(created_at);

-- إدراج بيانات أولية (اختياري)
INSERT INTO users (email, username, hashed_password, full_name, role, is_verified, is_active)
VALUES 
    ('admin@boai.dev', 'admin', '$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW', 'مدير النظام', 'admin', TRUE, TRUE),
    ('tutor@boai.dev', 'tutor', '$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW', 'المعلم المساعد', 'tutor', TRUE, TRUE)
ON CONFLICT (email) DO NOTHING;

-- إدراج بعض بيانات قاعدة المعرفة الأولية
INSERT INTO knowledge_base (subject, language, question, answer, tags, confidence_score)
VALUES 
    ('programming', 'ar', 'ما هي لغة Python؟', 'بايثون هي لغة برمجة عالية المستوى، مفسرة، تفاعلية وموجهة للكائنات. تتميز ببساطة كتابتها وسهولة قراءتها.', '{"python", "برمجة", "لغة"}', 0.95),
    ('programming', 'en', 'What is Python?', 'Python is a high-level, interpreted, interactive and object-oriented programming language. It is known for its simplicity and readability.', '{"python", "programming", "language"}', 0.95),
    ('mathematics', 'ar', 'ما هو الجذر التربيعي؟', 'الجذر التربيعي لعدد ما هو القيمة التي عندما تضرب في نفسها تعطي العدد الأصلي.', '{"رياضيات", "جذر", "تربيعي"}', 0.9)
ON CONFLICT DO NOTHING;

-- تسجيل اكتمال التهيئة
DO $$ 
BEGIN
    RAISE NOTICE 'تم تهيئة قاعدة بيانات BoAI بنجاح في %', CURRENT_TIMESTAMP;
END $$;
