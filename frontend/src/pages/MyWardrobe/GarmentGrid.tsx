import { motion } from 'framer-motion';
import { Heart, ShoppingBag, Eye } from 'lucide-react';
import type { Garment } from '../../api/types';

interface Props {
  garments: Garment[];
  onGarmentSelect?: (garment: Garment) => void;
  isLoading?: boolean;
  viewMode?: 'grid' | 'list';
  onAddNew?: () => void;
}

const GarmentGrid: React.FC<Props> = ({ garments, onGarmentSelect, isLoading, viewMode = 'grid', onAddNew }) => {
  if (isLoading) {
    return (
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
        {[...Array(8)].map((_, i) => (
          <div key={i} className="card animate-pulse">
            <div className="aspect-[3/4] bg-gray-200 rounded-lg mb-4" />
            <div className="h-4 bg-gray-200 rounded mb-2" />
            <div className="h-3 bg-gray-200 rounded w-2/3" />
          </div>
        ))}
      </div>
    );
  }

  if (garments.length === 0) {
    return (
      <div className="text-center py-12">
        <div className="w-32 h-32 bg-gray-200 rounded-full mx-auto mb-4 flex items-center justify-center">
          <ShoppingBag className="h-12 w-12 text-gray-400" />
        </div>
        <h3 className="text-lg font-medium text-gray-900 mb-2">No garments yet</h3>
        <p className="text-gray-600 mb-6">Start building your virtual wardrobe</p>
        <button className="btn btn-primary" onClick={() => onAddNew && onAddNew()}>
          Add Your First Garment
        </button>
      </div>
    );
  }

  const containerClass =
    viewMode === 'list'
      ? 'flex flex-col gap-6'
      : 'grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6';

  return (
    <div className={containerClass}>
      {garments.map((garment, index) => (
        <motion.div
          key={garment.id}
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: index * 0.05 }}
          className="card group hover:shadow-xl cursor-pointer"
          onClick={() => onGarmentSelect && onGarmentSelect(garment)}
        >
          {/* Garment Image */}
          <div className="aspect-[3/4] bg-gradient-to-br from-purple-100 to-pink-100 rounded-lg mb-4 overflow-hidden relative">
            {garment.thumbnail_url || garment.original_image_url ? (
              <img
                src={garment.thumbnail_url || garment.original_image_url}
                alt={garment.name}
                className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-300"
              />
            ) : (
              <div className="w-full h-full flex items-center justify-center text-gray-400">
                <ShoppingBag className="h-12 w-12" />
              </div>
            )}
            
            {/* Overlay */}
            <div className="absolute inset-0 bg-black bg-opacity-0 group-hover:bg-opacity-20 transition-all duration-300 flex items-center justify-center">
              <div className="opacity-0 group-hover:opacity-100 transition-opacity duration-300 flex space-x-2">
                <button className="p-2 bg-white rounded-full shadow-lg hover:scale-110 transition-transform">
                  <Eye className="h-4 w-4 text-gray-700" />
                </button>
                <button className="p-2 bg-white rounded-full shadow-lg hover:scale-110 transition-transform">
                  <Heart className="h-4 w-4 text-gray-700" />
                </button>
              </div>
            </div>
          </div>
          
          {/* Garment Info */}
          <div className="space-y-2">
            <h3 className="font-semibold text-gray-900 truncate">{garment.name}</h3>
            <div className="flex items-center justify-between">
              <p className="text-sm text-gray-600 capitalize">{garment.category}</p>
              {garment.price && (
                <p className="text-sm font-medium text-purple-600">
                  ${garment.price}
                </p>
              )}
            </div>
            {garment.brand && (
              <p className="text-xs text-gray-500">{garment.brand}</p>
            )}
            
            {/* Tags */}
            <div className="flex flex-wrap gap-1 pt-2">
              {garment.color && (
                <span className="px-2 py-1 text-xs bg-gray-100 text-gray-700 rounded-full">
                  {garment.color}
                </span>
              )}
              {garment.gender && garment.gender !== 'unisex' && (
                <span className="px-2 py-1 text-xs bg-purple-100 text-purple-700 rounded-full capitalize">
                  {garment.gender}
                </span>
              )}
            </div>
          </div>
        </motion.div>
      ))}
    </div>
  );
};

export default GarmentGrid; 