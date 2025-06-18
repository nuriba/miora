import React from 'react';

interface StyleEvolutionProps {
  timeline: Array<{
    period: string;
    dominant_style: string;
    style_diversity: number;
  }>;
  milestones: any[];
}

const StyleEvolution: React.FC<StyleEvolutionProps> = ({ timeline, milestones }) => {
  return (
    <div className="bg-white rounded-lg shadow-md p-6">
      <h3 className="text-lg font-semibold text-gray-900 mb-4">Style Evolution</h3>
      
      <div className="mb-6">
        <h4 className="text-md font-medium text-gray-700 mb-3">Timeline</h4>
        <div className="space-y-3">
          {(timeline || []).map((period, index) => (
            <div key={index} className="flex items-center justify-between p-3 bg-gray-50 rounded">
              <div>
                <span className="text-sm font-medium text-gray-900">{period.period}</span>
                <p className="text-sm text-gray-600 capitalize">{period.dominant_style}</p>
              </div>
              <div className="text-right">
                <span className="text-xs text-gray-500">Diversity</span>
                <p className="text-sm font-medium text-gray-900">{period.style_diversity}</p>
              </div>
            </div>
          ))}
        </div>
      </div>

      <div>
        <h4 className="text-md font-medium text-gray-700 mb-3">Style Milestones</h4>
        <div className="space-y-2">
          {(milestones || []).slice(0, 3).map((milestone, index) => (
            <div key={index} className="p-3 border-l-4 border-blue-500 bg-blue-50">
              <h5 className="text-sm font-medium text-blue-900">{milestone.title}</h5>
              <p className="text-xs text-blue-700">{milestone.description}</p>
              <span className="text-xs text-blue-600">
                {new Date(milestone.achievedAt).toLocaleDateString()}
              </span>
            </div>
          ))}
        </div>
      </div>

      {(!timeline || timeline.length === 0) && (
        <div className="text-center py-8 text-gray-500">
          <p>No style evolution data available yet.</p>
          <p className="text-sm">Keep using Miora to track your style journey!</p>
        </div>
      )}
    </div>
  );
};

export default StyleEvolution; 