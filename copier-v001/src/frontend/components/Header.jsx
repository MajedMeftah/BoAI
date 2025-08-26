import React, { useState } from 'react';

const Header = ({ currentPage, onPageChange, onThemeToggle, isDarkMode }) => {
  const [isMenuOpen, setIsMenuOpen] = useState(false);

  const navigationItems = [
    { id: 'chat', label: 'المحادثة', icon: 'fa-comments' },
    { id: 'learning', label: 'التعلم', icon: 'fa-graduation-cap' },
    { id: 'resources', label: 'المصادر', icon: 'fa-book' },
    { id: 'profile', label: 'الملف الشخصي', icon: 'fa-user' },
    { id: 'settings', label: 'الإعدادات', icon: 'fa-cog' }
  ];

  return (
    <header className="bg-white dark:bg-gray-800 shadow-lg border-b border-gray-200 dark:border-gray-700">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          {/* Logo and Brand */}
          <div className="flex items-center space-x-3">
            <div className="w-10 h-10 bg-gradient-to-r from-blue-500 to-purple-600 rounded-lg flex items-center justify-center">
              <i className="fas fa-robot text-white"></i>
            </div>
            <div>
              <h1 className="text-xl font-bold text-gray-900 dark:text-white">BoAI</h1>
              <p className="text-sm text-gray-500 dark:text-gray-400">منصة التعلم الذكي</p>
            </div>
          </div>

          {/* Desktop Navigation */}
          <nav className="hidden md:flex items-center space-x-1">
            {navigationItems.map((item) => (
              <button
                key={item.id}
                onClick={() => onPageChange(item.id)}
                className={`px-4 py-2 rounded-lg text-sm font-medium transition-colors flex items-center space-x-2 ${
                  currentPage === item.id
                    ? 'bg-blue-500 text-white'
                    : 'text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700'
                }`}
              >
                <i className={`fas ${item.icon}`}></i>
                <span>{item.label}</span>
              </button>
            ))}
          </nav>

          {/* Right Side Controls */}
          <div className="flex items-center space-x-3">
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
              <button className="w-10 h-10 bg-gradient-to-r from-green-500 to-teal-600 rounded-full flex items-center justify-center text-white">
                <i className="fas fa-user"></i>
              </button>
            </div>

            {/* Mobile Menu Button */}
            <button
              onClick={() => setIsMenuOpen(!isMenuOpen)}
              className="md:hidden p-2 text-gray-600 dark:text-gray-400 hover:text-gray-900 dark:hover:text-white transition-colors rounded-lg hover:bg-gray-100 dark:hover:bg-gray-700"
            >
              <i className={`fas ${isMenuOpen ? 'fa-times' : 'fa-bars'}`}></i>
            </button>
          </div>
        </div>

        {/* Mobile Navigation */}
        {isMenuOpen && (
          <div className="md:hidden border-t border-gray-200 dark:border-gray-700 mt-2 pt-2">
            <nav className="flex flex-col space-y-1">
              {navigationItems.map((item) => (
                <button
                  key={item.id}
                  onClick={() => {
                    onPageChange(item.id);
                    setIsMenuOpen(false);
                  }}
                  className={`px-4 py-3 rounded-lg text-sm font-medium transition-colors flex items-center space-x-3 ${
                    currentPage === item.id
                      ? 'bg-blue-500 text-white'
                      : 'text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700'
                  }`}
                >
                  <i className={`fas ${item.icon}`}></i>
                  <span>{item.label}</span>
                </button>
              ))}
            </nav>
          </div>
        )}
      </div>
    </header>
  );
};

export default Header;
