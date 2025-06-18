import { useState } from 'react';
import { motion } from 'framer-motion';
import { Plus, Filter, Search, Grid, List } from 'lucide-react';
import GarmentGrid from './GarmentGrid';
import GarmentUpload from './GarmentUpload';
import FilterPanel from './FilterPanel';
import { useGarments } from '../../hooks/useGarment';

const MyWardrobe = () => {
  const [showUpload, setShowUpload] = useState(false);
  const [viewMode, setViewMode] = useState<'grid' | 'list'>('grid');
  const [showFilters, setShowFilters] = useState(false);
  const [filters, setFilters] = useState({
    category: '',
    status: '',
    search: '',
  });
  
  const { data: garments, isLoading } = useGarments(filters);
  
  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <div className="mb-8">
        <div className="flex justify-between items-center">
          <div>
            <h1 className="text-3xl font-bold text-gray-900">My Wardrobe</h1>
            <p className="mt-1 text-lg text-gray-500">
              {garments?.count || 0} items in your virtual closet
            </p>
          </div>
          <button
            onClick={() => setShowUpload(true)}
            className="btn btn-primary"
          >
            <Plus className="h-5 w-5 mr-2" />
            Add Garment
          </button>
        </div>
      </div>
      
      {/* Search and Filters */}
      <div className="mb-6 flex items-center space-x-4">
        <div className="flex-1 relative">
          <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 h-5 w-5 text-gray-400" />
          <input
            type="text"
            value={filters.search}
            onChange={(e) => setFilters({ ...filters, search: e.target.value })}
            placeholder="Search garments..."
            className="w-full pl-10 pr-4 py-2 border-gray-300 rounded-lg shadow-sm focus:ring-purple-500 focus:border-purple-500"
          />
        </div>
        
        <button
          onClick={() => setShowFilters(!showFilters)}
          className={`btn ${showFilters ? 'btn-primary' : 'btn-secondary'}`}
        >
          <Filter className="h-5 w-5 mr-2" />
          Filters
        </button>
        
        <div className="flex border border-gray-300 rounded-lg">
          <button
            onClick={() => setViewMode('grid')}
            className={`p-2 ${viewMode === 'grid' ? 'bg-purple-100 text-purple-600' : 'text-gray-600'}`}
          >
            <Grid className="h-5 w-5" />
          </button>
          <button
            onClick={() => setViewMode('list')}
            className={`p-2 ${viewMode === 'list' ? 'bg-purple-100 text-purple-600' : 'text-gray-600'}`}
          >
            <List className="h-5 w-5" />
          </button>
        </div>
      </div>
      
      {/* Filter Panel */}
      {showFilters && (
        <motion.div
          initial={{ opacity: 0, height: 0 }}
          animate={{ opacity: 1, height: 'auto' }}
          exit={{ opacity: 0, height: 0 }}
          className="mb-6"
        >
          <FilterPanel filters={filters} onChange={setFilters} />
        </motion.div>
      )}
      
      {/* Garment Grid */}
      <GarmentGrid
        garments={garments?.results || []}
        viewMode={viewMode}
        isLoading={isLoading}
        onAddNew={() => setShowUpload(true)}
      />
      
      {/* Upload Modal */}
      {showUpload && (
        <GarmentUpload onClose={() => setShowUpload(false)} />
      )}
    </div>
  );
};

export default MyWardrobe;