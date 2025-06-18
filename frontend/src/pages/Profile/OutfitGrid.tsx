import { motion } from 'framer-motion';
import { Heart, Eye } from 'lucide-react';

interface Props {
  filterFavorites?: boolean;
}

const OutfitGrid: React.FC<Props> = ({ filterFavorites = false }) => {
  // Mock data - replace with actual API call
  const outfits = [
    {
      id: '1',
      name: 'Casual Friday',
      thumbnail: '/outfit1.jpg',
      likes: 24,
      views: 156,
      is_favorite: true,
    },
    {
      id: '2',
      name: 'Business Meeting',
      thumbnail: '/outfit2.jpg',
      likes: 18,
      views: 89,
      is_favorite: false,
    },
    // Add more outfits...
  ];
  
  const displayOutfits = filterFavorites 
    ? outfits.filter(o => o.is_favorite)
    : outfits;
  
  return (
    <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-6">
      {displayOutfits.map((outfit, index) => (
        <motion.div
          key={outfit.id}
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: index * 0.1 }}
          className="group cursor-pointer"
        >
          <div className="aspect-[3/4] bg-gray-200 rounded-lg overflow-hidden mb-3 relative">
            {/* Outfit thumbnail would go here */}
            <div className="absolute inset-0 bg-gradient-to-t from-black/50 to-transparent opacity-0 group-hover:opacity-100 transition-opacity">
              <div className="absolute bottom-4 left-4 right-4 text-white">
                <p className="font-semibold">{outfit.name}</p>
                <div className="flex items-center space-x-4 text-sm mt-1">
                  <span className="flex items-center">
                    <Heart className="h-4 w-4 mr-1" />
                    {outfit.likes}
                  </span>
                  <span className="flex items-center">
                    <Eye className="h-4 w-4 mr-1" />
                    {outfit.views}
                  </span>
                </div>
              </div>
            </div>
          </div>
        </motion.div>
      ))}
    </div>
  );
};

export default OutfitGrid;