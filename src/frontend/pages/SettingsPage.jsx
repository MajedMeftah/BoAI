import React, { useState } from 'react';

const SettingsPage = () => {
  const [activeTab, setActiveTab] = useState('general');
  const [settings, setSettings] = useState({
    // General Settings
    language: 'ar',
    theme: 'system',
    fontSize: 'medium',
    
    // Notification Settings
    emailNotifications: true,
    pushNotifications: true,
    courseUpdates: true,
    achievementAlerts: true,
    
    // Privacy Settings
    profileVisibility: 'public',
    showOnlineStatus: true,
    allowMessages: true,
    
    // Account Settings
    twoFactorAuth: false,
    dataExport: false,
    deleteAccount: false
  });

  const handleSettingChange = (key, value) => {
    setSettings(prev => ({
      ...prev,
      [key]: value
    }));
  };

  const tabs = [
    { id: 'general', label: 'عام', icon: 'fa-cog' },
    { id: 'notifications', label: 'الإشعارات', icon: 'fa-bell' },
    { id: 'privacy', label: 'الخصوصية', icon: 'fa-shield' },
    { id: 'account', label: 'الحساب', icon: 'fa-user' }
  ];

  const languages = [
    { value: 'ar', label: 'العربية' },
    { value: 'en', label: 'English' },
    { value: 'fr', label: 'Français' }
  ];

  const themes = [
    { value: 'light', label: 'فاتح' },
    { value: 'dark', label: 'داكن' },
    { value: 'system', label: 'تلقائي (نظام)' }
  ];

  const fontSizes = [
    { value: 'small', label: 'صغير' },
    { value: 'medium', label: 'متوسط' },
    { value: 'large', label: 'كبير' },
    { value: 'xlarge', label: 'كبير جداً' }
  ];

  const privacyOptions = [
    { value: 'public', label: 'عام', description: 'الجميع يمكنه رؤية ملفك الشخصي' },
    { value: 'friends', label: 'الأصدقاء فقط', description: 'الأصدقاء فقط يمكنهم رؤية ملفك' },
    { value: 'private', label: 'خاص', description: 'أنت فقط يمكنك رؤية ملفك' }
  ];

  return (
    <div className="min-h-screen bg-gray-50 dark:bg-gray-900">
      <div className="max-w-6xl mx-auto p-6">
        {/* Header */}
        <div className="text-center mb-8">
          <h1 className="text-3xl font-bold text-gray-900 dark:text-white mb-4">
            الإعدادات
          </h1>
          <p className="text-gray-600 dark:text-gray-400 text-lg">
            خصص تجربتك التعليمية وفقاً لتفضيلاتك
          </p>
        </div>

        <div className="bg-white dark:bg-gray-800 rounded-2xl shadow-xl">
          {/* Tabs */}
          <div className="flex border-b border-gray-200 dark:border-gray-700">
            {tabs.map((tab) => (
              <button
                key={tab.id}
                onClick={() => setActiveTab(tab.id)}
                className={`px-6 py-4 text-sm font-medium transition-colors flex items-center space-x-2 ${
                  activeTab === tab.id
                    ? 'text-blue-500 border-b-2 border-blue-500'
                    : 'text-gray-600 dark:text-gray-400 hover:text-gray-900 dark:hover:text-white'
                }`}
              >
                <i className={`fas ${tab.icon}`}></i>
                <span>{tab.label}</span>
              </button>
            ))}
          </div>

          {/* Tab Content */}
          <div className="p-6">
            {/* General Settings */}
            {activeTab === 'general' && (
              <div className="space-y-6">
                <div>
                  <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-4">الإعدادات العامة</h3>
                  
                  <div className="space-y-4">
                    {/* Language */}
                    <div>
                      <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                        اللغة
                      </label>
                      <select
                        value={settings.language}
                        onChange={(e) => handleSettingChange('language', e.target.value)}
                        className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg dark:bg-gray-700 dark:text-white"
                      >
                        {languages.map((lang) => (
                          <option key={lang.value} value={lang.value}>
                            {lang.label}
                          </option>
                        ))}
                      </select>
                    </div>

                    {/* Theme */}
                    <div>
                      <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                        المظهر
                      </label>
                      <select
                        value={settings.theme}
                        onChange={(e) => handleSettingChange('theme', e.target.value)}
                        className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg dark:bg-gray-700 dark:text-white"
                      >
                        {themes.map((theme) => (
                          <option key={theme.value} value={theme.value}>
                            {theme.label}
                          </option>
                        ))}
                      </select>
                    </div>

                    {/* Font Size */}
                    <div>
                      <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                        حجم الخط
                      </label>
                      <select
                        value={settings.fontSize}
                        onChange={(e) => handleSettingChange('fontSize', e.target.value)}
                        className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg dark:bg-gray-700 dark:text-white"
                      >
                        {fontSizes.map((size) => (
                          <option key={size.value} value={size.value}>
                            {size.label}
                          </option>
                        ))}
                      </select>
                    </div>
                  </div>
                </div>

                <div className="border-t border-gray-200 dark:border-gray-700 pt-6">
                  <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-4">إعدادات الوصول</h3>
                  
                  <div className="space-y-3">
                    <label className="flex items-center">
                      <input
                        type="checkbox"
                        checked={settings.twoFactorAuth}
                        onChange={(e) => handleSettingChange('twoFactorAuth', e.target.checked)}
                        className="rounded border-gray-300 text-blue-500"
                      />
                      <span className="ml-2 text-sm text-gray-700 dark:text-gray-300">
                        المصادقة الثنائية (2FA)
                      </span>
                    </label>
                    
                    <label className="flex items-center">
                      <input
                        type="checkbox"
                        checked={settings.dataExport}
                        onChange={(e) => handleSettingChange('dataExport', e.target.checked)}
                        className="rounded border-gray-300 text-blue-500"
                      />
                      <span className="ml-2 text-sm text-gray-700 dark:text-gray-300">
                        تصدير بيانات التعلم تلقائياً
                      </span>
                    </label>
                  </div>
                </div>
              </div>
            )}

            {/* Notification Settings */}
            {activeTab === 'notifications' && (
              <div className="space-y-6">
                <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-4">إعدادات الإشعارات</h3>
                
                <div className="space-y-4">
                  <div className="bg-gray-50 dark:bg-gray-700 rounded-lg p-4">
                    <h4 className="font-medium text-gray-900 dark:text-white mb-3">البريد الإلكتروني</h4>
                    <div className="space-y-3">
                      <label className="flex items-center">
                        <input
                          type="checkbox"
                          checked={settings.emailNotifications}
                          onChange={(e) => handleSettingChange('emailNotifications', e.target.checked)}
                          className="rounded border-gray-300 text-blue-500"
                        />
                        <span className="ml-2 text-sm text-gray-700 dark:text-gray-300">
                          الإشعارات البريدية
                        </span>
                      </label>
                      
                      <label className="flex items-center">
                        <input
                          type="checkbox"
                          checked={settings.courseUpdates}
                          onChange={(e) => handleSettingChange('courseUpdates', e.target.checked)}
                          className="rounded border-gray-300 text-blue-500"
                        />
                        <span className="ml-2 text-sm text-gray-700 dark:text-gray-300">
                          تحديثات الدروس الجديدة
                        </span>
                      </label>
                    </div>
                  </div>

                  <div className="bg-gray-50 dark:bg-gray-700 rounded-lg p-4">
                    <h4 className="font-medium text-gray-900 dark:text-white mb-3">التنبيهات</h4>
                    <div className="space-y-3">
                      <label className="flex items-center">
                        <input
                          type="checkbox"
                          checked={settings.pushNotifications}
                          onChange={(e) => handleSettingChange('pushNotifications', e.target.checked)}
                          className="rounded border-gray-300 text-blue-500"
                        />
                        <span className="ml-2 text-sm text-gray-700 dark:text-gray-300">
                          التنبيهات الفورية
                        </span>
                      </label>
                      
                      <label className="flex items-center">
                        <input
                          type="checkbox"
                          checked={settings.achievementAlerts}
                          onChange={(e) => handleSettingChange('achievementAlerts', e.target.checked)}
                          className="rounded border-gray-300 text-blue-500"
                        />
                        <span className="ml-2 text-sm text-gray-700 dark:text-gray-300">
                          تنبيهات الإنجازات
                        </span>
                      </label>
                    </div>
                  </div>
                </div>
              </div>
            )}

            {/* Privacy Settings */}
            {activeTab === 'privacy' && (
              <div className="space-y-6">
                <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-4">إعدادات الخصوصية</h3>
                
                <div className="space-y-4">
                  {/* Profile Visibility */}
                  <div>
                    <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                      رؤية الملف الشخصي
                    </label>
                    <select
                      value={settings.profileVisibility}
                      onChange={(e) => handleSettingChange('profileVisibility', e.target.value)}
                      className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg dark:bg-gray-700 dark:text-white"
                    >
                      {privacyOptions.map((option) => (
                        <option key={option.value} value={option.value}>
                          {option.label} - {option.description}
                        </option>
                      ))}
                    </select>
                  </div>

                  {/* Privacy Options */}
                  <div className="space-y-3">
                    <label className="flex items-center">
                      <input
                        type="checkbox"
                        checked={settings.showOnlineStatus}
                        onChange={(e) => handleSettingChange('showOnlineStatus', e.target.checked)}
                        className="rounded border-gray-300 text-blue-500"
                      />
                      <span className="ml-2 text-sm text-gray-700 dark:text-gray-300">
                        إظهار حالة الاتصال
                      </span>
                    </label>
                    
                    <label className="flex items-center">
                      <input
                        type="checkbox"
                        checked={settings.allowMessages}
                        onChange={(e) => handleSettingChange('allowMessages', e.target.checked)}
                        className="rounded border-gray-300 text-blue-500"
                      />
                      <span className="ml-2 text-sm text-gray-700 dark:text-gray-300">
                        السماح بالرسائل الخاصة
                      </span>
                    </label>
                  </div>
                </div>
              </div>
            )}

            {/* Account Settings */}
            {activeTab === 'account' && (
              <div className="space-y-6">
                <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-4">إعدادات الحساب</h3>
                
                <div className="space-y-4">
                  {/* Data Management */}
                  <div className="bg-gray-50 dark:bg-gray-700 rounded-lg p-4">
                    <h4 className="font-medium text-gray-900 dark:text-white mb-3">إدارة البيانات</h4>
                    <div className="space-y-3">
                      <button className="w-full px-4 py-2 bg-blue-500 hover:bg-blue-600 text-white rounded-lg text-sm transition-colors">
                        <i className="fas fa-download mr-2"></i>
                        تصدير جميع البيانات
                      </button>
                      
                      <button className="w-full px-4 py-2 border border-red-500 text-red-500 hover:bg-red-50 dark:hover:bg-red-900/20 rounded-lg text-sm transition-colors">
                        <i className="fas fa-trash mr-2"></i>
                        حذف الحساب
                      </button>
                    </div>
                  </div>

                  {/* Security */}
                  <div className="bg-gray-50 dark:bg-gray-700 rounded-lg p-4">
                    <h4 className="font-medium text-gray-900 dark:text-white mb-3">الأمان</h4>
                    <div className="space-y-3">
                      <button className="w-full px-4 py-2 bg-green-500 hover:bg-green-600 text-white rounded-lg text-sm transition-colors">
                        <i className="fas fa-key mr-2"></i>
                        تغيير كلمة المرور
                      </button>
                      
                      <label className="flex items-center">
                        <input
                          type="checkbox"
                          checked={settings.twoFactorAuth}
                          onChange={(e) => handleSettingChange('twoFactorAuth', e.target.checked)}
                          className="rounded border-gray-300 text-blue-500"
                        />
                        <span className="ml-2 text-sm text-gray-700 dark:text-gray-300">
                          تفعيل المصادقة الثنائية
                        </span>
                      </label>
                    </div>
                  </div>
                </div>
              </div>
            )}
          </div>
        </div>

        {/* Save Button */}
        <div className="mt-6 text-center">
          <button className="px-8 py-3 bg-blue-500 hover:bg-blue-600 text-white rounded-lg font-medium transition-colors">
            حفظ التغييرات
          </button>
        </div>
      </div>
    </div>
  );
};

export default SettingsPage;
