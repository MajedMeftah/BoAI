import React, { useState, useEffect } from 'react';
import Header from './components/Header';
import Footer from './components/Footer';
import ChatPage from './pages/ChatPage';
import LearningPage from './pages/LearningPage';
import ResourcesPage from './pages/ResourcesPage';
import ProfilePage from './pages/ProfilePage';
import SettingsPage from './pages/SettingsPage';

const App = () => {
  const [currentPage, setCurrentPage] = useState('chat');
  const [isDarkMode, setIsDarkMode] = useState(false);
  
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
        return <ChatPage />;
    }
  };


  return (
    <div className="min-h-screen bg-gray-50 dark:bg-gray-900 flex flex-col">
      <Header 
        currentPage={currentPage}
        onPageChange={setCurrentPage}
        onThemeToggle={handleThemeToggle}
        isDarkMode={isDarkMode}
      />
      
      <main className="flex-1">
        {renderCurrentPage()}
      </main>
      
      <Footer />
    </div>
  );
};

export default App;
