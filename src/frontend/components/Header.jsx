import React, { useState } from 'react';

const Header = ({ currentPage, onPageChange, onThemeToggle, onSidebarToggle, isDarkMode, isSidebarOpen }) => {
  const [isUserMenuOpen, setIsUserMenuOpen] = useState(false);

  return (
    <header className="bg-white/80 dark:bg-gray-800/80 backdrop-blur-sm border-b border-gray-200/50 dark:border-gray-700/50">
      <div className="px-6 py-4">
        <div className="flex items-center justify-between">
          {/* Left side - Sidebar toggle and breadcrumb */}
          <div className="flex items-center space-x-4">
            {/* Sidebar Toggle */}
            <button
              onClick={onSidebarToggle}
              className="p-2 text-gray-600 dark:text-gray-400 hover:text-gray-900 dark:hover:text-white transition-colors rounded-lg hover:bg-gray-100 dark:hover:bg-gray-700"
              title={isSidebarOpen ? 'إغلاق الشريط الجانبي' : 'فتح الشريط الجانبي'}
            >
              <i className={`fas ${isSidebarOpen ? 'fa-bars' : 'fa-bars'} text-lg`}></i>
            </button>

            {/* Breadcrumb */}
            <div className="hidden md:flex items-center space-x-2 text-sm text-gray-600 dark:text-gray-400">
              <span>BoAI</span>
              <i className="fas fa-chevron-left text-xs"></i>
              <span className="font-medium text-gray-900 dark:text-white capitalize">
                {currentPage === 'dashboard' ? 'لوحة التحكم' : 
                 currentPage === 'chat' ? 'المحادثة' :
                 currentPage === 'learning' ? 'التعلم' :
                 currentPage === 'resources' ? 'المصادر' :
                 currentPage === 'profile' ? 'الملف الشخصي' : 'الإعدادات'}
              </span>
            </div>
          </div>

          {/* Center - Search Bar */}
          <div className="flex-1 max-w-md mx-8">
            <div className="relative">
              <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                <i className="fas fa-search text-gray-400"></i>
              </div>
              <input
                type="text"
                placeholder="ابحث في المنصة..."
                className="w-full pl-10 pr-4 py-2 border border-gray-300 dark:border-gray-600 rounded-xl bg-white/50 dark:bg-gray-700/50 text-gray-900 dark:text-white placeholder-gray-500 dark:placeholder-gray-400 focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all duration-200"
              />
            </div>
          </div>

          {/* Right side - Controls */}
          <div className="flex items-center space-x-3">
            {/* Notifications */}
            <button className="relative p-2 text-gray-600 dark:text-gray-400 hover:text-gray-900 dark:hover:text-white transition-colors rounded-lg hover:bg-gray-100 dark:hover:bg-gray-700">
              <i className="fas fa-bell"></i>
              <span className="absolute -top-1 -right-1 w-4 h-4 bg-red-500 text-white text-xs rounded-full flex items-center justify-center">
                3
              </span>
            </button>

            {/* Theme Toggle */}
            <button
              onClick={onThemeToggle}
              className="p-2 text-gray-600 dark:text-gray-400 hover:text-gray-900 dark:hover:text-white transition-colors rounded-lg hover:bg-gray-100 dark:hover:bg-gray-700"
              title={isDarkMode ? 'تفعيل الوضع الفاتح' : 'تفعيل الوضع الداكن'}
            >
              <i className={`fas ${isDarkMode ? 'fa-sun' : 'fa-moon'}`}></i>
            </button>

            {/* User Menu */}
            <div className="relative">
              <button
                onClick={() => setIsUserMenuOpen(!isUserMenuOpen)}
                className="flex items-center space-x-3 p-2 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-700 transition-colors"
              >
                <div className="w-10 h-10 bg-gradient-to-r from-blue-500 to-purple-600 rounded-full flex items-center justify-center text-white">
                  <i className="fas fa-user"></i>
                </div>
                <div className="hidden md:block text-left">
                  <p className="text-sm font-medium text-gray-900 dark:text-white">المستخدم</p>
                  <p className="text-xs text-gray-500 dark:text-gray-400">مشرف النظام</p>
                </div>
                <i className={`fas fa-chevron-down text-gray-400 transition-transform ${isUserMenuOpen ? 'rotate-180' : ''}`}></i>
              </button>

              {/* User Dropdown Menu */}
              {isUserMenuOpen && (
                <div className="absolute right-0 mt-2 w-48 bg-white dark:bg-gray-800 rounded-xl shadow-lg border border-gray-200 dark:border-gray-700 py-2 z-50">
                  <button
                    onClick={() => onPageChange('profile')}
                    className="w-full px-4 py-2 text-left text-sm text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700 transition-colors"
                  >
                    <i className="fas fa-user mr-2"></i>
                    الملف الشخصي
                  </button>
                  <button
                    onClick={() => onPageChange('settings')}
                    className="w-full px-4 py-2 text-left text-sm text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700 transition-colors"
                  >
                    <i className="fas fa-cog mr-2"></i>
                    الإعدادات
                  </button>
                  <div className="border-t border-gray-200 dark:border-gray-700 my-1"></div>
                  <button className="w-full px-4 py-2 text-left text-sm text-red-600 hover:bg-red-50 dark:hover:bg-red-900/20 transition-colors">
                    <i className="fas fa-sign-out-alt mr-2"></i>
                    تسجيل الخروج
                  </button>
                </div>
              )}
            </div>
          </div>
        </div>
      </div>
    </header>
  );
};

export default Header;
