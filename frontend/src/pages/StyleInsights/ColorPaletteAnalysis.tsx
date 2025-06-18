import React from 'react';

interface ColorPaletteAnalysisProps {
  mostWornColors: Record<string, number>;
  colorCombinations: string[][];
}

const ColorPaletteAnalysis: React.FC<ColorPaletteAnalysisProps> = ({
  mostWornColors,
  colorCombinations
}) => {
  const getColorStyle = (color: string) => ({
    backgroundColor: color.toLowerCase(),
    width: '20px',
    height: '20px',
    borderRadius: '50%',
    display: 'inline-block',
    marginRight: '8px',
    border: '1px solid #e5e7eb'
  });

  const sortedColors = Object.entries(mostWornColors || {})
    .sort(([, a], [, b]) => b - a)
    .slice(0, 10);

  return (
    <div className="bg-white rounded-lg shadow-md p-6">
      <h3 className="text-lg font-semibold text-gray-900 mb-4">Color Palette Analysis</h3>
      
      <div className="mb-6">
        <h4 className="text-md font-medium text-gray-700 mb-3">Most Worn Colors</h4>
        <div className="space-y-2">
          {sortedColors.map(([color, count]) => (
            <div key={color} className="flex items-center justify-between">
              <div className="flex items-center">
                <div style={getColorStyle(color)}></div>
                <span className="text-sm text-gray-600 capitalize">{color}</span>
              </div>
              <span className="text-sm font-medium text-gray-900">{count}</span>
            </div>
          ))}
        </div>
      </div>

      <div>
        <h4 className="text-md font-medium text-gray-700 mb-3">Favorite Color Combinations</h4>
        <div className="space-y-2">
          {(colorCombinations || []).slice(0, 5).map((combination, index) => (
            <div key={index} className="flex items-center">
              {combination.map((color, colorIndex) => (
                <React.Fragment key={colorIndex}>
                  <div style={getColorStyle(color)}></div>
                  {colorIndex < combination.length - 1 && (
                    <span className="mx-1 text-gray-400">+</span>
                  )}
                </React.Fragment>
              ))}
              <span className="ml-2 text-sm text-gray-600 capitalize">
                {combination.join(' + ')}
              </span>
            </div>
          ))}
        </div>
      </div>

      {(!mostWornColors || Object.keys(mostWornColors).length === 0) && (
        <div className="text-center py-8 text-gray-500">
          <p>No color data available yet.</p>
          <p className="text-sm">Add some garments to see your color preferences!</p>
        </div>
      )}
    </div>
  );
};

export default ColorPaletteAnalysis; 