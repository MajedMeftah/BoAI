import React from 'react';

const Sidebar = ({ currentPage, onPageChange, isOpen, onToggle }) => {
  const navigationItems = [
    { id: 'dashboard', label: 'لوحة التحكم', icon: 'fa-chart-line', color: 'text-blue-500' },
    { id: 'chat', label: 'المحادثة', icon: 'fa-comments', color: 'text-green-500' },
    { id: 'learning', label: 'التعلم', icon: 'fa-graduation-cap', color: 'text-purple-500' },
    { id: 'resources', label: 'المصادر', icon: 'fa-book', color: 'text-orange-500' },
    { id: 'profile', label: 'الملف الشخصي', icon: 'fa-user', color: 'text-pink-500' },
    { id: 'settings', label: 'الإعدادات', icon: 'fa-cog', color: 'text-gray-500' }
  ];

  return (
    <>
      {/* Sidebar Overlay for mobile */}
      {isOpen && (
        <div 
          className="fixed inset-0 bg-black bg-opacity-50 z-40 lg:hidden"
          onClick={onToggle}
        />
      )}
      
      {/* Sidebar */}
      <aside className={`
        fixed top-0 left-0 z-50 h-screen bg-white dark:bg-gray-800 shadow-xl
        transform transition-transform duration-300 ease-in-out
        ${isOpen ? 'translate-x-0' : '-translate-x-full'}
        lg:translate-x-0 lg:static lg:inset-0
        w-64 border-r border-gray-200 dark:border-gray-700
      `}>
        {/* Sidebar Header */}
        <div className="p-6 border-b border-gray-200 dark:border-gray-700">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-3">
              <div className="w-12 h-12 bg-gradient-to-r from-blue-500 to-purple-600 rounded-xl flex items-center justify-center shadow-lg">
                <i className="fas fa-robot text-white text-xl"></i>
              </div>
              <div>
                <h1 className="text-xl font-bold text-gray-900 dark:text-white">BoAI</h1>
                <p className="text-sm text-gray-500 dark:text-gray-400">الذكاء الاصطناعي</p>
              </div>
            </div>
            
            {/* Close button for mobile */}
            <button
              onClick={onToggle}
              className="lg:hidden p-2 text-gray-500 hover:text-gray-700 dark:text-gray-400 dark:hover:text-white"
            >
              <i className="fas fa-times"></i>
            </button>
          </div>
        </div>

        {/* Navigation */}
        <nav className="p-4 space-y-2">
          {navigationItems.map((item) => (
            <button
              key={item.id}
              onClick={() => {
                onPageChange(item.id);
                if (window.innerWidth < 1024) {
                  onToggle(); // Close sidebar on mobile after selection
                }
              }}
              className={`
                w-full flex items-center space-x-3 px-4 py-3 rounded-xl
                transition-all duration-200 transform hover:scale-105
                ${currentPage === item.id
                  ? 'bg-gradient-to-r from-blue-500 to-purple-600 text-white shadow-lg'
                  : 'text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700'
                }
              `}
            >
              <i className={`fas ${item.icon} ${item.color} ${currentPage === item.id ? 'text-white' : ''}`}></i>
              <span className="font-medium">{item.label}</span>
              {currentPage === item.id && (
                <div className="ml-auto w-2 h-2 bg-white rounded-full"></div>
              )}
            </button>
          ))}
        </nav>

        {/* Sidebar Footer */}
        <div className="absolute bottom-0 left-0 right-0 p-4 border-t border-gray-200 dark:border-gray-700">
          <div className="bg-gradient-to-r from-blue-50 to-purple-50 dark:from-blue-900/20 dark:to-purple-900/20 rounded-xl p-4">
            <div className="text-center">
              <div className="w-10 h-10 bg-gradient-to-r from-blue-500 to-purple-600 rounded-full flex items-center justify-center mx-auto mb-2">
                <i className="fas fa-star text-white"></i>
              </div>
              <h3 className="text-sm font-semibold text-gray-900 dark:text-white mb-1">
                التحديث الجديد!
              </h3>
              <p className="text-xs text-gray-600 dark:text-gray-400">
                نظام التعلم الذاتي المتقدم
              </p>
            </div>
          </div>
        </div>
      </aside>
    </>
  );
};

export default Sidebar;
