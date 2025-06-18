import { useState } from 'react';
import { useForm } from 'react-hook-form';
import { motion } from 'framer-motion';
import { X, Info, Save } from 'lucide-react';
import { useCreateAvatar } from '../../hooks/useAvatar';

interface MeasurementForm {
  name: string;
  height: number;
  weight?: number;
  chest: number;
  waist: number;
  hips: number;
  shoulder_width?: number;
  arm_length?: number;
  inseam?: number;
  neck?: number;
  body_type: string;
}

interface Props {
  onClose: () => void;
}

const ManualMeasurements: React.FC<Props> = ({ onClose }) => {
  const [step, setStep] = useState(1);
  const createAvatar = useCreateAvatar();
  
  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm<MeasurementForm>({
    defaultValues: {
      body_type: 'average',
    },
  });
  
  const onSubmit = async (data: MeasurementForm) => {
    try {
      await createAvatar.mutateAsync(data);
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
        <h2 className="text-xl font-semibold">Manual Measurements</h2>
        <button
          onClick={onClose}
          className="p-2 hover:bg-gray-100 rounded-lg transition"
        >
          <X className="h-5 w-5" />
        </button>
      </div>
      
      <form onSubmit={handleSubmit(onSubmit)} className="space-y-6">
        {/* Step 1: Basic Info */}
        {step === 1 && (
          <div className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Avatar Name
              </label>
              <input
                {...register('name', { required: 'Name is required' })}
                type="text"
                className="w-full border-gray-300 rounded-lg shadow-sm focus:ring-purple-500 focus:border-purple-500"
                placeholder="e.g., Casual Me, Work Avatar"
              />
              {errors.name && (
                <p className="mt-1 text-sm text-red-600">{errors.name.message}</p>
              )}
            </div>
            
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Body Type
              </label>
              <select
                {...register('body_type')}
                className="w-full border-gray-300 rounded-lg shadow-sm focus:ring-purple-500 focus:border-purple-500"
              >
                <option value="slim">Slim</option>
                <option value="average">Average</option>
                <option value="athletic">Athletic</option>
                <option value="curvy">Curvy</option>
              </select>
            </div>
            
            <div className="grid grid-cols-2 gap-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Height (cm)
                </label>
                <input
                  {...register('height', {
                    required: 'Height is required',
                    min: { value: 100, message: 'Minimum 100cm' },
                    max: { value: 250, message: 'Maximum 250cm' },
                  })}
                  type="number"
                  className="w-full border-gray-300 rounded-lg shadow-sm focus:ring-purple-500 focus:border-purple-500"
                  placeholder="175"
                />
                {errors.height && (
                  <p className="mt-1 text-sm text-red-600">{errors.height.message}</p>
                )}
              </div>
              
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Weight (kg) <span className="text-gray-400">(optional)</span>
                </label>
                <input
                  {...register('weight', {
                    min: { value: 30, message: 'Minimum 30kg' },
                    max: { value: 200, message: 'Maximum 200kg' },
                  })}
                  type="number"
                  className="w-full border-gray-300 rounded-lg shadow-sm focus:ring-purple-500 focus:border-purple-500"
                  placeholder="70"
                />
              </div>
            </div>
            
            <button
              type="button"
              onClick={() => setStep(2)}
              className="w-full btn btn-primary"
            >
              Next: Body Measurements
            </button>
          </div>
        )}
        
        {/* Step 2: Body Measurements */}
        {step === 2 && (
          <div className="space-y-4">
            <div className="bg-purple-50 border border-purple-200 rounded-lg p-4 mb-4">
              <div className="flex items-start">
                <Info className="h-5 w-5 text-purple-600 mr-2 mt-0.5" />
                <div className="text-sm text-purple-800">
                  <p className="font-medium mb-1">Measurement Tips</p>
                  <ul className="list-disc list-inside space-y-1">
                    <li>Use a flexible measuring tape</li>
                    <li>Measure over undergarments for accuracy</li>
                    <li>Keep tape parallel to the floor</li>
                  </ul>
                </div>
              </div>
            </div>
            
            <div className="grid grid-cols-2 gap-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Chest (cm)
                </label>
                <input
                  {...register('chest', {
                    required: 'Chest measurement is required',
                    min: { value: 60, message: 'Minimum 60cm' },
                    max: { value: 150, message: 'Maximum 150cm' },
                  })}
                  type="number"
                  className="w-full border-gray-300 rounded-lg shadow-sm focus:ring-purple-500 focus:border-purple-500"
                  placeholder="95"
                />
                {errors.chest && (
                  <p className="mt-1 text-sm text-red-600">{errors.chest.message}</p>
                )}
              </div>
              
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Waist (cm)
                </label>
                <input
                  {...register('waist', {
                    required: 'Waist measurement is required',
                    min: { value: 50, message: 'Minimum 50cm' },
                    max: { value: 140, message: 'Maximum 140cm' },
                  })}
                  type="number"
                  className="w-full border-gray-300 rounded-lg shadow-sm focus:ring-purple-500 focus:border-purple-500"
                  placeholder="80"
                />
                {errors.waist && (
                  <p className="mt-1 text-sm text-red-600">{errors.waist.message}</p>
                )}
              </div>
              
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Hips (cm)
                </label>
                <input
                  {...register('hips', {
                    required: 'Hips measurement is required',
                    min: { value: 60, message: 'Minimum 60cm' },
                    max: { value: 150, message: 'Maximum 150cm' },
                  })}
                  type="number"
                  className="w-full border-gray-300 rounded-lg shadow-sm focus:ring-purple-500 focus:border-purple-500"
                  placeholder="95"
                />
                {errors.hips && (
                  <p className="mt-1 text-sm text-red-600">{errors.hips.message}</p>
                )}
              </div>
              
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Shoulder Width (cm) <span className="text-gray-400">(optional)</span>
                </label>
                <input
                  {...register('shoulder_width')}
                  type="number"
                  className="w-full border-gray-300 rounded-lg shadow-sm focus:ring-purple-500 focus:border-purple-500"
                  placeholder="45"
                />
              </div>
            </div>
            
            <div className="flex space-x-4">
              <button
                type="button"
                onClick={() => setStep(1)}
                className="flex-1 btn btn-secondary"
              >
                Back
              </button>
              <button
                type="submit"
                disabled={createAvatar.isPending}
                className="flex-1 btn btn-primary"
              >
                {createAvatar.isPending ? (
                  'Creating...'
                ) : (
                  <>
                    <Save className="h-4 w-4 mr-2" />
                    Create Avatar
                  </>
                )}
              </button>
            </div>
          </div>
        )}
      </form>
    </motion.div>
  );
};

export default ManualMeasurements;