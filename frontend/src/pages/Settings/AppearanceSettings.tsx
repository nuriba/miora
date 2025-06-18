import { useState } from 'react';
import { Sun, Moon, Monitor, Layout } from 'lucide-react';

const AppearanceSettings = () => {
  const [appearance, setAppearance] = useState({
    theme: 'system',
    color_scheme: 'purple',
    font_size: 'medium',
    compact_mode: false,
  });
  
  const colorSchemes = [
    { id: 'purple', color: 'bg-purple-600', label: 'Purple' },
    { id: 'blue', color: 'bg-blue-600', label: 'Blue' },
    { id: 'green', color: 'bg-green-600', label: 'Green' },
    { id: 'pink', color: 'bg-pink-600', label: 'Pink' },
    { id: 'orange', color: 'bg-orange-600', label: 'Orange' },
  ];
  
  return (
    <div className="space-y-6">
      {/* Theme */}
      <div className="bg-white rounded-xl shadow-lg p-6">
        <h2 className="text-xl font-semibold mb-6">Theme</h2>
        
        <div className="grid grid-cols-3 gap-4">
          <button
            onClick={() => setAppearance({ ...appearance, theme: 'light' })}
            className={`p-4 rounded-xl border-2 transition ${
              appearance.theme === 'light'
                ? 'border-purple-600 bg-purple-50'
                : 'border-gray-200 hover:border-gray-300'
            }`}
          >
            <Sun className="h-8 w-8 mx-auto mb-2 text-yellow-500" />
            <p className="font-medium">Light</p>
          </button>
          
          <button
            onClick={() => setAppearance({ ...appearance, theme: 'dark' })}
            className={`p-4 rounded-xl border-2 transition ${
              appearance.theme === 'dark'
                ? 'border-purple-600 bg-purple-50'
                : 'border-gray-200 hover:border-gray-300'
            }`}
          >
            <Moon className="h-8 w-8 mx-auto mb-2 text-gray-700" />
            <p className="font-medium">Dark</p>
          </button>
          
          <button
            onClick={() => setAppearance({ ...appearance, theme: 'system' })}
            className={`p-4 rounded-xl border-2 transition ${
              appearance.theme === 'system'
                ? 'border-purple-600 bg-purple-50'
                : 'border-gray-200 hover:border-gray-300'
            }`}
          >
            <Monitor className="h-8 w-8 mx-auto mb-2 text-gray-500" />
            <p className="font-medium">System</p>
          </button>
        </div>
      </div>
      
      {/* Color Scheme */}
      <div className="bg-white rounded-xl shadow-lg p-6">
        <h2 className="text-xl font-semibold mb-6">Color Scheme</h2>
        
        <div className="flex space-x-4">
          {colorSchemes.map((scheme) => (
            <button
              key={scheme.id}
              onClick={() => setAppearance({ ...appearance, color_scheme: scheme.id })}
              className={`relative ${
                appearance.color_scheme === scheme.id ? 'ring-2 ring-offset-2 ring-purple-600' : ''
              } rounded-lg`}
            >
              <div className={`w-16 h-16 ${scheme.color} rounded-lg`} />
              <p className="text-sm mt-2">{scheme.label}</p>
            </button>
          ))}
        </div>
      </div>
      
      {/* Typography */}
      <div className="bg-white rounded-xl shadow-lg p-6">
        <h2 className="text-xl font-semibold mb-6">Typography</h2>
        
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-3">
            Font Size
          </label>
          <div className="flex space-x-4">
            {['small', 'medium', 'large'].map((size) => (
              <button
                key={size}
                onClick={() => setAppearance({ ...appearance, font_size: size })}
                className={`px-6 py-2 rounded-lg capitalize ${
                  appearance.font_size === size
                    ? 'bg-purple-600 text-white'
                    : 'bg-gray-100 hover:bg-gray-200'
                }`}
              >
                {size}
              </button>
            ))}
          </div>
        </div>
      </div>
      
      {/* Layout */}
      <div className="bg-white rounded-xl shadow-lg p-6">
        <h2 className="text-xl font-semibold mb-6">Layout</h2>
        
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-3">
            <Layout className="h-5 w-5 text-gray-400" />
            <div>
              <p className="font-medium">Compact Mode</p>
              <p className="text-sm text-gray-500">
                Show more content with smaller spacing
              </p>
            </div>
          </div>
          <button
            onClick={() => setAppearance({ ...appearance, compact_mode: !appearance.compact_mode })}
            className={`relative inline-flex h-6 w-11 items-center rounded-full transition ${
              appearance.compact_mode ? 'bg-purple-600' : 'bg-gray-200'
            }`}
          >
            <span
              className={`inline-block h-4 w-4 transform rounded-full bg-white transition ${
                appearance.compact_mode ? 'translate-x-6' : 'translate-x-1'
              }`}
            />
          </button>
        </div>
      </div>
      
      {/* Preview */}
      <div className="bg-gray-50 rounded-xl p-6">
        <p className="text-sm text-gray-600 mb-4">Preview</p>
        <div className={`bg-white rounded-lg p-4 shadow ${
          appearance.font_size === 'small' ? 'text-sm' :
          appearance.font_size === 'large' ? 'text-lg' : ''
        }`}>
          <h3 className="font-semibold mb-2">This is how your content will look</h3>
          <p className="text-gray-600">
            Your selected theme and preferences will be applied across the entire application.
          </p>
        </div>
      </div>
    </div>
  );
};

export default AppearanceSettings;