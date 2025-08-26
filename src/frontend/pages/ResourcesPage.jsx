import React, { useState } from 'react';

const ResourcesPage = () => {
  const [selectedCategory, setSelectedCategory] = useState('tutorials');

  const categories = [
    {
      id: 'tutorials',
      title: 'الدروس',
      icon: 'fa-graduation-cap',
      color: 'blue',
      resources: [
        {
          title: 'دورة Python الشاملة',
          description: 'تعلم Python من الصفر إلى الاحتراف مع مشاريع عملية',
          type: 'فيديو',
          duration: '12 ساعة',
          level: 'جميع المستويات',
          rating: 4.8,
          students: 1250
        },
        {
          title: 'أساسيات HTML و CSS',
          description: 'بناء مواقع ويب جميلة وتفاعلية',
          type: 'نصي',
          duration: '8 ساعات',
          level: 'مبتدئ',
          rating: 4.6,
          students: 890
        },
        {
          title: 'JavaScript المتقدم',
          description: 'التفاعلية والخوارزميات في JavaScript',
          type: 'فيديو',
          duration: '15 ساعة',
          level: 'متقدم',
          rating: 4.9,
          students: 670
        }
      ]
    },
    {
      id: 'docs',
      title: 'المستندات',
      icon: 'fa-file-alt',
      color: 'green',
      resources: [
        {
          title: 'وثائق Python الرسمية',
          description: 'المرجع الشامل للغة Python',
          type: 'نصي',
          duration: 'مرجعي',
          level: 'جميع المستويات',
          rating: 4.7,
          students: 2300
        },
        {
          title: 'دليل React.js',
          description: 'التوثيق الرسمي لمكتبة React',
          type: 'نصي',
          duration: 'مرجعي',
          level: 'متوسط',
          rating: 4.8,
          students: 1800
        },
        {
          title: 'SQL المرجعي',
          description: 'كل ما تحتاجه عن قواعد البيانات',
          type: 'نصي',
          duration: 'مرجعي',
          level: 'جميع المستويات',
          rating: 4.5,
          students: 950
        }
      ]
    },
    {
      id: 'examples',
      title: 'الأمثلة',
      icon: 'fa-code',
      color: 'purple',
      resources: [
        {
          title: 'مشاريع Python عملية',
          description: '30 مشروع عملي لتعزيز مهاراتك',
          type: 'كود',
          duration: 'متنوع',
          level: 'متوسط',
          rating: 4.9,
          students: 2100
        },
        {
          title: 'نماذج React جاهزة',
          description: 'مكونات قابلة لإعادة الاستخدام',
          type: 'كود',
          duration: 'متنوع',
          level: 'متوسط',
          rating: 4.7,
          students: 1500
        },
        {
          title: 'أمثلة الخوارزميات',
          description: 'حلول لمشاكل برمجية شائعة',
          type: 'كود',
          duration: 'متنوع',
          level: 'متقدم',
          rating: 4.8,
          students: 1200
        }
      ]
    },
    {
      id: 'cheatsheets',
      title: 'الملخصات',
      icon: 'fa-clipboard-list',
      color: 'orange',
      resources: [
        {
          title: 'ملخص أوامر Git',
          description: 'كل أوامر Git التي تحتاجها',
          type: 'PDF',
          duration: 'سريع',
          level: 'جميع المستويات',
          rating: 4.6,
          students: 2800
        },
        {
          title: 'CSS Cheat Sheet',
          description: 'خصائص CSS وأمثلة عليها',
          type: 'PDF',
          duration: 'سريع',
          level: 'جميع المستويات',
          rating: 4.5,
          students: 1900
        },
        {
          title: 'ملخص Python',
          description: 'بناء الجمل والدوال الأساسية',
          type: 'PDF',
          duration: 'سريع',
          level: 'مبتدئ',
          rating: 4.7,
          students: 2200
        }
      ]
    }
  ];

  const selectedCategoryData = categories.find(cat => cat.id === selectedCategory);

  const getTypeIcon = (type) => {
    switch (type) {
      case 'فيديو': return 'fa-video';
      case 'نصي': return 'fa-file-alt';
      case 'كود': return 'fa-code';
      case 'PDF': return 'fa-file-pdf';
      default: return 'fa-file';
    }
  };

  const getTypeColor = (type) => {
    switch (type) {
      case 'فيديو': return 'red';
      case 'نصي': return 'blue';
      case 'كود': return 'green';
      case 'PDF': return 'orange';
      default: return 'gray';
    }
  };

  return (
    <div className="min-h-screen bg-gray-50 dark:bg-gray-900">
      <div className="max-w-7xl mx-auto p-6">
        {/* Header */}
        <div className="text-center mb-8">
          <h1 className="text-3xl font-bold text-gray-900 dark:text-white mb-4">
            المصادر التعليمية
          </h1>
          <p className="text-gray-600 dark:text-gray-400 text-lg">
            اكتشف مجموعة واسعة من المصادر لتعزيز مهاراتك التعليمية
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

        {/* Resources Grid */}
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
                {selectedCategoryData.resources.length} مصدر متاح
              </p>
            </div>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {selectedCategoryData.resources.map((resource, index) => (
              <div
                key={index}
                className="bg-gray-50 dark:bg-gray-700 rounded-xl p-5 hover:shadow-md transition-shadow group"
              >
                {/* Resource Type Badge */}
                <div className="flex justify-between items-start mb-4">
                  <span className={`px-3 py-1 rounded-full text-xs font-medium bg-${getTypeColor(resource.type)}-100 text-${getTypeColor(resource.type)}-800 dark:bg-${getTypeColor(resource.type)}-900 dark:text-${getTypeColor(resource.type)}-200`}>
                    <i className={`fas ${getTypeIcon(resource.type)} mr-1`}></i>
                    {resource.type}
                  </span>
                  <span className="px-2 py-1 rounded-full text-xs font-medium bg-yellow-100 text-yellow-800 dark:bg-yellow-900 dark:text-yellow-200">
                    <i className="fas fa-star mr-1"></i>
                    {resource.rating}
                  </span>
                </div>

                {/* Resource Content */}
                <div className="mb-4">
                  <h3 className="font-semibold text-gray-900 dark:text-white text-lg mb-2 group-hover:text-blue-600 dark:group-hover:text-blue-400 transition-colors">
                    {resource.title}
                  </h3>
                  <p className="text-gray-600 dark:text-gray-400 text-sm mb-3">
                    {resource.description}
                  </p>
                </div>

                {/* Resource Meta */}
                <div className="space-y-2 text-sm text-gray-600 dark:text-gray-400">
                  <div className="flex items-center justify-between">
                    <span>
                      <i className="fas fa-clock mr-1"></i>
                      {resource.duration}
                    </span>
                    <span>
                      <i className="fas fa-users mr-1"></i>
                      {resource.students.toLocaleString()}
                    </span>
                  </div>
                  
                  <div className="flex items-center justify-between">
                    <span className={`px-2 py-1 rounded-full text-xs ${
                      resource.level === 'مبتدئ' 
                        ? 'bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-200'
                        : resource.level === 'متوسط'
                        ? 'bg-blue-100 text-blue-800 dark:bg-blue-900 dark:text-blue-200'
                        : 'bg-purple-100 text-purple-800 dark:bg-purple-900 dark:text-purple-200'
                    }`}>
                      {resource.level}
                    </span>
                  </div>
                </div>

                {/* Action Button */}
                <button className="w-full mt-4 px-4 py-2 bg-blue-500 hover:bg-blue-600 text-white rounded-lg text-sm font-medium transition-colors flex items-center justify-center space-x-2">
                  <i className="fas fa-download"></i>
                  <span>تحميل المصدر</span>
                </button>
              </div>
            ))}
          </div>
        </div>

        {/* Quick Stats */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mt-8">
          <div className="bg-white dark:bg-gray-800 rounded-2xl p-6 text-center">
            <div className="w-12 h-12 bg-blue-500 rounded-full flex items-center justify-center mx-auto mb-3">
              <i className="fas fa-book text-white text-xl"></i>
            </div>
            <h3 className="text-2xl font-bold text-gray-900 dark:text-white mb-1">156</h3>
            <p className="text-gray-600 dark:text-gray-400">مصدر متاح</p>
          </div>

          <div className="bg-white dark:bg-gray-800 rounded-2xl p-6 text-center">
            <div className="w-12 h-12 bg-green-500 rounded-full flex items-center justify-center mx-auto mb-3">
              <i className="fas fa-users text-white text-xl"></i>
            </div>
            <h3 className="text-2xl font-bold text-gray-900 dark:text-white mb-1">8,742</h3>
            <p className="text-gray-600 dark:text-gray-400">مستخدم نشط</p>
          </div>

          <div className="bg-white dark:bg-gray-800 rounded-2xl p-6 text-center">
            <div className="w-12 h-12 bg-purple-500 rounded-full flex items-center justify-center mx-auto mb-3">
              <i className="fas fa-download text-white text-xl"></i>
            </div>
            <h3 className="text-2xl font-bold text-gray-900 dark:text-white mb-1">24,891</h3>
            <p className="text-gray-600 dark:text-gray-400">تحميل</p>
          </div>

          <div className="bg-white dark:bg-gray-800 rounded-2xl p-6 text-center">
            <div className="w-12 h-12 bg-orange-500 rounded-full flex items-center justify-center mx-auto mb-3">
              <i className="fas fa-star text-white text-xl"></i>
            </div>
            <h3 className="text-2xl font-bold text-gray-900 dark:text-white mb-1">4.7</h3>
            <p className="text-gray-600 dark:text-gray-400">متوسط التقييم</p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ResourcesPage;
