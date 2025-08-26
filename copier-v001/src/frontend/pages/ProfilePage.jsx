import React, { useState } from 'react';

const ProfilePage = () => {
  const [activeTab, setActiveTab] = useState('overview');
  const [isEditing, setIsEditing] = useState(false);

  const userData = {
    name: 'أحمد محمد',
    email: 'ahmed@example.com',
    username: 'ahmed_dev',
    joinDate: '2024-01-15',
    level: 'متوسط',
    points: 1250,
    avatar: 'https://images.unsplash.com/photo-1472099645785-5658abf4ff4e?w=150&h=150&fit=crop&crop=face'
  };

  const stats = {
    coursesCompleted: 8,
    hoursLearned: 42,
    certificates: 3,
    streak: 12
  };

  const recentActivities = [
    {
      type: 'course',
      title: 'أكملت دورة Python الأساسية',
      time: 'منذ ساعتين',
      icon: 'fa-graduation-cap',
      color: 'green'
    },
    {
      type: 'quiz',
      title: 'حللت اختبار الخوارزميات',
      score: '85%',
      time: 'منذ يوم',
      icon: 'fa-trophy',
      color: 'blue'
    },
    {
      type: 'resource',
      title: 'حملت ملخص CSS',
      time: 'منذ يومين',
      icon: 'fa-download',
      color: 'purple'
    },
    {
      type: 'chat',
      title: 'تواصلت مع المساعد حول React',
      time: 'منذ 3 أيام',
      icon: 'fa-comments',
      color: 'orange'
    }
  ];

  const skills = [
    { name: 'Python', level: 85, color: 'blue' },
    { name: 'JavaScript', level: 70, color: 'yellow' },
    { name: 'HTML/CSS', level: 90, color: 'red' },
    { name: 'React', level: 65, color: 'cyan' },
    { name: 'SQL', level: 60, color: 'green' }
  ];

  const ProgressBar = ({ progress, color }) => (
    <div className="w-full bg-gray-200 dark:bg-gray-700 rounded-full h-2">
      <div
        className={`bg-${color}-500 h-2 rounded-full transition-all duration-300`}
        style={{ width: `${progress}%` }}
      ></div>
    </div>
  );

  return (
    <div className="min-h-screen bg-gray-50 dark:bg-gray-900">
      <div className="max-w-6xl mx-auto p-6">
        {/* Header */}
        <div className="text-center mb-8">
          <h1 className="text-3xl font-bold text-gray-900 dark:text-white mb-4">
            الملف الشخصي
          </h1>
          <p className="text-gray-600 dark:text-gray-400 text-lg">
            إدارة معلوماتك ومتابعة تقدمك التعليمي
          </p>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Profile Sidebar */}
          <div className="lg:col-span-1">
            <div className="bg-white dark:bg-gray-800 rounded-2xl shadow-xl p-6">
              {/* Avatar */}
              <div className="text-center mb-6">
                <div className="w-24 h-24 mx-auto mb-4 relative">
                  <img
                    src={userData.avatar}
                    alt="Profile"
                    className="w-full h-full rounded-full object-cover border-4 border-white dark:border-gray-800 shadow-lg"
                  />
                  <button className="absolute bottom-0 right-0 w-8 h-8 bg-blue-500 text-white rounded-full flex items-center justify-center hover:bg-blue-600 transition-colors">
                    <i className="fas fa-camera text-sm"></i>
                  </button>
                </div>
                
                {isEditing ? (
                  <div className="space-y-3">
                    <input
                      type="text"
                      defaultValue={userData.name}
                      className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg dark:bg-gray-700 dark:text-white"
                      placeholder="الاسم الكامل"
                    />
                    <input
                      type="text"
                      defaultValue={userData.username}
                      className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg dark:bg-gray-700 dark:text-white"
                      placeholder="اسم المستخدم"
                    />
                  </div>
                ) : (
                  <>
                    <h2 className="text-xl font-bold text-gray-900 dark:text-white mb-1">
                      {userData.name}
                    </h2>
                    <p className="text-gray-600 dark:text-gray-400">@{userData.username}</p>
                  </>
                )}
              </div>

              {/* Stats */}
              <div className="grid grid-cols-2 gap-4 mb-6">
                <div className="text-center p-3 bg-blue-50 dark:bg-blue-900/20 rounded-lg">
                  <div className="w-10 h-10 bg-blue-500 rounded-full flex items-center justify-center mx-auto mb-2">
                    <i className="fas fa-graduation-cap text-white"></i>
                  </div>
                  <h3 className="font-bold text-gray-900 dark:text-white">{stats.coursesCompleted}</h3>
                  <p className="text-sm text-gray-600 dark:text-gray-400">دورة مكتملة</p>
                </div>

                <div className="text-center p-3 bg-green-50 dark:bg-green-900/20 rounded-lg">
                  <div className="w-10 h-10 bg-green-500 rounded-full flex items-center justify-center mx-auto mb-2">
                    <i className="fas fa-clock text-white"></i>
                  </div>
                  <h3 className="font-bold text-gray-900 dark:text-white">{stats.hoursLearned}</h3>
                  <p className="text-sm text-gray-600 dark:text-gray-400">ساعة تعلم</p>
                </div>

                <div className="text-center p-3 bg-purple-50 dark:bg-purple-900/20 rounded-lg">
                  <div className="w-10 h-10 bg-purple-500 rounded-full flex items-center justify-center mx-auto mb-2">
                    <i className="fas fa-certificate text-white"></i>
                  </div>
                  <h3 className="font-bold text-gray-900 dark:text-white">{stats.certificates}</h3>
                  <p className="text-sm text-gray-600 dark:text-gray-400">شهادة</p>
                </div>

                <div className="text-center p-3 bg-orange-50 dark:bg-orange-900/20 rounded-lg">
                  <div className="w-10 h-10 bg-orange-500 rounded-full flex items-center justify-center mx-auto mb-2">
                    <i className="fas fa-fire text-white"></i>
                  </div>
                  <h3 className="font-bold text-gray-900 dark:text-white">{stats.streak}</h3>
                  <p className="text-sm text-gray-600 dark:text-gray-400">يوم متتالي</p>
                </div>
              </div>

              {/* Actions */}
              <div className="space-y-2">
                <button
                  onClick={() => setIsEditing(!isEditing)}
                  className="w-full px-4 py-2 bg-blue-500 hover:bg-blue-600 text-white rounded-lg transition-colors"
                >
                  {isEditing ? 'حفظ التغييرات' : 'تعديل الملف'}
                </button>
                <button className="w-full px-4 py-2 border border-gray-300 dark:border-gray-600 text-gray-700 dark:text-gray-300 rounded-lg hover:bg-gray-50 dark:hover:bg-gray-700 transition-colors">
                  تغيير كلمة المرور
                </button>
              </div>
            </div>

            {/* Level Progress */}
            <div className="bg-white dark:bg-gray-800 rounded-2xl shadow-xl p-6 mt-6">
              <h3 className="font-semibold text-gray-900 dark:text-white mb-4">تقدم المستوى</h3>
              <div className="space-y-2">
                <div className="flex justify-between items-center text-sm">
                  <span className="text-gray-600 dark:text-gray-400">المستوى الحالي</span>
                  <span className="font-semibold text-blue-500">{userData.level}</span>
                </div>
                <ProgressBar progress={65} color="blue" />
                <div className="flex justify-between items-center text-sm">
                  <span className="text-gray-600 dark:text-gray-400">النقاط</span>
                  <span className="font-semibold">{userData.points} نقطة</span>
                </div>
              </div>
            </div>
          </div>

          {/* Main Content */}
          <div className="lg:col-span-2">
            {/* Tabs */}
            <div className="bg-white dark:bg-gray-800 rounded-2xl shadow-xl mb-6">
              <div className="flex border-b border-gray-200 dark:border-gray-700">
                {['overview', 'skills', 'achievements', 'settings'].map((tab) => (
                  <button
                    key={tab}
                    onClick={() => setActiveTab(tab)}
                    className={`px-6 py-3 text-sm font-medium transition-colors ${
                      activeTab === tab
                        ? 'text-blue-500 border-b-2 border-blue-500'
                        : 'text-gray-600 dark:text-gray-400 hover:text-gray-900 dark:hover:text-white'
                    }`}
                  >
                    {tab === 'overview' && 'نظرة عامة'}
                    {tab === 'skills' && 'المهارات'}
                    {tab === 'achievements' && 'الإنجازات'}
                    {tab === 'settings' && 'الإعدادات'}
                  </button>
                ))}
              </div>

              {/* Tab Content */}
              <div className="p-6">
                {activeTab === 'overview' && (
                  <div>
                    <h3 className="font-semibold text-gray-900 dark:text-white mb-4">النشاط الأخير</h3>
                    <div className="space-y-3">
                      {recentActivities.map((activity, index) => (
                        <div key={index} className="flex items-center space-x-3 p-3 bg-gray-50 dark:bg-gray-700 rounded-lg">
                          <div className={`w-10 h-10 bg-${activity.color}-500 rounded-full flex items-center justify-center flex-shrink-0`}>
                            <i className={`fas ${activity.icon} text-white`}></i>
                          </div>
                          <div className="flex-1">
                            <p className="text-sm text-gray-900 dark:text-white">{activity.title}</p>
                            <p className="text-xs text-gray-600 dark:text-gray-400">{activity.time}</p>
                          </div>
                          {activity.score && (
                            <span className="px-2 py-1 bg-green-100 text-green-800 text-xs rounded-full">
                              {activity.score}
                            </span>
                          )}
                        </div>
                      ))}
                    </div>
                  </div>
                )}

                {activeTab === 'skills' && (
                  <div>
                    <h3 className="font-semibold text-gray-900 dark:text-white mb-4">مهاراتك</h3>
                    <div className="space-y-4">
                      {skills.map((skill, index) => (
                        <div key={index}>
                          <div className="flex justify-between items-center mb-2">
                            <span className="text-sm font-medium text-gray-900 dark:text-white">{skill.name}</span>
                            <span className="text-sm text-gray-600 dark:text-gray-400">{skill.level}%</span>
                          </div>
                          <ProgressBar progress={skill.level} color={skill.color} />
                        </div>
                      ))}
                    </div>
                  </div>
                )}

                {activeTab === 'achievements' && (
                  <div>
                    <h3 className="font-semibold text-gray-900 dark:text-white mb-4">الإنجازات</h3>
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                      <div className="text-center p-4 bg-yellow-50 dark:bg-yellow-900/20 rounded-lg">
                        <i className="fas fa-trophy text-3xl text-yellow-500 mb-2"></i>
                        <h4 className="font-semibold text-gray-900 dark:text-white">المتعلم النشط</h4>
                        <p className="text-sm text-gray-600 dark:text-gray-400">أكمل 5 دورات</p>
                      </div>
                    <div className="text-center p-4 bg-blue-50 dark:bg-blue-900/20 rounded-lg">
                        <i className="fas fa-star text-3xl text-blue-500 mb-2"></i>
                        <h4 className="font-semibold text-gray-900 dark:text-white">الطالب المتميز</h4>
                        <p className="text-sm text-gray-600 dark:text-gray-400">حقق معدل 90% في الاختبارات</p>
                      </div>
                    </div>
                  </div>
                )}

                {activeTab === 'settings' && (
                  <div>
                    <h3 className="font-semibold text-gray-900 dark:text-white mb-4">الإعدادات</h3>
                    <div className="space-y-4">
                      <div>
                        <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                          البريد الإلكتروني
                        </label>
                        <input
                          type="email"
                          defaultValue={userData.email}
                          className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg dark:bg-gray-700 dark:text-white"
                        />
                      </div>
                      <div>
                        <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                          تفضيلات الإشعارات
                        </label>
                        <div className="space-y-2">
                          <label className="flex items-center">
                            <input type="checkbox" className="rounded border-gray-300 text-blue-500" defaultChecked />
                            <span className="ml-2 text-sm text-gray-700 dark:text-gray-300">الإشعارات البريدية</span>
                          </label>
                          <label className="flex items-center">
                            <input type="checkbox" className="rounded border-gray-300 text-blue-500" defaultChecked />
                            <span className="ml-2 text-sm text-gray-700 dark:text-gray-300">تنبيهات الدروس الجديدة</span>
                          </label>
                        </div>
                      </div>
                    </div>
                  </div>
                )}
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ProfilePage;
