import React from 'react';

const Footer = () => {
  const currentYear = new Date().getFullYear();

  const footerLinks = {
    learning: [
      { label: 'البرمجة', href: '#programming' },
      { label: 'الرياضيات', href: '#math' },
      { label: 'العلوم', href: '#science' },
      { label: 'التعلم الذاتي', href: '#self-learning' }
    ],
    resources: [
      { label: 'المستندات', href: '#docs' },
      { label: 'الدروس', href: '#tutorials' },
      { label: 'الأمثلة', href: '#examples' },
      { label: 'المساعدة', href: '#help' }
    ],
    company: [
      { label: 'عن BoAI', href: '#about' },
      { label: 'الاتصال', href: '#contact' },
      { label: 'الخصوصية', href: '#privacy' },
      { label: 'الشروط', href: '#terms' }
    ]
  };

  return (
    <footer className="bg-white dark:bg-gray-800 border-t border-gray-200 dark:border-gray-700 mt-auto">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
          {/* Brand Section */}
          <div className="lg:col-span-1">
            <div className="flex items-center space-x-3 mb-4">
              <div className="w-12 h-12 bg-gradient-to-r from-blue-500 to-purple-600 rounded-lg flex items-center justify-center">
                <i className="fas fa-robot text-white text-xl"></i>
              </div>
              <div>
                <h3 className="text-lg font-bold text-gray-900 dark:text-white">BoAI</h3>
                <p className="text-sm text-gray-600 dark:text-gray-400">منصة التعلم الذكي</p>
              </div>
            </div>
            <p className="text-gray-600 dark:text-gray-400 text-sm mb-4">
              مساعدك الذكي للتعلم والبرمجة. نساعدك في رحلة التعلم بذكاء اصطناعي متقدم.
            </p>
            <div className="flex space-x-4">
              <a href="#" className="text-gray-400 hover:text-blue-500 transition-colors">
                <i className="fab fa-twitter text-lg"></i>
              </a>
              <a href="#" className="text-gray-400 hover:text-blue-600 transition-colors">
                <i className="fab fa-linkedin text-lg"></i>
              </a>
              <a href="#" className="text-gray-400 hover:text-purple-600 transition-colors">
                <i className="fab fa-github text-lg"></i>
              </a>
              <a href="#" className="text-gray-400 hover:text-red-500 transition-colors">
                <i className="fab fa-youtube text-lg"></i>
              </a>
            </div>
          </div>

          {/* Learning Links */}
          <div>
            <h4 className="text-sm font-semibold text-gray-900 dark:text-white uppercase tracking-wider mb-4">
              التعلم
            </h4>
            <ul className="space-y-2">
              {footerLinks.learning.map((link, index) => (
                <li key={index}>
                  <a
                    href={link.href}
                    className="text-gray-600 dark:text-gray-400 hover:text-blue-500 dark:hover:text-blue-400 transition-colors text-sm"
                  >
                    {link.label}
                  </a>
                </li>
              ))}
            </ul>
          </div>

          {/* Resources Links */}
          <div>
            <h4 className="text-sm font-semibold text-gray-900 dark:text-white uppercase tracking-wider mb-4">
              المصادر
            </h4>
            <ul className="space-y-2">
              {footerLinks.resources.map((link, index) => (
                <li key={index}>
                  <a
                    href={link.href}
                    className="text-gray-600 dark:text-gray-400 hover:text-blue-500 dark:hover:text-blue-400 transition-colors text-sm"
                  >
                    {link.label}
                  </a>
                </li>
              ))}
            </ul>
          </div>

          {/* Company Links */}
          <div>
            <h4 className="text-sm font-semibold text-gray-900 dark:text-white uppercase tracking-wider mb-4">
              الشركة
            </h4>
            <ul className="space-y-2">
              {footerLinks.company.map((link, index) => (
                <li key={index}>
                  <a
                    href={link.href}
                    className="text-gray-600 dark:text-gray-400 hover:text-blue-500 dark:hover:text-blue-400 transition-colors text-sm"
                  >
                    {link.label}
                  </a>
                </li>
              ))}
            </ul>
          </div>
        </div>

        {/* Bottom Section */}
        <div className="mt-12 pt-8 border-t border-gray-200 dark:border-gray-700">
          <div className="flex flex-col md:flex-row justify-between items-center space-y-4 md:space-y-0">
            <p className="text-sm text-gray-600 dark:text-gray-400">
              © {currentYear} BoAI. جميع الحقوق محفوظة.
            </p>
            <div className="flex items-center space-x-6 text-sm text-gray-600 dark:text-gray-400">
              <span>مصنوع بـ ❤️ للتعلم</span>
              <div className="flex items-center space-x-2">
                <i className="fas fa-heart text-red-500"></i>
                <span>الإصدار 1.0.0</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </footer>
  );
};

export default Footer;
