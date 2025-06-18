import { useState } from 'react';
import { Bell, Mail, MessageSquare, Heart, ShoppingBag, TrendingUp } from 'lucide-react';

const NotificationSettings = () => {
  const [notifications, setNotifications] = useState<Record<string, boolean>>({
    // Email Notifications
    email_marketing: true,
    email_product_updates: true,
    email_tips: false,
    
    // Push Notifications
    push_messages: true,
    push_likes: true,
    push_comments: true,
    push_follows: true,
    push_recommendations: true,
    push_sales: false,
  });
  
  const handleToggle = (key: string) => {
    setNotifications(prev => ({
      ...prev,
      [key]: !prev[key],
    }));
  };
  
  return (
    <div className="space-y-6">
      {/* Email Notifications */}
      <div className="bg-white rounded-xl shadow-lg p-6">
        <h2 className="text-xl font-semibold mb-6">Email Notifications</h2>
        
        <div className="space-y-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-3">
              <Mail className="h-5 w-5 text-gray-400" />
              <div>
                <p className="font-medium">Marketing Emails</p>
                <p className="text-sm text-gray-500">
                  New features, promotions, and fashion tips
                </p>
              </div>
            </div>
            <button
              onClick={() => handleToggle('email_marketing')}
              className={`relative inline-flex h-6 w-11 items-center rounded-full transition ${
                notifications.email_marketing ? 'bg-purple-600' : 'bg-gray-200'
              }`}
            >
              <span
                className={`inline-block h-4 w-4 transform rounded-full bg-white transition ${
                  notifications.email_marketing ? 'translate-x-6' : 'translate-x-1'
                }`}
              />
            </button>
          </div>
          
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-3">
              <TrendingUp className="h-5 w-5 text-gray-400" />
              <div>
                <p className="font-medium">Product Updates</p>
                <p className="text-sm text-gray-500">
                  New features and improvements
                </p>
              </div>
            </div>
            <button
              onClick={() => handleToggle('email_product_updates')}
              className={`relative inline-flex h-6 w-11 items-center rounded-full transition ${
                notifications.email_product_updates ? 'bg-purple-600' : 'bg-gray-200'
              }`}
            >
              <span
                className={`inline-block h-4 w-4 transform rounded-full bg-white transition ${
                  notifications.email_product_updates ? 'translate-x-6' : 'translate-x-1'
                }`}
              />
            </button>
          </div>
          
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-3">
              <Bell className="h-5 w-5 text-gray-400" />
              <div>
                <p className="font-medium">Tips & Tricks</p>
                <p className="text-sm text-gray-500">
                  Get the most out of Miora
                </p>
              </div>
            </div>
            <button
              onClick={() => handleToggle('email_tips')}
              className={`relative inline-flex h-6 w-11 items-center rounded-full transition ${
                notifications.email_tips ? 'bg-purple-600' : 'bg-gray-200'
              }`}
            >
              <span
                className={`inline-block h-4 w-4 transform rounded-full bg-white transition ${
                  notifications.email_tips ? 'translate-x-6' : 'translate-x-1'
                }`}
              />
            </button>
          </div>
        </div>
      </div>
      
      {/* Push Notifications */}
      <div className="bg-white rounded-xl shadow-lg p-6">
        <h2 className="text-xl font-semibold mb-6">Push Notifications</h2>
        
        <div className="space-y-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-3">
              <MessageSquare className="h-5 w-5 text-gray-400" />
              <div>
                <p className="font-medium">Messages</p>
                <p className="text-sm text-gray-500">
                  New messages from other users
                </p>
              </div>
            </div>
            <button
              onClick={() => handleToggle('push_messages')}
              className={`relative inline-flex h-6 w-11 items-center rounded-full transition ${
                notifications.push_messages ? 'bg-purple-600' : 'bg-gray-200'
              }`}
            >
              <span
                className={`inline-block h-4 w-4 transform rounded-full bg-white transition ${
                  notifications.push_messages ? 'translate-x-6' : 'translate-x-1'
                }`}
              />
            </button>
          </div>
          
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-3">
              <Heart className="h-5 w-5 text-gray-400" />
              <div>
                <p className="font-medium">Likes & Reactions</p>
                <p className="text-sm text-gray-500">
                  Someone likes your outfit
                </p>
              </div>
            </div>
            <button
              onClick={() => handleToggle('push_likes')}
              className={`relative inline-flex h-6 w-11 items-center rounded-full transition ${
                notifications.push_likes ? 'bg-purple-600' : 'bg-gray-200'
              }`}
            >
              <span
                className={`inline-block h-4 w-4 transform rounded-full bg-white transition ${
                  notifications.push_likes ? 'translate-x-6' : 'translate-x-1'
                }`}
              />
            </button>
          </div>
          
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-3">
              <ShoppingBag className="h-5 w-5 text-gray-400" />
              <div>
                <p className="font-medium">Sales & Discounts</p>
                <p className="text-sm text-gray-500">
                  Price drops on saved items
                </p>
              </div>
            </div>
            <button
              onClick={() => handleToggle('push_sales')}
              className={`relative inline-flex h-6 w-11 items-center rounded-full transition ${
                notifications.push_sales ? 'bg-purple-600' : 'bg-gray-200'
              }`}
            >
              <span
                className={`inline-block h-4 w-4 transform rounded-full bg-white transition ${
                  notifications.push_sales ? 'translate-x-6' : 'translate-x-1'
                }`}
              />
            </button>
          </div>
        </div>
      </div>
      
      {/* Notification Schedule */}
      <div className="bg-white rounded-xl shadow-lg p-6">
        <h2 className="text-xl font-semibold mb-6">Quiet Hours</h2>
        
        <div className="space-y-4">
          <p className="text-gray-600">
            We won't send you push notifications during these hours
          </p>
          
          <div className="grid grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                From
              </label>
              <input
                type="time"
                defaultValue="22:00"
                className="w-full border-gray-300 rounded-lg shadow-sm focus:ring-purple-500 focus:border-purple-500"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                To
              </label>
              <input
                type="time"
                defaultValue="08:00"
                className="w-full border-gray-300 rounded-lg shadow-sm focus:ring-purple-500 focus:border-purple-500"
              />
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default NotificationSettings;