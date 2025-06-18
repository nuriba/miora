import { useState } from 'react';
import { motion } from 'framer-motion';
import { 
  User, Shield, Bell, Palette, Globe, CreditCard, 
  HelpCircle, LogOut, ChevronRight 
} from 'lucide-react';
import AccountSettings from './AccountSettings.tsx';
import PrivacySettings from './PrivacySettings.tsx';
import NotificationSettings from './NotificationSettings.tsx';
import AppearanceSettings from './AppearanceSettings.tsx';
import { useAuthStore } from '../../store/authStore';

const Settings = () => {
  const [activeSection, setActiveSection] = useState('account');
  const { logout } = useAuthStore();
  
  const sections = [
    { id: 'account', label: 'Account', icon: User, component: AccountSettings },
    { id: 'privacy', label: 'Privacy & Security', icon: Shield, component: PrivacySettings },
    { id: 'notifications', label: 'Notifications', icon: Bell, component: NotificationSettings },
    { id: 'appearance', label: 'Appearance', icon: Palette, component: AppearanceSettings },
    { id: 'language', label: 'Language & Region', icon: Globe, component: null },
    { id: 'billing', label: 'Billing & Plans', icon: CreditCard, component: null },
    { id: 'help', label: 'Help & Support', icon: HelpCircle, component: null },
  ];
  
  const ActiveComponent = sections.find(s => s.id === activeSection)?.component;
  
  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900">Settings</h1>
        <p className="mt-1 text-lg text-gray-500">
          Manage your account settings and preferences
        </p>
      </div>
      
      <div className="grid grid-cols-1 lg:grid-cols-4 gap-8">
        {/* Sidebar Navigation */}
        <div className="lg:col-span-1">
          <nav className="bg-white rounded-xl shadow-lg p-2">
            {sections.map((section) => (
              <button
                key={section.id}
                onClick={() => setActiveSection(section.id)}
                className={`w-full flex items-center justify-between px-4 py-3 rounded-lg transition ${
                  activeSection === section.id
                    ? 'bg-purple-50 text-purple-600'
                    : 'hover:bg-gray-50 text-gray-700'
                }`}
              >
                <div className="flex items-center space-x-3">
                  <section.icon className="h-5 w-5" />
                  <span className="font-medium">{section.label}</span>
                </div>
                <ChevronRight className="h-4 w-4" />
              </button>
            ))}
            
            <hr className="my-2" />
            
            <button
              onClick={logout}
              className="w-full flex items-center space-x-3 px-4 py-3 rounded-lg text-red-600 hover:bg-red-50 transition"
            >
              <LogOut className="h-5 w-5" />
              <span className="font-medium">Sign Out</span>
            </button>
          </nav>
        </div>
        
        {/* Settings Content */}
        <div className="lg:col-span-3">
          <motion.div
            key={activeSection}
            initial={{ opacity: 0, x: 20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ duration: 0.3 }}
          >
            {ActiveComponent ? (
              <ActiveComponent />
            ) : (
              <div className="bg-white rounded-xl shadow-lg p-8 text-center">
                <p className="text-gray-500">
                  This section is coming soon!
                </p>
              </div>
            )}
          </motion.div>
        </div>
      </div>
    </div>
  );
};

export default Settings;