import { useState } from 'react';
import { Eye, Database, Download } from 'lucide-react';

const PrivacySettings = () => {
  const [privacy, setPrivacy] = useState<Record<string, boolean | string>>({
    profile_visibility: 'friends',
    show_activity: true,
    allow_messages: 'everyone',
    share_analytics: true,
  });
  
  const handleToggle = (key: string) => {
    setPrivacy(prev => ({
      ...prev,
      [key]: !prev[key],
    }));
  };
  
  return (
    <div className="space-y-6">
      {/* Profile Privacy */}
      <div className="bg-white rounded-xl shadow-lg p-6">
        <h2 className="text-xl font-semibold mb-6">Profile Privacy</h2>
        
        <div className="space-y-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Who can see your profile?
            </label>
            <select
              value={privacy.profile_visibility as string}
              onChange={(e) => setPrivacy({ ...privacy, profile_visibility: e.target.value })}
              className="w-full border-gray-300 rounded-lg shadow-sm focus:ring-purple-500 focus:border-purple-500"
            >
              <option value="everyone">Everyone</option>
              <option value="friends">Friends Only</option>
              <option value="private">Only Me</option>
            </select>
          </div>
          
          <div className="flex items-center justify-between py-4 border-t">
            <div className="flex items-center space-x-3">
              <Eye className="h-5 w-5 text-gray-400" />
              <div>
                <p className="font-medium">Show Activity Status</p>
                <p className="text-sm text-gray-500">
                  Let others see when you're online
                </p>
              </div>
            </div>
            <button
              onClick={() => handleToggle('show_activity')}
              className={`relative inline-flex h-6 w-11 items-center rounded-full transition ${
                privacy.show_activity ? 'bg-purple-600' : 'bg-gray-200'
              }`}
            >
              <span
                className={`inline-block h-4 w-4 transform rounded-full bg-white transition ${
                  privacy.show_activity ? 'translate-x-6' : 'translate-x-1'
                }`}
              />
            </button>
          </div>
        </div>
      </div>
      
      {/* Communication */}
      <div className="bg-white rounded-xl shadow-lg p-6">
        <h2 className="text-xl font-semibold mb-6">Communication</h2>
        
        <div className="space-y-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Who can send you messages?
            </label>
            <select
              value={privacy.allow_messages as string}
              onChange={(e) => setPrivacy({ ...privacy, allow_messages: e.target.value })}
              className="w-full border-gray-300 rounded-lg shadow-sm focus:ring-purple-500 focus:border-purple-500"
            >
              <option value="everyone">Everyone</option>
              <option value="friends">Friends Only</option>
              <option value="nobody">Nobody</option>
            </select>
          </div>
        </div>
      </div>
      
      {/* Data & Analytics */}
      <div className="bg-white rounded-xl shadow-lg p-6">
        <h2 className="text-xl font-semibold mb-6">Data & Analytics</h2>
        
        <div className="space-y-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-3">
              <Database className="h-5 w-5 text-gray-400" />
              <div>
                <p className="font-medium">Share Anonymous Analytics</p>
                <p className="text-sm text-gray-500">
                  Help brands improve sizing with anonymous data
                </p>
              </div>
            </div>
            <button
              onClick={() => handleToggle('share_analytics')}
              className={`relative inline-flex h-6 w-11 items-center rounded-full transition ${
                privacy.share_analytics ? 'bg-purple-600' : 'bg-gray-200'
              }`}
            >
              <span
                className={`inline-block h-4 w-4 transform rounded-full bg-white transition ${
                  privacy.share_analytics ? 'translate-x-6' : 'translate-x-1'
                }`}
              />
            </button>
          </div>
          
          <div className="pt-4 border-t">
            <button className="flex items-center space-x-2 text-purple-600 hover:text-purple-700 font-medium">
              <Download className="h-5 w-5" />
              <span>Download My Data</span>
            </button>
            <p className="mt-1 text-sm text-gray-500 ml-7">
              Get a copy of all your Miora data
            </p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default PrivacySettings;