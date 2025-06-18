import { motion } from 'framer-motion';
import { CheckCircle, AlertCircle, Info, Ruler, TrendingUp } from 'lucide-react';

interface FitScore {
  overall: number;
  chest: number;
  waist: number;
  length: number;
  shoulders: number;
}

interface Props {
  selectedGarments: any[];
  avatar: any;
}

const FitAnalysisPanel: React.FC<Props> = ({ selectedGarments, avatar }) => {
  // Mock fit analysis data - would come from AI analysis
  const fitScore: FitScore = {
    overall: 87,
    chest: 92,
    waist: 85,
    length: 88,
    shoulders: 84,
  };

  const recommendations = [
    {
      type: 'success',
      title: 'Perfect Chest Fit',
      description: 'This garment fits your chest measurements perfectly.',
      icon: CheckCircle,
      color: 'text-green-600',
      bgColor: 'bg-green-50',
    },
    {
      type: 'warning',
      title: 'Slightly Loose Waist',
      description: 'The waist might be 2-3cm looser than your preference.',
      icon: AlertCircle,
      color: 'text-yellow-600',
      bgColor: 'bg-yellow-50',
    },
    {
      type: 'info',
      title: 'Length Recommendation',
      description: 'Consider rolling up sleeves for a more tailored look.',
      icon: Info,
      color: 'text-blue-600',
      bgColor: 'bg-blue-50',
    },
  ];

  const getScoreColor = (score: number) => {
    if (score >= 90) return 'text-green-600';
    if (score >= 80) return 'text-yellow-600';
    return 'text-red-600';
  };

  const getScoreBgColor = (score: number) => {
    if (score >= 90) return 'bg-green-500';
    if (score >= 80) return 'bg-yellow-500';
    return 'bg-red-500';
  };

  if (!selectedGarments.length || !avatar) {
    return (
      <div className="w-80 bg-white/95 backdrop-blur-md border-l border-gray-200 p-6">
        <div className="text-center py-8">
          <Ruler className="h-12 w-12 text-gray-400 mx-auto mb-4" />
          <h3 className="text-lg font-semibold text-gray-900 mb-2">Fit Analysis</h3>
          <p className="text-gray-600">
            Select garments and an avatar to see detailed fit analysis
          </p>
        </div>
      </div>
    );
  }

  return (
    <div className="w-80 bg-white/95 backdrop-blur-md border-l border-gray-200 p-6 overflow-y-auto">
      {/* Overall Fit Score */}
      <div className="mb-6">
        <h3 className="text-lg font-semibold mb-4">Fit Analysis</h3>
        <div className="text-center">
          <div className="relative w-24 h-24 mx-auto mb-3">
            <svg className="w-24 h-24 transform -rotate-90">
              <circle
                cx="48"
                cy="48"
                r="40"
                stroke="currentColor"
                strokeWidth="8"
                fill="none"
                className="text-gray-200"
              />
              <circle
                cx="48"
                cy="48"
                r="40"
                stroke="currentColor"
                strokeWidth="8"
                fill="none"
                strokeDasharray={`${2 * Math.PI * 40}`}
                strokeDashoffset={`${2 * Math.PI * 40 * (1 - fitScore.overall / 100)}`}
                className={getScoreColor(fitScore.overall)}
                strokeLinecap="round"
              />
            </svg>
            <div className="absolute inset-0 flex items-center justify-center">
              <span className={`text-2xl font-bold ${getScoreColor(fitScore.overall)}`}>
                {fitScore.overall}
              </span>
            </div>
          </div>
          <p className="text-sm text-gray-600">Overall Fit Score</p>
        </div>
      </div>

      {/* Detailed Measurements */}
      <div className="mb-6">
        <h4 className="font-semibold mb-3">Fit Breakdown</h4>
        <div className="space-y-3">
          {Object.entries(fitScore).filter(([key]) => key !== 'overall').map(([key, value]) => (
            <div key={key} className="flex items-center justify-between">
              <span className="text-sm text-gray-700 capitalize">{key}</span>
              <div className="flex items-center">
                <div className="w-20 h-2 bg-gray-200 rounded-full mr-3">
                  <div
                    className={`h-2 rounded-full ${getScoreBgColor(value)}`}
                    style={{ width: `${value}%` }}
                  />
                </div>
                <span className={`text-sm font-medium ${getScoreColor(value)}`}>
                  {value}%
                </span>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Recommendations */}
      <div className="mb-6">
        <h4 className="font-semibold mb-3">Recommendations</h4>
        <div className="space-y-3">
          {recommendations.map((rec, index) => (
            <motion.div
              key={index}
              initial={{ opacity: 0, x: 20 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ delay: index * 0.1 }}
              className={`${rec.bgColor} border border-opacity-20 rounded-lg p-3`}
            >
              <div className="flex items-start">
                <rec.icon className={`h-5 w-5 ${rec.color} mr-2 mt-0.5`} />
                <div>
                  <p className={`font-medium text-sm ${rec.color}`}>{rec.title}</p>
                  <p className="text-xs text-gray-600 mt-1">{rec.description}</p>
                </div>
              </div>
            </motion.div>
          ))}
        </div>
      </div>

      {/* Size Suggestions */}
      <div>
        <h4 className="font-semibold mb-3">Size Suggestions</h4>
        <div className="bg-purple-50 border border-purple-200 rounded-lg p-3">
          <div className="flex items-center mb-2">
            <TrendingUp className="h-4 w-4 text-purple-600 mr-2" />
            <span className="text-sm font-medium text-purple-800">
              Recommended Size: M
            </span>
          </div>
          <p className="text-xs text-purple-700">
            Based on your measurements and fit preferences, size M provides 
            the best balance of comfort and style.
          </p>
          <div className="mt-3 flex space-x-2">
            <button className="px-3 py-1 text-xs bg-purple-100 text-purple-700 rounded-full">
              Try Size S
            </button>
            <button className="px-3 py-1 text-xs bg-purple-600 text-white rounded-full">
              Size M ✓
            </button>
            <button className="px-3 py-1 text-xs bg-purple-100 text-purple-700 rounded-full">
              Try Size L
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default FitAnalysisPanel; 