import React from 'react';

interface FitPreferencesProps {
  preferredFits: Record<string, number>;
  sizeHistory: Record<string, Record<string, number>>;
}

const FitPreferences: React.FC<FitPreferencesProps> = ({ preferredFits, sizeHistory }) => {
  const sortedFits = Object.entries(preferredFits || {})
    .sort(([, a], [, b]) => b - a)
    .slice(0, 5);

  return (
    <div className="bg-white rounded-lg shadow-md p-6">
      <h3 className="text-lg font-semibold text-gray-900 mb-4">Fit Preferences</h3>
      
      <div className="mb-6">
        <h4 className="text-md font-medium text-gray-700 mb-3">Preferred Fits (Rating)</h4>
        <div className="space-y-2">
          {sortedFits.map(([fit, rating]) => (
            <div key={fit} className="flex items-center justify-between">
              <span className="text-sm text-gray-600 capitalize">{fit}</span>
              <div className="flex items-center">
                <div className="w-16 h-2 bg-gray-200 rounded-full mr-2">
                  <div
                    className="h-2 bg-blue-500 rounded-full"
                    style={{ width: `${(rating / 5) * 100}%` }}
                  ></div>
                </div>
                <span className="text-sm font-medium text-gray-900">{rating.toFixed(1)}/5</span>
              </div>
            </div>
          ))}
        </div>
      </div>

      <div>
        <h4 className="text-md font-medium text-gray-700 mb-3">Size Consistency</h4>
        <div className="space-y-3">
          {Object.entries(sizeHistory || {}).slice(0, 4).map(([category, sizes]) => (
            <div key={category} className="p-3 bg-gray-50 rounded">
              <h5 className="text-sm font-medium text-gray-900 capitalize mb-2">{category}</h5>
              <div className="flex flex-wrap gap-2">
                {Object.entries(sizes).map(([size, count]) => (
                  <span
                    key={size}
                    className="px-2 py-1 bg-blue-100 text-blue-800 text-xs rounded-full"
                  >
                    {size} ({count})
                  </span>
                ))}
              </div>
            </div>
          ))}
        </div>
      </div>

      {(!preferredFits || Object.keys(preferredFits).length === 0) && (
        <div className="text-center py-8 text-gray-500">
          <p>No fit preference data available yet.</p>
          <p className="text-sm">Rate your outfits to see fit insights!</p>
        </div>
      )}
    </div>
  );
};

export default FitPreferences; 