import React, { useState, useEffect, useRef } from 'react';

const ChatPage = () => {
  const [messages, setMessages] = useState([
    {
      message: "مرحباً بك في BoAI! 👋 أنا مساعدك الذكي للتعلم والبرمجة. يمكنني مساعدتك في البرمجة، الرياضيات، العلوم، والتعلم الذاتي. كيف يمكنني مساعدتك اليوم؟",
      sender: "assistant",
      timestamp: new Date().toISOString()
    }
  ]);
  
  const [isTyping, setIsTyping] = useState(false);
  const [conversationHistory, setConversationHistory] = useState([]);
  const messageEndRef = useRef(null);

  // Load conversation history from localStorage
  useEffect(() => {
    const savedHistory = localStorage.getItem('boai_conversation_history');
    if (savedHistory) {
      try {
        const history = JSON.parse(savedHistory);
        setConversationHistory(history);
      } catch (error) {
        console.error('Error loading conversation history:', error);
      }
    }
  }, []);

  // Save conversation history to localStorage
  useEffect(() => {
    localStorage.setItem('boai_conversation_history', JSON.stringify(conversationHistory));
  }, [conversationHistory]);

  // Scroll to bottom when messages change
  useEffect(() => {
    messageEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  const handleSend = async (message) => {
    const newMessage = {
      message,
      sender: "user",
      timestamp: new Date().toISOString()
    };

    setMessages(prevMessages => [...prevMessages, newMessage]);
    setIsTyping(true);

    try {
      // Simulate API call to backend
      const response = await simulateAIResponse(message);
      
      const assistantMessage = {
        message: response,
        sender: "assistant",
        timestamp: new Date().toISOString()
      };

      setMessages(prevMessages => [...prevMessages, assistantMessage]);
      
      // Update conversation history
      setConversationHistory(prev => [...prev, {
        user: message,
        assistant: response,
        timestamp: new Date().toISOString()
      }]);

    } catch (error) {
      console.error('Error getting AI response:', error);
      
      const errorMessage = {
        message: "عذراً، حدث خطأ في المعالجة. يرجى المحاولة مرة أخرى.",
        sender: "assistant",
        timestamp: new Date().toISOString()
      };
      
      setMessages(prevMessages => [...prevMessages, errorMessage]);
    } finally {
      setIsTyping(false);
    }
  };

  const simulateAIResponse = async (userMessage) => {
    // Simulate API delay
    await new Promise(resolve => setTimeout(resolve, 1500));

    // Enhanced response logic based on keywords
    const responses = {
      'python': 'بايثون لغة برمجة رائعة! هل تريد شرحاً عن أساسياتها أو مشروع معين؟',
      'دالة': 'لتعريف دالة في Python استخدم `def` اسم_الدالة():',
      'كود': 'يمكنني مساعدتك في كتابة وتصحيح الأكواد. ما المشكلة التي تواجهها؟',
      'تعلم': 'أهلاً بك في رحلة التعلم! ما المجال الذي تريد التعلم فيه؟',
      'برمجة': 'البرمجة مهارة رائعة! هل تبدأ بمشروع معين أو تتعلم الأساسيات؟',
      'html': 'HTML هي لغة ترميز لإنشاء صفحات الويب. هل تحتاج مساعدة في HTML؟',
      'css': 'CSS用于 تنسيق صفحات الويب. كيف يمكنني المساعدة؟',
      'javascript': 'JavaScript لغة برمجة للويب. هل تريد تعلم الأساسيات أو مشروع معين؟',
      'react': 'React مكتبة JavaScript لبناء واجهات المستخدم. هل تحتاج مساعدة؟',
      'مشروع': 'رائع! أخبرني أكثر عن المشروع الذي تعمل عليه.',
      'خطأ': 'أخبرني بالخطأ الذي تواجهه وسأساعدك في حله.',
      'شرح': 'أي مفهوم تريد أن أشرحه لك؟',
      'مثال': 'سأعطيك مثالاً عملياً. ما الموضوع الذي تريده؟',
      'شكر': 'على الرحب والسعة! أنا هنا لمساعدتك دائماً.',
      'مرحبا': 'مرحباً بك! كيف يمكنني مساعدتك اليوم؟'
    };

    for (const [keyword, response] of Object.entries(responses)) {
      if (userMessage.toLowerCase().includes(keyword)) {
        return response;
      }
    }

    return 'شكراً لرسالتك! أنا هنا لمساعدتك في التعلم والبرمجة. هل يمكنك توضيح سؤالك أكثر أو اختيار أحد المواضيع التالية: البرمجة، الرياضيات، العلوم، أو التعلم الذاتي؟';
  };

  const startNewSession = () => {
    setMessages([{
      message: "مرحباً بك في BoAI! 👋 أنا مساعدك الذكي للتعلم والبرمجة. كيف يمكنني مساعدتك اليوم؟",
      sender: "assistant",
      timestamp: new Date().toISOString()
    }]);
    setConversationHistory([]);
  };

  const exportConversation = () => {
    const conversationText = conversationHistory
      .map(entry => `المستخدم (${new Date(entry.timestamp).toLocaleString('ar-SA')}): ${entry.user}\nBoAI: ${entry.assistant}\n${'-'.repeat(50)}`)
      .join('\n');
    
    const blob = new Blob([conversationText], { type: 'text/plain' });
    const url = URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.download = `boai_conversation_${new Date().toISOString().split('T')[0]}.txt`;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    URL.revokeObjectURL(url);
  };

  const quickSuggestions = [
    { icon: 'fa-code', text: 'شرح الـ OOP' },
    { icon: 'fa-calculator', text: 'مسألة رياضية' },
    { icon: 'fa-bug', text: 'تصحيح كود' },
    { icon: 'fa-graduation-cap', text: 'خطة تعلم' }
  ];

  return (
    <div className="min-h-screen bg-gray-50 dark:bg-gray-900">
      <div className="max-w-4xl mx-auto p-4">
        {/* Welcome Card */}
        <div className="bg-white dark:bg-gray-800 rounded-2xl shadow-xl mb-6 p-6">
          <div className="flex items-start space-x-4">
            <div className="w-12 h-12 bg-gradient-to-r from-blue-500 to-purple-600 rounded-full flex items-center justify-center flex-shrink-0">
              <i className="fas fa-robot text-white text-lg"></i>
            </div>
            <div className="flex-1">
              <h2 className="text-2xl font-bold text-gray-900 dark:text-white mb-2">مرحباً بك في BoAI! 👋</h2>
              <p className="text-gray-700 dark:text-gray-300 mb-4">
                أنا مساعدك الذكي للتعلم والبرمجة. يمكنني مساعدتك في:
              </p>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-3 mb-4">
                <div className="flex items-center space-x-2 p-3 bg-blue-50 dark:bg-blue-900/20 rounded-lg">
                  <i className="fas fa-code text-blue-500"></i>
                  <span className="text-sm">البرمجة والأكواد</span>
                </div>
                <div className="flex items-center space-x-2 p-3 bg-green-50 dark:bg-green-900/20 rounded-lg">
                  <i className="fas fa-calculator text-green-500"></i>
                  <span className="text-sm">الرياضيات والعلوم</span>
                </div>
                <div className="flex items-center space-x-2 p-3 bg-purple-50 dark:bg-purple-900/20 rounded-lg">
                  <i className="fas fa-graduation-cap text-purple-500"></i>
                  <span className="text-sm">التعلم الذاتي</span>
                </div>
                <div className="flex items-center space-x-2 p-3 bg-orange-50 dark:bg-orange-900/20 rounded-lg">
                  <i className="fas fa-lightbulb text-orange-500"></i>
                  <span className="text-sm">حل المشكلات</span>
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* Chat Messages */}
        <div className="space-y-4 mb-6">
          {messages.map((msg, index) => (
            <div
              key={index}
              className={`flex ${msg.sender === 'user' ? 'justify-end' : 'justify-start'}`}
            >
              <div className={`p-4 max-w-md rounded-2xl ${
                msg.sender === 'user' 
                  ? 'bg-gradient-to-r from-blue-500 to-purple-600 text-white rounded-br-none' 
                  : 'bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 rounded-bl-none'
              }`}>
                <div className="flex items-start space-x-3">
                  {msg.sender === 'assistant' && (
                    <div className="w-8 h-8 bg-gradient-to-r from-blue-500 to-purple-600 rounded-full flex items-center justify-center flex-shrink-0">
                      <i className="fas fa-robot text-white text-sm"></i>
                    </div>
                  )}
                  <div className="flex-1">
                    <p className="text-sm">{msg.message}</p>
                    <p className="text-xs opacity-70 mt-2">
                      {new Date(msg.timestamp).toLocaleString('ar-SA')}
                    </p>
                  </div>
                  {msg.sender === 'user' && (
                    <div className="w-8 h-8 bg-green-500 rounded-full flex items-center justify-center flex-shrink-0">
                      <i className="fas fa-user text-white text-sm"></i>
                    </div>
                  )}
                </div>
              </div>
            </div>
          ))}

          {isTyping && (
            <div className="flex justify-start">
              <div className="p-4 max-w-md bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 rounded-2xl rounded-bl-none">
                <div className="flex items-start space-x-3">
                  <div className="w-8 h-8 bg-gradient-to-r from-blue-500 to-purple-600 rounded-full flex items-center justify-center flex-shrink-0">
                    <i className="fas fa-robot text-white text-sm"></i>
                  </div>
                  <div className="typing-indicator flex space-x-1">
                    <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce"></div>
                    <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{animationDelay: '0.1s'}}></div>
                    <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{animationDelay: '0.2s'}}></div>
                  </div>
                </div>
              </div>
            </div>
          )}
          
          <div ref={messageEndRef} />
        </div>

        {/* Quick Suggestions */}
        <div className="flex flex-wrap gap-2 mb-6">
          {quickSuggestions.map((suggestion, index) => (
            <button
              key={index}
              onClick={() => handleSend(suggestion.text)}
              className="px-4 py-2 bg-gray-100 dark:bg-gray-700 text-gray-700 dark:text-gray-300 rounded-full text-sm hover:bg-gray-200 dark:hover:bg-gray-600 transition-colors flex items-center space-x-2"
            >
              <i className={`fas ${suggestion.icon}`}></i>
              <span>{suggestion.text}</span>
            </button>
          ))}
        </div>

        {/* Chat Input */}
        <div className="bg-white dark:bg-gray-800 rounded-2xl shadow-xl p-4">
          <div className="flex items-end space-x-4">
            <div className="flex-1 relative">
              <textarea
                placeholder="اكتب رسالتك هنا..."
                className="w-full px-4 py-3 border border-gray-300 dark:border-gray-600 rounded-xl resize-none focus:ring-2 focus:ring-blue-500 focus:border-transparent dark:bg-gray-700 dark:text-white"
                rows="1"
                onKeyPress={(e) => {
                  if (e.key === 'Enter' && !e.shiftKey) {
                    e.preventDefault();
                    if (e.target.value.trim()) {
                      handleSend(e.target.value.trim());
                      e.target.value = '';
                    }
                  }
                }}
              />
              
              <div className="absolute left-3 top-3 flex space-x-2">
                <button className="p-1 text-gray-500 hover:text-blue-500 transition-colors rounded">
                  <i className="fas fa-paperclip"></i>
                </button>
                <button className="p-1 text-gray-500 hover:text-blue-500 transition-colors rounded">
                  <i className="fas fa-image"></i>
                </button>
              </div>
            </div>
            
            <button
              onClick={() => {
                const input = document.querySelector('textarea');
                if (input.value.trim()) {
                  handleSend(input.value.trim());
                  input.value = '';
                }
              }}
              className="px-6 py-3 bg-blue-500 hover:bg-blue-600 text-white rounded-xl transition-colors flex items-center space-x-2"
            >
              <i className="fas fa-paper-plane"></i>
              <span>إرسال</span>
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ChatPage;
