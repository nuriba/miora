// frontend/src/pages/StyleInsights/index.tsx
import React from 'react';
import { useStyleAnalytics } from '../../hooks/useStyleAnalytics';
import ColorPaletteAnalysis from './ColorPaletteAnalysis';
import StyleEvolution from './StyleEvolution';
import FitPreferences from './FitPreferences';
import BrandAffinityMap from './BrandAffinityMap';
import SeasonalTrends from './SeasonalTrends';
import SustainabilityScore from './SustainabilityScore';
import LoadingSpinner from '../../components/common/LoadingSpinner';

const StyleInsights: React.FC = () => {
  const { data: analytics, isLoading, error } = useStyleAnalytics();

  if (isLoading) {
    return (
      <div className="flex justify-center items-center min-h-screen">
        <LoadingSpinner />
      </div>
    );
  }

  if (error) {
    return (
      <div className="text-center py-12">
        <h2 className="text-2xl font-bold text-gray-900 mb-4">Unable to load analytics</h2>
        <p className="text-gray-600">Please try again later or contact support if the problem persists.</p>
      </div>
    );
  }

  if (!analytics) {
    return (
      <div className="text-center py-12">
        <h2 className="text-2xl font-bold text-gray-900 mb-4">No analytics data available</h2>
        <p className="text-gray-600">Start using Miora to see your style insights!</p>
      </div>
    );
  }

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900">Style Insights</h1>
        <p className="mt-2 text-gray-600">
          Discover patterns in your personal style and get insights into your fashion preferences.
        </p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <ColorPaletteAnalysis 
          mostWornColors={analytics.color_frequency}
          colorCombinations={analytics.favorite_color_combinations}
        />
        
        <StyleEvolution 
          timeline={analytics.style_evolution_timeline}
          milestones={[]} // TODO: Add milestones from separate hook
        />
        
        <FitPreferences 
          preferredFits={analytics.preferred_fits}
          sizeHistory={analytics.size_consistency}
        />
        
        <BrandAffinityMap 
          brands={analytics.top_brands}
          loyaltyScore={analytics.brand_loyalty_score}
        />
        
        <SeasonalTrends 
          seasonal={analytics.seasonal_preferences}
          weatherScore={analytics.weather_adaptation_score}
        />
        
        <SustainabilityScore 
          reuseRate={analytics.garment_reuse_rate}
          costPerWear={analytics.cost_per_wear}
          sustainabilityScore={analytics.sustainability_score}
        />
      </div>
    </div>
  );
};

export default StyleInsights;