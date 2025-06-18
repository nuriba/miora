import { useState } from 'react';
import { motion } from 'framer-motion';
import { Camera, Ruler } from 'lucide-react';
import AvatarList from './AvatarList';
import ManualMeasurements from './ManualMeasurements';
import PhotoUpload from './PhotoUpload';
import AvatarPreview from './AvatarPreview';
import { useAvatars } from '../../hooks/useAvatar';

type CreationMethod = 'manual' | 'photo' | null;

const AvatarCreation = () => {
  const [creationMethod, setCreationMethod] = useState<CreationMethod>(null);
  const [selectedAvatarId, setSelectedAvatarId] = useState<string | null>(null);
  const { data: avatars, isLoading } = useAvatars();
  
  const resetCreation = () => {
    setCreationMethod(null);
  };
  
  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900">My Avatars</h1>
        <p className="mt-1 text-lg text-gray-500">
          Create and manage your 3D avatars for virtual try-on
        </p>
      </div>
      
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        {/* Avatar List */}
        <div className="lg:col-span-2">
          <AvatarList
            avatars={avatars || []}
            selectedId={selectedAvatarId}
            onSelect={setSelectedAvatarId}
            isLoading={isLoading}
          />
          
          {/* Creation Options */}
          {!creationMethod && (
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              className="mt-8"
            >
              <h2 className="text-xl font-semibold mb-4">Create New Avatar</h2>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <button
                  onClick={() => setCreationMethod('manual')}
                  className="card hover:shadow-xl group"
                >
                  <Ruler className="h-12 w-12 text-purple-600 mb-4 group-hover:scale-110 transition" />
                  <h3 className="text-lg font-semibold mb-2">Manual Input</h3>
                  <p className="text-gray-600">
                    Enter your body measurements manually for precise fitting
                  </p>
                </button>
                
                <button
                  onClick={() => setCreationMethod('photo')}
                  className="card hover:shadow-xl group"
                >
                  <Camera className="h-12 w-12 text-purple-600 mb-4 group-hover:scale-110 transition" />
                  <h3 className="text-lg font-semibold mb-2">From Photo</h3>
                  <p className="text-gray-600">
                    Upload a photo and let AI generate your avatar automatically
                  </p>
                </button>
              </div>
            </motion.div>
          )}
          
          {/* Creation Forms */}
          {creationMethod === 'manual' && (
            <ManualMeasurements onClose={resetCreation} />
          )}
          
          {creationMethod === 'photo' && (
            <PhotoUpload onClose={resetCreation} />
          )}
        </div>
        
        {/* Avatar Preview */}
        <div className="lg:col-span-1">
          <AvatarPreview avatarId={selectedAvatarId} />
        </div>
      </div>
    </div>
  );
};

export default AvatarCreation;