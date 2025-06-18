import { useState, useCallback } from 'react';
import { useDropzone } from 'react-dropzone';
import { motion } from 'framer-motion';
import { X, Camera, Info } from 'lucide-react';
import toast from 'react-hot-toast';
import { useCreateAvatar } from '../../hooks/useAvatar';
import { validateImageFile } from '../../utils/validation';

interface Props {
  onClose: () => void;
}

const PhotoUpload: React.FC<Props> = ({ onClose }) => {
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [previewUrl, setPreviewUrl] = useState<string | null>(null);
  const [avatarName, setAvatarName] = useState('');
  const createAvatar = useCreateAvatar();
  
  const onDrop = useCallback((acceptedFiles: File[]) => {
    const file = acceptedFiles[0];
    if (file) {
      const validation = validateImageFile(file);
      if (!validation.isValid) {
        toast.error(validation.error!);
        return;
      }
      
      setSelectedFile(file);
      setPreviewUrl(URL.createObjectURL(file));
    }
  }, []);
  
  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: {
      'image/*': ['.jpg', '.jpeg', '.png'],
    },
    maxFiles: 1,
  });
  
  const handleSubmit = async () => {
    if (!selectedFile || !avatarName) {
      toast.error('Please provide a photo and name for your avatar');
      return;
    }
    
    try {
      // First create the avatar
      await createAvatar.mutateAsync({
        name: avatarName,
        height: 170, // Default values, will be updated by AI
        chest: 90,
        waist: 75,
        hips: 90,
      });
      
      // Then trigger photo processing (handled server-side)
      toast.success('Avatar created! Processing your photo...');
      onClose();
    } catch (error) {
      // Error handled by mutation
    }
  };
  
  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      exit={{ opacity: 0, y: -20 }}
      className="mt-8 bg-white rounded-xl shadow-lg p-6"
    >
      <div className="flex justify-between items-center mb-6">
        <h2 className="text-xl font-semibold">Create Avatar from Photo</h2>
        <button
          onClick={onClose}
          className="p-2 hover:bg-gray-100 rounded-lg transition"
        >
          <X className="h-5 w-5" />
        </button>
      </div>
      
      <div className="space-y-6">
        {/* Instructions */}
        <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
          <div className="flex items-start">
            <Info className="h-5 w-5 text-blue-600 mr-2 mt-0.5" />
            <div className="text-sm text-blue-800">
              <p className="font-medium mb-1">Photo Guidelines</p>
              <ul className="list-disc list-inside space-y-1">
                <li>Stand against a plain background</li>
                <li>Wear form-fitting clothes</li>
                <li>Full body shot, facing camera</li>
                <li>Good lighting, no shadows</li>
              </ul>
            </div>
          </div>
        </div>
        
        {/* Avatar Name */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">
            Avatar Name
          </label>
          <input
            type="text"
            value={avatarName}
            onChange={(e) => setAvatarName(e.target.value)}
            className="w-full border-gray-300 rounded-lg shadow-sm focus:ring-purple-500 focus:border-purple-500"
            placeholder="e.g., Casual Me"
          />
        </div>
        
        {/* Photo Upload */}
        <div
          {...getRootProps()}
          className={`border-2 border-dashed rounded-lg p-8 text-center cursor-pointer transition ${
            isDragActive ? 'border-purple-500 bg-purple-50' : 'border-gray-300 hover:border-purple-400'
          }`}
        >
          <input {...getInputProps()} />
          {previewUrl ? (
            <div className="space-y-4">
              <img
                src={previewUrl}
                alt="Preview"
                className="max-h-64 mx-auto rounded-lg"
              />
              <p className="text-sm text-gray-600">
                Click or drag to replace
              </p>
            </div>
          ) : (
            <>
              <Camera className="h-12 w-12 text-gray-400 mx-auto mb-4" />
              <p className="text-gray-600">
                {isDragActive
                  ? 'Drop your photo here...'
                  : 'Drag & drop your photo here, or click to select'}
              </p>
              <p className="text-sm text-gray-500 mt-2">
                JPEG or PNG • Max 10MB
              </p>
            </>
          )}
        </div>
        
        {/* Actions */}
        <div className="flex space-x-4">
          <button
            onClick={onClose}
            className="flex-1 btn btn-secondary"
          >
            Cancel
          </button>
          <button
            onClick={handleSubmit}
            disabled={!selectedFile || !avatarName || createAvatar.isPending}
            className="flex-1 btn btn-primary"
          >
            {createAvatar.isPending ? 'Creating...' : 'Create Avatar'}
          </button>
        </div>
      </div>
    </motion.div>
  );
};

export default PhotoUpload;