import React, { useState, useEffect } from 'react';
import Header from './components/Header';
import Sidebar from './components/Sidebar';
import Footer from './components/Footer';
import ChatPage from './pages/ChatPage';
import LearningPage from './pages/LearningPage';
import ResourcesPage from './pages/ResourcesPage';
import ProfilePage from './pages/ProfilePage';
import SettingsPage from './pages/SettingsPage';
import DashboardPage from './pages/DashboardPage';

const App = () => {
  const [currentPage, setCurrentPage] = useState('dashboard');
  const [isDarkMode, setIsDarkMode] = useState(false);
  const [isSidebarOpen, setIsSidebarOpen] = useState(true);
  
  // Handle theme toggle
  const handleThemeToggle = () => {
    const newDarkMode = !isDarkMode;
    setIsDarkMode(newDarkMode);
    
    // Update HTML class for dark mode
    if (newDarkMode) {
      document.documentElement.classList.add('dark');
    } else {
      document.documentElement.classList.remove('dark');
    }
    
    // Save preference to localStorage
    localStorage.setItem('darkMode', newDarkMode.toString());
  };

  // Handle sidebar toggle
  const handleSidebarToggle = () => {
    setIsSidebarOpen(!isSidebarOpen);
  };

  // Load theme preference on component mount
  useEffect(() => {
    const savedDarkMode = localStorage.getItem('darkMode');
    if (savedDarkMode === 'true') {
      setIsDarkMode(true);
      document.documentElement.classList.add('dark');
    } else {
      setIsDarkMode(false);
      document.documentElement.classList.remove('dark');
    }
  }, []);

  // Render current page
  const renderCurrentPage = () => {
    switch (currentPage) {
      case 'dashboard':
        return <DashboardPage />;
      case 'chat':
        return <ChatPage />;
      case 'learning':
        return <LearningPage />;
      case 'resources':
        return <ResourcesPage />;
      case 'profile':
        return <ProfilePage />;
      case 'settings':
        return <SettingsPage />;
      default:
        return <DashboardPage />;
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-50 via-white to-gray-100 dark:from-gray-900 dark:via-gray-800 dark:to-gray-900 flex">
      {/* Sidebar */}
      <Sidebar 
        currentPage={currentPage}
        onPageChange={setCurrentPage}
        isOpen={isSidebarOpen}
        onToggle={handleSidebarToggle}
      />
      
      {/* Main Content */}
      <div className={`flex-1 flex flex-col transition-all duration-300 ${isSidebarOpen ? 'lg:ml-64' : 'ml-0'}`}>
        <Header 
          currentPage={currentPage}
          onPageChange={setCurrentPage}
          onThemeToggle={handleThemeToggle}
          onSidebarToggle={handleSidebarToggle}
          isDarkMode={isDarkMode}
          isSidebarOpen={isSidebarOpen}
        />
        
        <main className="flex-1 p-6">
          {renderCurrentPage()}
        </main>
        
        <Footer />
      </div>
    </div>
  );
};

export default App;
