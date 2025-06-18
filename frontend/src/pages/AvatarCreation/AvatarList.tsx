import { motion } from 'framer-motion';
import { Check, Edit2, Trash2, User } from 'lucide-react';
import type { Avatar } from '../../api/types';
import { useSetActiveAvatar, useDeleteAvatar } from '../../hooks/useAvatar';
import { formatDate } from '../../utils/formatters';

interface Props {
  avatars: Avatar[];
  selectedId: string | null;
  onSelect: (id: string | null) => void;
  isLoading: boolean;
}

const AvatarList: React.FC<Props> = ({ avatars, selectedId, onSelect, isLoading }) => {
  const setActive = useSetActiveAvatar();
  const deleteAvatar = useDeleteAvatar();
  
  const handleSetActive = async (id: string) => {
    await setActive.mutateAsync(id);
  };
  
  const handleDelete = async (id: string) => {
    if (window.confirm('Are you sure you want to delete this avatar?')) {
      await deleteAvatar.mutateAsync(id);
    }
  };
  
  if (isLoading) {
    return (
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {[...Array(4)].map((_, i) => (
          <div key={i} className="card animate-pulse">
            <div className="h-32 bg-gray-200 rounded-lg mb-4" />
            <div className="h-4 bg-gray-200 rounded w-3/4 mb-2" />
            <div className="h-4 bg-gray-200 rounded w-1/2" />
          </div>
        ))}
      </div>
    );
  }
  
  if (avatars.length === 0) {
    return (
      <div className="text-center py-12 bg-gray-50 rounded-lg">
        <User className="h-12 w-12 text-gray-400 mx-auto mb-4" />
        <p className="text-gray-600">No avatars yet. Create your first avatar to get started!</p>
      </div>
    );
  }
  
  return (
    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
      {avatars.map((avatar) => (
        <motion.div
          key={avatar.id}
          layout
          onClick={() => onSelect(avatar.id)}
          className={`card cursor-pointer transition-all ${
            selectedId === avatar.id ? 'ring-2 ring-purple-500' : ''
          } ${avatar.is_active ? 'border-purple-500' : ''}`}
        >
          <div className="flex items-start justify-between mb-4">
            <div className="flex-1">
              <h3 className="text-lg font-semibold flex items-center">
                {avatar.name}
                {avatar.is_active && (
                  <span className="ml-2 text-xs bg-purple-100 text-purple-600 px-2 py-1 rounded-full">
                    Active
                  </span>
                )}
              </h3>
              <p className="text-sm text-gray-500">
                Created {formatDate(avatar.created_at)}
              </p>
            </div>
            <div className="flex space-x-1">
              {!avatar.is_active && (
                <button
                  onClick={(e) => {
                    e.stopPropagation();
                    handleSetActive(avatar.id);
                  }}
                  className="p-2 text-green-600 hover:bg-green-50 rounded-lg transition"
                  title="Set as active"
                >
                  <Check className="h-4 w-4" />
                </button>
              )}
              <button
                onClick={(e) => {
                  e.stopPropagation();
                  // Handle edit
                }}
                className="p-2 text-blue-600 hover:bg-blue-50 rounded-lg transition"
                title="Edit"
              >
                <Edit2 className="h-4 w-4" />
              </button>
              <button
                onClick={(e) => {
                  e.stopPropagation();
                  handleDelete(avatar.id);
                }}
                className="p-2 text-red-600 hover:bg-red-50 rounded-lg transition"
                title="Delete"
              >
                <Trash2 className="h-4 w-4" />
              </button>
            </div>
          </div>
          
          <div className="grid grid-cols-3 gap-2 text-sm">
            <div>
              <span className="text-gray-500">Height:</span>
              <p className="font-medium">{avatar.height} cm</p>
            </div>
            <div>
              <span className="text-gray-500">Chest:</span>
              <p className="font-medium">{avatar.chest} cm</p>
            </div>
            <div>
              <span className="text-gray-500">Waist:</span>
              <p className="font-medium">{avatar.waist} cm</p>
            </div>
          </div>
        </motion.div>
      ))}
    </div>
  );
};

export default AvatarList;