import React from 'react';

interface BrandAffinityMapProps {
  brands: Array<{ brand: string; count: number }>;
  loyaltyScore: number;
}

const BrandAffinityMap: React.FC<BrandAffinityMapProps> = ({ brands, loyaltyScore }) => {
  const maxCount = Math.max(...(brands || []).map(b => b.count), 1);

  return (
    <div className="bg-white rounded-lg shadow-md p-6">
      <h3 className="text-lg font-semibold text-gray-900 mb-4">Brand Affinity</h3>
      
      <div className="mb-6">
        <div className="flex items-center justify-between mb-2">
          <h4 className="text-md font-medium text-gray-700">Brand Loyalty Score</h4>
          <span className="text-lg font-bold text-blue-600">
            {((loyaltyScore || 0) * 100).toFixed(0)}%
          </span>
        </div>
        <div className="w-full h-3 bg-gray-200 rounded-full">
          <div
            className="h-3 bg-blue-500 rounded-full"
            style={{ width: `${(loyaltyScore || 0) * 100}%` }}
          ></div>
        </div>
        <p className="text-xs text-gray-500 mt-1">
          {loyaltyScore > 0.7 ? 'Very loyal' : loyaltyScore > 0.4 ? 'Moderately loyal' : 'Diverse preferences'}
        </p>
      </div>

      <div>
        <h4 className="text-md font-medium text-gray-700 mb-3">Top Brands</h4>
        <div className="space-y-3">
          {(brands || []).slice(0, 8).map((brand, index) => (
            <div key={brand.brand} className="flex items-center justify-between">
              <div className="flex items-center">
                <span className="text-xs font-medium text-gray-500 w-6">#{index + 1}</span>
                <span className="text-sm text-gray-900 capitalize">{brand.brand}</span>
              </div>
              <div className="flex items-center">
                <div className="w-20 h-2 bg-gray-200 rounded-full mr-2">
                  <div
                    className="h-2 bg-green-500 rounded-full"
                    style={{ width: `${(brand.count / maxCount) * 100}%` }}
                  ></div>
                </div>
                <span className="text-sm font-medium text-gray-900 w-8 text-right">
                  {brand.count}
                </span>
              </div>
            </div>
          ))}
        </div>
      </div>

      {(!brands || brands.length === 0) && (
        <div className="text-center py-8 text-gray-500">
          <p>No brand data available yet.</p>
          <p className="text-sm">Add garments with brand information to see your preferences!</p>
        </div>
      )}
    </div>
  );
};

export default BrandAffinityMap; 