import React, { useState, useEffect } from 'react';

const DashboardPage = () => {
  const [stats, setStats] = useState({
    totalUsers: 1247,
    activeSessions: 89,
    messagesToday: 345,
    learningProgress: 78
  });

  const [recentActivities, setRecentActivities] = useState([
    {
      id: 1,
      user: 'أحمد محمد',
      action: 'بدأ دورة جديدة',
      course: 'تعلم الذكاء الاصطناعي',
      time: 'منذ 5 دقائق',
      icon: 'fa-graduation-cap',
      color: 'text-green-500'
    },
    {
      id: 2,
      user: 'سارة علي',
      action: 'أكملت اختبار',
      course: 'أساسيات البرمجة',
      time: 'منذ 15 دقيقة',
      icon: 'fa-check-circle',
      color: 'text-blue-500'
    },
    {
      id: 3,
      user: 'محمد خالد',
      action: 'سأل سؤالاً',
      course: 'التعلم الآلي',
      time: 'منذ 30 دقيقة',
      icon: 'fa-question-circle',
      color: 'text-purple-500'
    },
    {
      id: 4,
      user: 'فاطمة عبدالله',
      action: 'حصلت على شهادة',
      course: 'تحليل البيانات',
      time: 'منذ ساعة',
      icon: 'fa-trophy',
      color: 'text-yellow-500'
    }
  ]);

  const [topCourses, setTopCourses] = useState([
    { name: 'تعلم الذكاء الاصطناعي', progress: 85, students: 234 },
    { name: 'أساسيات البرمجة', progress: 92, students: 189 },
    { name: 'التعلم الآلي', progress: 78, students: 156 },
    { name: 'تحليل البيانات', progress: 65, students: 123 }
  ]);

  return (
    <div className="space-y-6">
      {/* Page Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-gray-900 dark:text-white">لوحة التحكم</h1>
          <p className="text-gray-600 dark:text-gray-400">نظرة عامة على أداء المنصة</p>
        </div>
        <div className="flex items-center space-x-3">
          <button className="px-4 py-2 bg-gradient-to-r from-blue-500 to-purple-600 text-white rounded-xl hover:shadow-lg transition-all duration-200 transform hover:scale-105">
            <i className="fas fa-plus mr-2"></i>
            إنشاء جديد
          </button>
        </div>
      </div>

      {/* Stats Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        {/* Total Users Card */}
        <div className="bg-white dark:bg-gray-800 rounded-2xl p-6 shadow-lg border border-gray-100 dark:border-gray-700">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm font-medium text-gray-600 dark:text-gray-400">إجمالي المستخدمين</p>
              <p className="text-2xl font-bold text-gray-900 dark:text-white">{stats.totalUsers}</p>
              <p className="text-sm text-green-500 flex items-center">
                <i className="fas fa-arrow-up mr-1"></i>
                12% زيادة
              </p>
            </div>
            <div className="w-12 h-12 bg-blue-100 dark:bg-blue-900/30 rounded-xl flex items-center justify-center">
              <i className="fas fa-users text-blue-500 text-xl"></i>
            </div>
          </div>
        </div>

        {/* Active Sessions Card */}
        <div className="bg-white dark:bg-gray-800 rounded-2xl p-6 shadow-lg border border-gray-100 dark:border-gray-700">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm font-medium text-gray-600 dark:text-gray-400">جلسات نشطة</p>
              <p className="text-2xl font-bold text-gray-900 dark:text-white">{stats.activeSessions}</p>
              <p className="text-sm text-green-500 flex items-center">
                <i className="fas fa-arrow-up mr-1"></i>
                8% زيادة
              </p>
            </div>
            <div className="w-12 h-12 bg-green-100 dark:bg-green-900/30 rounded-xl flex items-center justify-center">
              <i className="fas fa-comments text-green-500 text-xl"></i>
            </div>
          </div>
        </div>

        {/* Messages Today Card */}
        <div className="bg-white dark:bg-gray-800 rounded-2xl p-6 shadow-lg border border-gray-100 dark:border-gray-700">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm font-medium text-gray-600 dark:text-gray-400">رسائل اليوم</p>
              <p className="text-2xl font-bold text-gray-900 dark:text-white">{stats.messagesToday}</p>
              <p className="text-sm text-green-500 flex items-center">
                <i className="fas fa-arrow-up mr-1"></i>
                15% زيادة
              </p>
            </div>
            <div className="w-12 h-12 bg-purple-100 dark:bg-purple-900/30 rounded-xl flex items-center justify-center">
              <i className="fas fa-envelope text-purple-500 text-xl"></i>
            </div>
          </div>
        </div>

        {/* Learning Progress Card */}
        <div className="bg-white dark:bg-gray-800 rounded-2xl p-6 shadow-lg border border-gray-100 dark:border-gray-700">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm font-medium text-gray-600 dark:text-gray-400">التقدم في التعلم</p>
              <p className="text-2xl font-bold text-gray-900 dark:text-white">{stats.learningProgress}%</p>
              <p className="text-sm text-green-500 flex items-center">
                <i className="fas fa-arrow-up mr-1"></i>
                5% زيادة
              </p>
            </div>
            <div className="w-12 h-12 bg-orange-100 dark:bg-orange-900/30 rounded-xl flex items-center justify-center">
              <i className="fas fa-graduation-cap text-orange-500 text-xl"></i>
            </div>
          </div>
        </div>
      </div>

      {/* Main Content Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Recent Activities */}
        <div className="bg-white dark:bg-gray-800 rounded-2xl p-6 shadow-lg border border-gray-100 dark:border-gray-700">
          <div className="flex items-center justify-between mb-6">
            <h2 className="text-lg font-semibold text-gray-900 dark:text-white">النشاطات الحديثة</h2>
            <button className="text-blue-500 hover:text-blue-600 text-sm">
              عرض الكل
            </button>
          </div>
          
          <div className="space-y-4">
            {recentActivities.map((activity) => (
              <div key={activity.id} className="flex items-center space-x-4 p-3 rounded-xl hover:bg-gray-50 dark:hover:bg-gray-700/50 transition-colors">
                <div className={`w-10 h-10 ${activity.color} bg-opacity-20 rounded-xl flex items-center justify-center`}>
                  <i className={`fas ${activity.icon} ${activity.color}`}></i>
                </div>
                <div className="flex-1">
                  <p className="text-sm font-medium text-gray-900 dark:text-white">
                    {activity.user} <span className="text-gray-600 dark:text-gray-400">{activity.action}</span>
                  </p>
                  <p className="text-xs text-gray-500 dark:text-gray-400">{activity.course}</p>
                </div>
                <span className="text-xs text-gray-400">{activity.time}</span>
              </div>
            ))}
          </div>
        </div>

        {/* Top Courses */}
        <div className="bg-white dark:bg-gray-800 rounded-2xl p-6 shadow-lg border border-gray-100 dark:border-gray-700">
          <div className="flex items-center justify-between mb-6">
            <h2 className="text-lg font-semibold text-gray-900 dark:text-white">أفضل الدورات</h2>
            <button className="text-blue-500 hover:text-blue-600 text-sm">
              عرض الكل
            </button>
          </div>
          
          <div className="space-y-4">
            {topCourses.map((course, index) => (
              <div key={index} className="space-y-2">
                <div className="flex items-center justify-between">
                  <span className="text-sm font-medium text-gray-900 dark:text-white">{course.name}</span>
                  <span className="text-sm text-gray-500">{course.progress}%</span>
                </div>
                <div className="w-full bg-gray-200 dark:bg-gray-700 rounded-full h-2">
                  <div 
                    className="bg-gradient-to-r from-blue-500 to-purple-600 h-2 rounded-full transition-all duration-300"
                    style={{ width: `${course.progress}%` }}
                  ></div>
                </div>
                <div className="flex items-center justify-between text-xs text-gray-500">
                  <span>{course.students} طالب</span>
                  <span>مستمر</span>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* System Status */}
      <div className="bg-white dark:bg-gray-800 rounded-2xl p-6 shadow-lg border border-gray-100 dark:border-gray-700">
        <h2 className="text-lg font-semibold text-gray-900 dark:text-white mb-6">حالة النظام</h2>
        
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          <div className="text-center p-4 bg-green-50 dark:bg-green-900/20 rounded-xl">
            <div className="w-12 h-12 bg-green-500 rounded-full flex items-center justify-center mx-auto mb-3">
              <i className="fas fa-check text-white"></i>
            </div>
            <h3 className="font-semibold text-green-900 dark:text-green-400">API</h3>
            <p className="text-sm text-green-600 dark:text-green-300">يعمل بشكل طبيعي</p>
          </div>
          
          <div className="text-center p-4 bg-green-50 dark:bg-green-900/20 rounded-xl">
            <div className="w-12 h-12 bg-green-500 rounded-full flex items-center justify-center mx-auto mb-3">
              <i className="fas fa-database text-white"></i>
            </div>
            <h3 className="font-semibold text-green-900 dark:text-green-400">قاعدة البيانات</h3>
            <p className="text-sm text-green-600 dark:text-green-300">متصل</p>
          </div>
          
          <div className="text-center p-4 bg-blue-50 dark:bg-blue-900/20 rounded-xl">
            <div className="w-12 h-12 bg-blue-500 rounded-full flex items-center justify-center mx-auto mb-3">
              <i className="fas fa-brain text-white"></i>
            </div>
            <h3 className="font-semibold text-blue-900 dark:text-blue-400">نموذج الذكاء</h3>
            <p className="text-sm text-blue-600 dark:text-blue-300">جاري التعلم</p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default DashboardPage;
