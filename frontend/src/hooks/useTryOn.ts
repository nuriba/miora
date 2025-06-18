import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { tryOnApi } from '../api/tryOn';
import toast from 'react-hot-toast';

export const useTryOnSessions = () => {
  return useQuery({
    queryKey: ['tryon-sessions'],
    queryFn: async () => {
      const response = await tryOnApi.getSessions();
      return response.data.results;
    },
  });
};

export const useCreateTryOnSession = () => {
  const queryClient = useQueryClient();
  
  return useMutation({
    mutationFn: tryOnApi.createSession,
    onSuccess: (response) => {
      queryClient.invalidateQueries({ queryKey: ['tryon-sessions'] });
      toast.success('Try-on session created!');
      return response.data;
    },
    onError: (error: any) => {
      toast.error(error.response?.data?.detail || 'Failed to create session');
    },
  });
};

export const useOutfits = (filters?: any) => {
  return useQuery({
    queryKey: ['outfits', filters],
    queryFn: async () => {
      const response = await tryOnApi.getOutfits(filters);
      return response.data;
    },
  });
};

export const useSaveAsOutfit = () => {
  const queryClient = useQueryClient();
  
  return useMutation({
    mutationFn: ({ sessionId, data }: { sessionId: string; data: any }) =>
      tryOnApi.saveAsOutfit(sessionId, data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['outfits'] });
      toast.success('Outfit saved successfully!');
    },
    onError: (error: any) => {
      toast.error(error.response?.data?.detail || 'Failed to save outfit');
    },
  });
};

export const useToggleFavorite = () => {
  const queryClient = useQueryClient();
  
  return useMutation({
    mutationFn: (id: string) => tryOnApi.toggleFavorite(id),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['outfits'] });
    },
    onError: (error: any) => {
      toast.error(error.response?.data?.detail || 'Failed to update favorite');
    },
  });
};