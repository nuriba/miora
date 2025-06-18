import { motion } from 'framer-motion';
import { Camera, Edit2, Share2, Settings } from 'lucide-react';
import { Link } from 'react-router-dom';
import { User } from '../../api/types';

interface Props {
  user: User | null;
  onEdit: () => void;
}

const ProfileHeader: React.FC<Props> = ({ user, onEdit }) => {
  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      className="bg-white rounded-2xl shadow-lg p-8 mb-8"
    >
      <div className="flex flex-col md:flex-row items-center md:items-start space-y-6 md:space-y-0 md:space-x-8">
        {/* Profile Image */}
        <div className="relative">
          <div className="w-32 h-32 bg-gradient-primary rounded-full flex items-center justify-center text-white text-4xl font-bold">
            {user?.email?.[0].toUpperCase()}
          </div>
          <button className="absolute bottom-0 right-0 bg-white rounded-full p-2 shadow-lg hover:shadow-xl transition">
            <Camera className="h-5 w-5 text-gray-600" />
          </button>
        </div>
        
        {/* Profile Info */}
        <div className="flex-1 text-center md:text-left">
          <h1 className="text-3xl font-bold text-gray-900 mb-2">
            {user?.email?.split('@')[0]}
          </h1>
          <p className="text-gray-600 mb-4">{user?.email}</p>
          
          {/* Bio */}
          <p className="text-gray-700 mb-6 max-w-2xl">
            Fashion enthusiast exploring virtual try-on technology. Love discovering new styles and sharing outfit ideas with the community.
          </p>
          
          {/* Action Buttons */}
          <div className="flex flex-wrap gap-4 justify-center md:justify-start">
            <button 
              onClick={onEdit}
              className="btn btn-primary"
            >
              <Edit2 className="h-4 w-4 mr-2" />
              Edit Profile
            </button>
            <button className="btn btn-secondary">
              <Share2 className="h-4 w-4 mr-2" />
              Share Profile
            </button>
            <Link to="/settings" className="btn btn-secondary">
              <Settings className="h-4 w-4 mr-2" />
              Settings
            </Link>
          </div>
        </div>
      </div>
    </motion.div>
  );
};

export default ProfileHeader;