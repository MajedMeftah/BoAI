import React, { useState } from 'react';

const LearningPage = () => {
  const [selectedCategory, setSelectedCategory] = useState('programming');

  const categories = [
    {
      id: 'programming',
      title: 'البرمجة',
      icon: 'fa-code',
      color: 'blue',
      topics: [
        {
          title: 'أساسيات البرمجة',
          description: 'تعلم المفاهيم الأساسية للبرمجة والخوارزميات',
          level: 'مبتدئ',
          duration: '4 أسابيع',
          progress: 25
        },
        {
          title: 'بايثون للمبتدئين',
          description: 'ابدأ رحلتك في لغة Python من الصفر',
          level: 'مبتدئ',
          duration: '6 أسابيع',
          progress: 10
        },
        {
          title: 'تطوير الويب',
          description: 'HTML, CSS, JavaScript وبناء مواقع تفاعلية',
          level: 'متوسط',
          duration: '8 أسابيع',
          progress: 0
        },
        {
          title: 'قواعد البيانات',
          description: 'SQL, MongoDB وإدارة البيانات',
          level: 'متوسط',
          duration: '5 أسابيع',
          progress: 0
        }
      ]
    },
    {
      id: 'math',
      title: 'الرياضيات',
      icon: 'fa-calculator',
      color: 'green',
      topics: [
        {
          title: 'الجبر الأساسي',
          description: 'المعادلات والمتباينات والدوال',
          level: 'مبتدئ',
          duration: '3 أسابيع',
          progress: 40
        },
        {
          title: 'حساب التفاضل',
          description: 'النهايات والمشتقات والتكامل',
          level: 'متوسط',
          duration: '6 أسابيع',
          progress: 15
        },
        {
          title: 'الإحصاء والاحتمالات',
          description: 'تحليل البيانات والتوزيعات الاحتمالية',
          level: 'متوسط',
          duration: '4 أسابيع',
          progress: 0
        }
      ]
    },
    {
      id: 'science',
      title: 'العلوم',
      icon: 'fa-flask',
      color: 'purple',
      topics: [
        {
          title: 'الفيزياء الأساسية',
          description: 'الميكانيكا والديناميكا الحرارية',
          level: 'مبتدئ',
          duration: '5 أسابيع',
          progress: 20
        },
        {
          title: 'الكيمياء العضوية',
          description: 'المركبات العضوية والتفاعلات',
          level: 'متوسط',
          duration: '6 أسابيع',
          progress: 5
        },
        {
          title: 'علم الأحياء',
          description: 'الخلية والوراثة والتطور',
          level: 'مبتدئ',
          duration: '4 أسابيع',
          progress: 0
        }
      ]
    },
    {
      id: 'languages',
      title: 'اللغات',
      icon: 'fa-language',
      color: 'orange',
      topics: [
        {
          title: 'الإنجليزية للأعمال',
          description: 'المصطلحات والتواصل المهني',
          level: 'متوسط',
          duration: '8 أسابيع',
          progress: 30
        },
        {
          title: 'اللغة العربية',
          description: 'قواعد اللغة والتعبير الكتابي',
          level: 'مبتدئ',
          duration: '6 أسابيع',
          progress: 60
        }
      ]
    }
  ];

  const selectedCategoryData = categories.find(cat => cat.id === selectedCategory);

  const ProgressBar = ({ progress }) => (
    <div className="w-full bg-gray-200 dark:bg-gray-700 rounded-full h-2">
      <div
        className="bg-blue-500 h-2 rounded-full transition-all duration-300"
        style={{ width: `${progress}%` }}
      ></div>
    </div>
  );

  return (
    <div className="min-h-screen bg-gray-50 dark:bg-gray-900">
      <div className="max-w-7xl mx-auto p-6">
        {/* Header */}
        <div className="text-center mb-8">
          <h1 className="text-3xl font-bold text-gray-900 dark:text-white mb-4">
            مركز التعلم
          </h1>
          <p className="text-gray-600 dark:text-gray-400 text-lg">
            اختر مجال التعلم الذي يناسبك وابدأ رحلتك التعليمية
          </p>
        </div>

        {/* Category Selection */}
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-8">
          {categories.map((category) => (
            <button
              key={category.id}
              onClick={() => setSelectedCategory(category.id)}
              className={`p-4 rounded-2xl transition-all duration-300 ${
                selectedCategory === category.id
                  ? `bg-${category.color}-500 text-white shadow-lg transform scale-105`
                  : 'bg-white dark:bg-gray-800 text-gray-700 dark:text-gray-300 hover:shadow-md'
              }`}
            >
              <div className="flex flex-col items-center space-y-2">
                <i className={`fas ${category.icon} text-2xl`}></i>
                <span className="font-semibold">{category.title}</span>
              </div>
            </button>
          ))}
        </div>

        {/* Learning Topics */}
        <div className="bg-white dark:bg-gray-800 rounded-2xl shadow-xl p-6">
          <div className="flex items-center space-x-3 mb-6">
            <div className={`w-12 h-12 bg-${selectedCategoryData.color}-500 rounded-lg flex items-center justify-center`}>
              <i className={`fas ${selectedCategoryData.icon} text-white text-xl`}></i>
            </div>
            <div>
              <h2 className="text-2xl font-bold text-gray-900 dark:text-white">
                {selectedCategoryData.title}
              </h2>
              <p className="text-gray-600 dark:text-gray-400">
                {selectedCategoryData.topics.length} مسار تعليمي
              </p>
            </div>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            {selectedCategoryData.topics.map((topic, index) => (
              <div
                key={index}
                className="bg-gray-50 dark:bg-gray-700 rounded-xl p-5 hover:shadow-md transition-shadow"
              >
                <div className="flex justify-between items-start mb-4">
                  <div>
                    <h3 className="font-semibold text-gray-900 dark:text-white text-lg mb-2">
                      {topic.title}
                    </h3>
                    <p className="text-gray-600 dark:text-gray-400 text-sm mb-3">
                      {topic.description}
                    </p>
                  </div>
                  <span className={`px-2 py-1 rounded-full text-xs font-medium ${
                    topic.level === 'مبتدئ' 
                      ? 'bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-200'
                      : 'bg-blue-100 text-blue-800 dark:bg-blue-900 dark:text-blue-200'
                  }`}>
                    {topic.level}
                  </span>
                </div>

                <div className="space-y-3">
                  <div className="flex justify-between items-center text-sm text-gray-600 dark:text-gray-400">
                    <span>التقدم</span>
                    <span>{topic.progress}%</span>
                  </div>
                  <ProgressBar progress={topic.progress} />
                  
                  <div className="flex justify-between items-center text-sm">
                    <span className="text-gray-600 dark:text-gray-400">
                      <i className="fas fa-clock mr-1"></i>
                      {topic.duration}
                    </span>
                    <button className="px-4 py-2 bg-blue-500 hover:bg-blue-600 text-white rounded-lg text-sm transition-colors">
                      {topic.progress > 0 ? 'استمر' : 'ابدأ'}
                    </button>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Quick Actions */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mt-8">
          <div className="bg-gradient-to-r from-blue-500 to-purple-600 rounded-2xl p-6 text-white">
            <div className="flex items-center space-x-3 mb-4">
              <i className="fas fa-trophy text-2xl"></i>
              <h3 className="font-semibold text-lg">إنجازاتك</h3>
            </div>
            <p className="text-blue-100 mb-4">تابع تقدمك واحصل على شهادات</p>
            <button className="px-4 py-2 bg-white text-blue-600 rounded-lg text-sm font-medium hover:bg-blue-50 transition-colors">
              عرض الإنجازات
            </button>
          </div>

          <div className="bg-gradient-to-r from-green-500 to-teal-600 rounded-2xl p-6 text-white">
            <div className="flex items-center space-x-3 mb-4">
              <i className="fas fa-chart-line text-2xl"></i>
              <h3 className="font-semibold text-lg">الإحصائيات</h3>
            </div>
            <p className="text-green-100 mb-4">تحليل أدائك وتقدمك التعليمي</p>
            <button className="px-4 py-2 bg-white text-green-600 rounded-lg text-sm font-medium hover:bg-green-50 transition-colors">
              عرض الإحصائيات
            </button>
          </div>

          <div className="bg-gradient-to-r from-orange-500 to-red-600 rounded-2xl p-6 text-white">
            <div className="flex items-center space-x-3 mb-4">
              <i className="fas fa-question-circle text-2xl"></i>
              <h3 className="font-semibold text-lg">المساعدة</h3>
            </div>
            <p className="text-orange-100 mb-4">احصل على دعم ومساعدة فورية</p>
            <button className="px-4 py-2 bg-white text-orange-600 rounded-lg text-sm font-medium hover:bg-orange-50 transition-colors">
              طلب المساعدة
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default LearningPage;
