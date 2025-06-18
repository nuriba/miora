import { useState, useCallback } from 'react';
import { useDropzone } from 'react-dropzone';
import { motion, AnimatePresence } from 'framer-motion';
import { X, Upload, Camera, Link } from 'lucide-react';
import { useForm } from 'react-hook-form';
import toast from 'react-hot-toast';
import { useUploadGarment, useGarmentCategories } from '../../hooks/useGarment';
import { validateImageFile } from '../../utils/validation';

interface Props {
  onClose: () => void;
}

interface UploadForm {
  name: string;
  category: string;
  brand?: string;
  source_url?: string;
  price?: number;
  currency: string;
  color?: string;
  gender: string;
  description?: string;
}

const GarmentUpload: React.FC<Props> = ({ onClose }) => {
  const [uploadMethod, setUploadMethod] = useState<'file' | 'camera' | 'url' | null>(null);
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [previewUrl, setPreviewUrl] = useState<string | null>(null);
  
  const uploadGarment = useUploadGarment();
  const { data: categories } = useGarmentCategories();
  
  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm<UploadForm>({
    defaultValues: {
      currency: 'USD',
      gender: 'unisex',
    },
  });
  
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
      setUploadMethod('file');
    }
  }, []);
  
  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: {
      'image/*': ['.jpg', '.jpeg', '.png', '.webp'],
    },
    maxFiles: 1,
  });
  
  const onSubmit = async (data: UploadForm) => {
    if (!selectedFile && uploadMethod === 'file') {
      toast.error('Please select an image');
      return;
    }
    
    try {
      await uploadGarment.mutateAsync({
        ...data,
        image: selectedFile!,
      });
      onClose();
    } catch (error) {
      // Error handled by mutation
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
            <h2 className="text-2xl font-bold">Add New Garment</h2>
            <button
              onClick={onClose}
              className="p-2 hover:bg-gray-100 rounded-lg transition"
            >
              <X className="h-5 w-5" />
            </button>
          </div>
          
          <form onSubmit={handleSubmit(onSubmit)} className="p-6 space-y-6">
            {/* Upload Method Selection */}
            {!uploadMethod && (
              <div className="space-y-4">
                <h3 className="text-lg font-semibold">Choose Upload Method</h3>
                <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                  <button
                    type="button"
                    onClick={() => setUploadMethod('file')}
                    className="card hover:shadow-lg group"
                  >
                    <Upload className="h-12 w-12 text-purple-600 mb-4 group-hover:scale-110 transition" />
                    <h4 className="font-semibold">Upload File</h4>
                    <p className="text-sm text-gray-600 mt-1">
                      Choose from your device
                    </p>
                  </button>
                  
                  <button
                    type="button"
                    onClick={() => setUploadMethod('camera')}
                    className="card hover:shadow-lg group"
                  >
                    <Camera className="h-12 w-12 text-purple-600 mb-4 group-hover:scale-110 transition" />
                    <h4 className="font-semibold">Take Photo</h4>
                    <p className="text-sm text-gray-600 mt-1">
                      Use your camera
                    </p>
                  </button>
                  
                  <button
                    type="button"
                    onClick={() => setUploadMethod('url')}
                    className="card hover:shadow-lg group"
                  >
                    <Link className="h-12 w-12 text-purple-600 mb-4 group-hover:scale-110 transition" />
                    <h4 className="font-semibold">From URL</h4>
                    <p className="text-sm text-gray-600 mt-1">
                      Import from web
                    </p>
                  </button>
                </div>
              </div>
            )}
            
            {/* File Upload */}
            {uploadMethod === 'file' && (
              <div className="space-y-4">
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
                      <Upload className="h-12 w-12 text-gray-400 mx-auto mb-4" />
                      <p className="text-gray-600">
                        {isDragActive
                          ? 'Drop the image here...'
                          : 'Drag & drop an image here, or click to select'}
                      </p>
                      <p className="text-sm text-gray-500 mt-2">
                        JPEG, PNG, or WebP • Max 10MB
                      </p>
                    </>
                  )}
                </div>
              </div>
            )}
            
            {/* Garment Details */}
            {(uploadMethod && previewUrl) && (
              <div className="space-y-4">
                <h3 className="text-lg font-semibold">Garment Details</h3>
                
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Name *
                  </label>
                  <input
                    {...register('name', { required: 'Name is required' })}
                    type="text"
                    className="w-full border-gray-300 rounded-lg shadow-sm focus:ring-purple-500 focus:border-purple-500"
                    placeholder="e.g., Blue Denim Jacket"
                  />
                  {errors.name && (
                    <p className="mt-1 text-sm text-red-600">{errors.name.message}</p>
                  )}
                </div>
                
                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">
                      Category *
                    </label>
                    <select
                      {...register('category', { required: 'Category is required' })}
                      className="w-full border-gray-300 rounded-lg shadow-sm focus:ring-purple-500 focus:border-purple-500"
                    >
                      <option value="">Select category</option>
                      {categories?.map((cat) => (
                        <option key={cat.value} value={cat.value}>
                          {cat.label}
                        </option>
                      ))}
                    </select>
                    {errors.category && (
                      <p className="mt-1 text-sm text-red-600">{errors.category.message}</p>
                    )}
                  </div>
                  
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">
                      Brand
                    </label>
                    <input
                      {...register('brand')}
                      type="text"
                      className="w-full border-gray-300 rounded-lg shadow-sm focus:ring-purple-500 focus:border-purple-500"
                      placeholder="e.g., Nike, Zara"
                    />
                  </div>
                </div>
                
                <div className="grid grid-cols-3 gap-4">
                  <div className="col-span-2">
                    <label className="block text-sm font-medium text-gray-700 mb-1">
                      Price
                    </label>
                    <input
                      {...register('price', { min: 0 })}
                      type="number"
                      step="0.01"
                      className="w-full border-gray-300 rounded-lg shadow-sm focus:ring-purple-500 focus:border-purple-500"
                      placeholder="99.99"
                    />
                  </div>
                  
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">
                      Currency
                    </label>
                    <select
                      {...register('currency')}
                      className="w-full border-gray-300 rounded-lg shadow-sm focus:ring-purple-500 focus:border-purple-500"
                    >
                      <option value="USD">USD</option>
                      <option value="EUR">EUR</option>
                      <option value="GBP">GBP</option>
                      <option value="TRY">TRY</option>
                    </select>
                  </div>
                </div>
                
                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">
                      Color
                    </label>
                    <input
                      {...register('color')}
                      type="text"
                      className="w-full border-gray-300 rounded-lg shadow-sm focus:ring-purple-500 focus:border-purple-500"
                      placeholder="e.g., Blue, Red, Multi"
                    />
                  </div>
                  
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">
                      Gender
                    </label>
                    <select
                      {...register('gender')}
                      className="w-full border-gray-300 rounded-lg shadow-sm focus:ring-purple-500 focus:border-purple-500"
                    >
                      <option value="unisex">Unisex</option>
                      <option value="male">Male</option>
                      <option value="female">Female</option>
                    </select>
                  </div>
                </div>
                
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Description
                  </label>
                  <textarea
                    {...register('description')}
                    rows={3}
                    className="w-full border-gray-300 rounded-lg shadow-sm focus:ring-purple-500 focus:border-purple-500"
                    placeholder="Optional description or details about this garment..."
                  />
                </div>
              </div>
            )}
            
            {/* Actions */}
            {(uploadMethod && previewUrl) && (
              <div className="flex space-x-4 pt-6 border-t">
                <button
                  type="button"
                  onClick={onClose}
                  className="flex-1 btn btn-secondary"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  disabled={uploadGarment.isPending}
                  className="flex-1 btn btn-primary"
                >
                  {uploadGarment.isPending ? 'Uploading...' : 'Add Garment'}
                </button>
              </div>
            )}
          </form>
        </motion.div>
      </motion.div>
    </AnimatePresence>
  );
};

export default GarmentUpload;