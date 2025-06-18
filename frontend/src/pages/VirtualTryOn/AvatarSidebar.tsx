import { motion } from 'framer-motion';
import { Edit2} from 'lucide-react';
import { useAvatarStore } from '../../store/avatarStore';

const AvatarSidebar = () => {
  const { activeAvatar } = useAvatarStore();
  
  return (
    <div className="w-72 bg-white/95 backdrop-blur-md border-r border-gray-200 p-6 overflow-y-auto">
      {/* Avatar Section */}
      <div className="mb-8">
        <h3 className="text-lg font-semibold mb-4">My Avatar</h3>
        <div className="bg-gradient-to-br from-purple-100 to-pink-100 rounded-xl p-4 mb-4">
          <div className="aspect-[3/4] bg-white/50 rounded-lg flex items-center justify-center mb-3">
            {activeAvatar ? (
              <div className="text-center">
                <div className="w-24 h-32 bg-purple-200 rounded-full mx-auto mb-2" />
                <p className="text-sm font-medium">{activeAvatar.name}</p>
              </div>
            ) : (
              <p className="text-gray-500">No avatar selected</p>
            )}
          </div>
          <button className="w-full btn btn-secondary text-sm">
            <Edit2 className="h-4 w-4 mr-2" />
            Edit Avatar
          </button>
        </div>
      </div>
      
      {/* Quick Wardrobe */}
      <div className="mb-8">
        <h3 className="text-lg font-semibold mb-4">Quick Wardrobe</h3>
        <div className="grid grid-cols-2 gap-3">
          {[1, 2, 3, 4].map((i) => (
            <motion.button
              key={i}
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
              className="aspect-square bg-gradient-to-br from-purple-100 to-pink-100 rounded-lg flex items-center justify-center text-2xl hover:shadow-md transition-shadow"
            >
              {i === 1 && '👔'}
              {i === 2 && '👖'}
              {i === 3 && '👗'}
              {i === 4 && '🧥'}
            </motion.button>
          ))}
        </div>
      </div>
      
      {/* Recent Outfits */}
      <div>
        <h3 className="text-lg font-semibold mb-4">Recent Outfits</h3>
        <div className="space-y-2">
          <button className="w-full text-left p-3 bg-gray-50 hover:bg-gray-100 rounded-lg transition">
            <p className="font-medium">Casual Friday</p>
            <p className="text-sm text-gray-500">3 items • Saved yesterday</p>
          </button>
          <button className="w-full text-left p-3 bg-gray-50 hover:bg-gray-100 rounded-lg transition">
            <p className="font-medium">Business Meeting</p>
            <p className="text-sm text-gray-500">4 items • Saved 3 days ago</p>
          </button>
        </div>
      </div>
    </div>
  );
};

export default AvatarSidebar; 