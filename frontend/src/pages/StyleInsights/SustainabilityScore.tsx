import React from 'react';

interface SustainabilityScoreProps {
  reuseRate: number;
  costPerWear: Record<string, number>;
  sustainabilityScore: number;
}

const SustainabilityScore: React.FC<SustainabilityScoreProps> = ({
  reuseRate,
  costPerWear,
  sustainabilityScore
}) => {
  const avgCostPerWear = Object.values(costPerWear || {}).length > 0
    ? Object.values(costPerWear).reduce((sum, cost) => sum + cost, 0) / Object.values(costPerWear).length
    : 0;

  const getScoreColor = (score: number) => {
    if (score >= 0.8) return 'text-green-600';
    if (score >= 0.6) return 'text-yellow-600';
    return 'text-red-600';
  };

  const getScoreLabel = (score: number) => {
    if (score >= 0.8) return 'Excellent';
    if (score >= 0.6) return 'Good';
    if (score >= 0.4) return 'Fair';
    return 'Needs Improvement';
  };

  return (
    <div className="bg-white rounded-lg shadow-md p-6">
      <h3 className="text-lg font-semibold text-gray-900 mb-4">Sustainability Score</h3>
      
      <div className="mb-6 text-center">
        <div className={`text-4xl font-bold mb-2 ${getScoreColor(sustainabilityScore || 0)}`}>
          {((sustainabilityScore || 0) * 100).toFixed(0)}%
        </div>
        <p className={`text-sm font-medium ${getScoreColor(sustainabilityScore || 0)}`}>
          {getScoreLabel(sustainabilityScore || 0)}
        </p>
        <div className="w-full h-4 bg-gray-200 rounded-full mt-3">
          <div
            className="h-4 bg-gradient-to-r from-red-500 via-yellow-500 to-green-500 rounded-full"
            style={{ width: `${(sustainabilityScore || 0) * 100}%` }}
          ></div>
        </div>
      </div>

      <div className="space-y-4">
        <div className="flex items-center justify-between p-3 bg-gray-50 rounded">
          <div>
            <h4 className="text-sm font-medium text-gray-900">Garment Reuse Rate</h4>
            <p className="text-xs text-gray-600">Percentage of wardrobe actively worn</p>
          </div>
          <span className="text-lg font-bold text-blue-600">
            {((reuseRate || 0) * 100).toFixed(0)}%
          </span>
        </div>

        <div className="flex items-center justify-between p-3 bg-gray-50 rounded">
          <div>
            <h4 className="text-sm font-medium text-gray-900">Average Cost Per Wear</h4>
            <p className="text-xs text-gray-600">Cost efficiency of your garments</p>
          </div>
          <span className="text-lg font-bold text-green-600">
            ${avgCostPerWear.toFixed(2)}
          </span>
        </div>

        <div className="p-3 bg-blue-50 rounded">
          <h4 className="text-sm font-medium text-blue-900 mb-2">Sustainability Tips</h4>
          <ul className="text-xs text-blue-700 space-y-1">
            {sustainabilityScore < 0.6 && (
              <>
                <li>• Try to wear items multiple times before washing</li>
                <li>• Experiment with different styling of existing pieces</li>
              </>
            )}
            {reuseRate < 0.7 && (
              <li>• Consider donating items you haven't worn in 6+ months</li>
            )}
            {avgCostPerWear > 50 && (
              <li>• Focus on cost-per-wear when making new purchases</li>
            )}
            <li>• Mix and match existing pieces to create new looks</li>
          </ul>
        </div>
      </div>

      {(!costPerWear || Object.keys(costPerWear).length === 0) && (
        <div className="text-center py-8 text-gray-500">
          <p>No sustainability data available yet.</p>
          <p className="text-sm">Track your outfit usage to see your impact!</p>
        </div>
      )}
    </div>
  );
};

export default SustainabilityScore; 