import React from 'react';

interface SeasonalTrendsProps {
  seasonal: Record<string, Record<string, number>>;
  weatherScore: number;
}

const SeasonalTrends: React.FC<SeasonalTrendsProps> = ({ seasonal, weatherScore }) => {
  const seasons = ['spring', 'summer', 'fall', 'winter'];
  const seasonEmojis = {
    spring: '🌸',
    summer: '☀️',
    fall: '🍂',
    winter: '❄️'
  };

  return (
    <div className="bg-white rounded-lg shadow-md p-6">
      <h3 className="text-lg font-semibold text-gray-900 mb-4">Seasonal Trends</h3>
      
      <div className="mb-6">
        <div className="flex items-center justify-between mb-2">
          <h4 className="text-md font-medium text-gray-700">Weather Adaptation</h4>
          <span className="text-lg font-bold text-green-600">
            {((weatherScore || 0) * 100).toFixed(0)}%
          </span>
        </div>
        <div className="w-full h-3 bg-gray-200 rounded-full">
          <div
            className="h-3 bg-green-500 rounded-full"
            style={{ width: `${(weatherScore || 0) * 100}%` }}
          ></div>
        </div>
        <p className="text-xs text-gray-500 mt-1">
          How well you adapt your wardrobe to weather conditions
        </p>
      </div>

      <div>
        <h4 className="text-md font-medium text-gray-700 mb-3">Seasonal Preferences</h4>
        <div className="grid grid-cols-2 gap-3">
          {seasons.map(season => {
            const seasonData = seasonal?.[season] || {};
            const topCategory = Object.entries(seasonData)
              .sort(([, a], [, b]) => b - a)[0];
            
            return (
              <div key={season} className="p-3 bg-gray-50 rounded">
                <div className="flex items-center mb-2">
                  <span className="text-lg mr-2">{seasonEmojis[season as keyof typeof seasonEmojis]}</span>
                  <h5 className="text-sm font-medium text-gray-900 capitalize">{season}</h5>
                </div>
                {topCategory ? (
                  <div>
                    <p className="text-xs text-gray-600 capitalize">{topCategory[0]}</p>
                    <span className="text-xs text-gray-500">{topCategory[1]} items</span>
                  </div>
                ) : (
                  <p className="text-xs text-gray-500">No data</p>
                )}
                
                {Object.keys(seasonData).length > 1 && (
                  <div className="mt-2 flex flex-wrap gap-1">
                    {Object.entries(seasonData).slice(1, 4).map(([category]) => (
                      <span
                        key={category}
                        className="px-1 py-0.5 bg-blue-100 text-blue-700 text-xs rounded"
                      >
                        {category}
                      </span>
                    ))}
                  </div>
                )}
              </div>
            );
          })}
        </div>
      </div>

      {(!seasonal || Object.keys(seasonal).length === 0) && (
        <div className="text-center py-8 text-gray-500">
          <p>No seasonal data available yet.</p>
          <p className="text-sm">Track your outfits throughout the year to see patterns!</p>
        </div>
      )}
    </div>
  );
};

export default SeasonalTrends; 