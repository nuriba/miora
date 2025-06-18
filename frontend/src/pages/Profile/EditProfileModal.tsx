import { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { X, Camera } from 'lucide-react';
import { useForm } from 'react-hook-form';
import toast from 'react-hot-toast';

interface Props {
  onClose: () => void;
}

interface ProfileForm {
  display_name: string;
  bio: string;
  language_preference: string;
  privacy_level: string;
}

const EditProfileModal: React.FC<Props> = ({ onClose }) => {
  const [avatarPreview, _setAvatarPreview] = useState<string | null>(null);
  
  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm<ProfileForm>({
    defaultValues: {
      display_name: '',
      bio: '',
      language_preference: 'en',
      privacy_level: 'private',
    },
  });
  
  const onSubmit = async (_data: ProfileForm) => {
    try {
      // Update profile API call
      toast.success('Profile updated successfully!');
      onClose();
    } catch (error) {
      toast.error('Failed to update profile');
    }
  };
  
  return (
    <AnimatePresence>
      <motion.div
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        exit={{ opacity: 0 }}
        className="fixed inset-0 bg-black bg-opacity-50 z-50 flex items-center justify-center p-4"
        onClick={onClose}
      >
        <motion.div
          initial={{ scale: 0.9, opacity: 0 }}
          animate={{ scale: 1, opacity: 1 }}
          exit={{ scale: 0.9, opacity: 0 }}
          className="bg-white rounded-2xl shadow-xl max-w-2xl w-full max-h-[90vh] overflow-y-auto"
          onClick={(e) => e.stopPropagation()}
        >
          <div className="sticky top-0 bg-white border-b px-6 py-4 flex justify-between items-center">
            <h2 className="text-2xl font-bold">Edit Profile</h2>
            <button
              onClick={onClose}
              className="p-2 hover:bg-gray-100 rounded-lg transition"
            >
              <X className="h-5 w-5" />
            </button>
          </div>
          
          <form onSubmit={handleSubmit(onSubmit)} className="p-6 space-y-6">
            {/* Profile Picture */}
            <div className="flex justify-center">
              <div className="relative">
                <div className="w-32 h-32 bg-gradient-primary rounded-full flex items-center justify-center text-white text-4xl font-bold">
                  {avatarPreview ? (
                    <img
                      src={avatarPreview}
                      alt="Avatar"
                      className="w-full h-full rounded-full object-cover"
                    />
                  ) : (
                    'A'
                  )}
                </div>
                <button
                  type="button"
                  className="absolute bottom-0 right-0 bg-white rounded-full p-2 shadow-lg hover:shadow-xl transition"
                >
                  <Camera className="h-5 w-5 text-gray-600" />
                </button>
              </div>
            </div>
            
            {/* Display Name */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Display Name
              </label>
              <input
                {...register('display_name', { required: 'Display name is required' })}
                type="text"
                className="w-full border-gray-300 rounded-lg shadow-sm focus:ring-purple-500 focus:border-purple-500"
                placeholder="John Doe"
              />
              {errors.display_name && (
                <p className="mt-1 text-sm text-red-600">{errors.display_name.message}</p>
              )}
            </div>
            
            {/* Bio */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Bio
              </label>
              <textarea
                {...register('bio')}
                rows={4}
                className="w-full border-gray-300 rounded-lg shadow-sm focus:ring-purple-500 focus:border-purple-500"
                placeholder="Tell us about yourself..."
              />
            </div>
            
            {/* Language Preference */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Language
              </label>
              <select
                {...register('language_preference')}
                className="w-full border-gray-300 rounded-lg shadow-sm focus:ring-purple-500 focus:border-purple-500"
              >
                <option value="en">English</option>
                <option value="tr">Turkish</option>
                <option value="es">Spanish</option>
                <option value="fr">French</option>
              </select>
            </div>
            
            {/* Privacy Level */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Profile Privacy
              </label>
              <select
                {...register('privacy_level')}
                className="w-full border-gray-300 rounded-lg shadow-sm focus:ring-purple-500 focus:border-purple-500"
              >
                <option value="public">Public - Anyone can see your profile</option>
                <option value="friends">Friends Only - Only friends can see</option>
                <option value="private">Private - Only you can see</option>
              </select>
            </div>
            
            {/* Action Buttons */}
            <div className="flex space-x-4">
              <button
                type="button"
                onClick={onClose}
                className="flex-1 btn btn-secondary"
              >
                Cancel
              </button>
              <button
                type="submit"
                className="flex-1 btn btn-primary"
              >
                Save Changes
              </button>
            </div>
          </form>
        </motion.div>
      </motion.div>
    </AnimatePresence>
  );
};

export default EditProfileModal;