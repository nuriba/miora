import { motion } from 'framer-motion';
import { Grid, Heart, Clock, Award } from 'lucide-react';
import OutfitGrid from './OutfitGrid.tsx';
import ActivityFeed from './ActivityFeed.tsx';
import Achievements from './Achievements.tsx';

interface Props {
  activeTab: string;
  onTabChange: (tab: string) => void;
}

const ProfileTabs: React.FC<Props> = ({ activeTab, onTabChange }) => {
  const tabs = [
    { id: 'overview', label: 'Overview', icon: Grid },
    { id: 'favorites', label: 'Favorites', icon: Heart },
    { id: 'activity', label: 'Activity', icon: Clock },
    { id: 'achievements', label: 'Achievements', icon: Award },
  ];
  
  return (
    <div className="bg-white rounded-2xl shadow-lg">
      {/* Tab Navigation */}
      <div className="border-b border-gray-200">
        <div className="flex space-x-8 px-8">
          {tabs.map((tab) => (
            <button
              key={tab.id}
              onClick={() => onTabChange(tab.id)}
              className={`relative py-4 px-1 flex items-center space-x-2 font-medium transition ${
                activeTab === tab.id
                  ? 'text-purple-600'
                  : 'text-gray-500 hover:text-gray-700'
              }`}
            >
              <tab.icon className="h-5 w-5" />
              <span>{tab.label}</span>
              {activeTab === tab.id && (
                <motion.div
                  layoutId="active-tab"
                  className="absolute bottom-0 left-0 right-0 h-0.5 bg-purple-600"
                />
              )}
            </button>
          ))}
        </div>
      </div>
      
      {/* Tab Content */}
      <div className="p-8">
        {activeTab === 'overview' && <OutfitGrid />}
        {activeTab === 'favorites' && <OutfitGrid filterFavorites />}
        {activeTab === 'activity' && <ActivityFeed />}
        {activeTab === 'achievements' && <Achievements />}
      </div>
    </div>
  );
};

export default ProfileTabs;