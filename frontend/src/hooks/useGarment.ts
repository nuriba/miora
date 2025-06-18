import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { garmentApi } from '../api/garments';
import toast from 'react-hot-toast';

export const useGarments = (filters?: any) => {
  return useQuery({
    queryKey: ['garments', filters],
    queryFn: async () => {
      const response = await garmentApi.getGarments(filters);
      return response.data;
    },
  });
};

export const useGarment = (id: string, includeLog: boolean = false) => {
  return useQuery({
    queryKey: ['garment', id, includeLog],
    queryFn: async () => {
      const response = await garmentApi.getGarment(id, includeLog);
      return response.data;
    },
    enabled: !!id,
  });
};

export const useUploadGarment = () => {
  const queryClient = useQueryClient();
  
  return useMutation({
    mutationFn: garmentApi.uploadGarment,
    onSuccess: (response) => {
      queryClient.invalidateQueries({ queryKey: ['garments'] });
      toast.success('Garment uploaded! Processing started.');
      return response.data;
    },
    onError: (error: any) => {
      toast.error(error.response?.data?.detail || 'Failed to upload garment');
    },
  });
};

export const useDeleteGarment = () => {
  const queryClient = useQueryClient();
  
  return useMutation({
    mutationFn: (id: string) => garmentApi.deleteGarment(id),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['garments'] });
      toast.success('Garment deleted successfully!');
    },
    onError: (error: any) => {
      toast.error(error.response?.data?.detail || 'Failed to delete garment');
    },
  });
};

export const useGarmentCategories = () => {
  return useQuery({
    queryKey: ['garment-categories'],
    queryFn: async () => {
      const response = await garmentApi.getCategories();
      return response.data;
    },
  });
};

export const useProcessingStatus = (id: string, enabled: boolean = false) => {
  return useQuery({
    queryKey: ['garment-processing', id],
    queryFn: async () => {
      const response = await garmentApi.getProcessingStatus(id);
      return response.data;
    },
    enabled: enabled && !!id,
    refetchInterval: enabled ? 5000 : false, // Poll every 5 seconds
  });
};