import { useState } from 'react';
import { motion } from 'framer-motion';
import { Plus, Search, Filter, Share, Heart } from 'lucide-react';

const Outfits = () => {
  const [searchQuery, setSearchQuery] = useState('');
  
  // Mock data - would come from API
  const outfits = [
    {
      id: 1,
      name: 'Casual Friday',
      items: ['Blue Jeans', 'White Shirt', 'Black Sneakers'],
      thumbnail: '/api/placeholder/300/400',
      createdAt: '2024-01-15',
      likes: 12,
      isLiked: true,
    },
    {
      id: 2,
      name: 'Business Meeting',
      items: ['Black Suit', 'White Dress Shirt', 'Black Shoes'],
      thumbnail: '/api/placeholder/300/400',
      createdAt: '2024-01-12',
      likes: 8,
      isLiked: false,
    },
    {
      id: 3,
      name: 'Weekend Vibes',
      items: ['Denim Jacket', 'White T-Shirt', 'Khaki Pants'],
      thumbnail: '/api/placeholder/300/400',
      createdAt: '2024-01-10',
      likes: 15,
      isLiked: true,
    },
  ];
  
  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      {/* Header */}
      <div className="flex justify-between items-center mb-8">
        <div>
          <h1 className="text-3xl font-bold text-gray-900">My Outfits</h1>
          <p className="text-gray-600 mt-1">Save and organize your favorite looks</p>
        </div>
        <button className="btn btn-primary">
          <Plus className="h-5 w-5 mr-2" />
          Create Outfit
        </button>
      </div>
      
      {/* Search and Filters */}
      <div className="flex space-x-4 mb-8">
        <div className="flex-1 relative">
          <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 h-5 w-5" />
          <input
            type="text"
            placeholder="Search outfits..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            className="w-full pl-10 pr-4 py-3 border border-gray-300 rounded-lg focus:ring-purple-500 focus:border-purple-500"
          />
        </div>
        <button className="btn btn-secondary">
          <Filter className="h-5 w-5 mr-2" />
          Filter
        </button>
      </div>
      
      {/* Outfits Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {outfits.map((outfit, index) => (
          <motion.div
            key={outfit.id}
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: index * 0.1 }}
            className="card group hover:shadow-xl"
          >
            {/* Outfit Thumbnail */}
            <div className="aspect-[3/4] bg-gradient-to-br from-purple-100 to-pink-100 rounded-lg mb-4 overflow-hidden">
              <div className="w-full h-full flex items-center justify-center text-gray-400">
                <div className="text-center">
                  <div className="w-24 h-32 bg-purple-200 rounded-lg mx-auto mb-2" />
                  <p className="text-sm">Outfit Preview</p>
                </div>
              </div>
            </div>
            
            {/* Outfit Info */}
            <div className="space-y-3">
              <h3 className="font-semibold text-lg">{outfit.name}</h3>
              <div className="text-sm text-gray-600">
                <p>{outfit.items.length} items</p>
                <p className="truncate">{outfit.items.join(', ')}</p>
              </div>
              
              {/* Actions */}
              <div className="flex items-center justify-between pt-3 border-t border-gray-100">
                <div className="flex items-center space-x-2">
                  <button 
                    className={`p-2 rounded-lg transition ${
                      outfit.isLiked 
                        ? 'text-red-500 bg-red-50' 
                        : 'text-gray-400 hover:text-red-500 hover:bg-red-50'
                    }`}
                  >
                    <Heart className={`h-4 w-4 ${outfit.isLiked ? 'fill-current' : ''}`} />
                  </button>
                  <span className="text-sm text-gray-500">{outfit.likes}</span>
                </div>
                
                <button className="p-2 text-gray-400 hover:text-purple-600 hover:bg-purple-50 rounded-lg transition">
                  <Share className="h-4 w-4" />
                </button>
              </div>
            </div>
          </motion.div>
        ))}
      </div>
      
      {/* Empty State */}
      {outfits.length === 0 && (
        <div className="text-center py-12">
          <div className="w-32 h-32 bg-gray-200 rounded-full mx-auto mb-4 flex items-center justify-center">
            <Plus className="h-12 w-12 text-gray-400" />
          </div>
          <h3 className="text-lg font-medium text-gray-900 mb-2">No outfits yet</h3>
          <p className="text-gray-600 mb-6">Start creating outfits from your wardrobe</p>
          <button className="btn btn-primary">Create Your First Outfit</button>
        </div>
      )}
    </div>
  );
};

export default Outfits; 