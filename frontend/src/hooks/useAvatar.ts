import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { avatarApi } from '../api/avatars';
import type { Avatar } from '../api/types';
import toast from 'react-hot-toast';

export const useAvatars = () => {
  return useQuery({
    queryKey: ['avatars'],
    queryFn: async () => {
      const response = await avatarApi.getAvatars();
      return response.data.results;
    },
  });
};

export const useAvatar = (id: string) => {
  return useQuery({
    queryKey: ['avatar', id],
    queryFn: async () => {
      const response = await avatarApi.getAvatar(id);
      return response.data;
    },
    enabled: !!id,
  });
};

export const useCreateAvatar = () => {
  const queryClient = useQueryClient();
  
  return useMutation({
    mutationFn: (data: Partial<Avatar>) => avatarApi.createAvatar(data),
    onSuccess: (response) => {
      queryClient.invalidateQueries({ queryKey: ['avatars'] });
      toast.success('Avatar created successfully!');
      return response.data;
    },
    onError: (error: any) => {
      toast.error(error.response?.data?.detail || 'Failed to create avatar');
    },
  });
};

export const useUpdateAvatar = () => {
  const queryClient = useQueryClient();
  
  return useMutation({
    mutationFn: ({ id, data }: { id: string; data: Partial<Avatar> }) =>
      avatarApi.updateAvatar(id, data),
    onSuccess: (_, variables) => {
      queryClient.invalidateQueries({ queryKey: ['avatars'] });
      queryClient.invalidateQueries({ queryKey: ['avatar', variables.id] });
      toast.success('Avatar updated successfully!');
    },
    onError: (error: any) => {
      toast.error(error.response?.data?.detail || 'Failed to update avatar');
    },
  });
};

export const useDeleteAvatar = () => {
  const queryClient = useQueryClient();
  
  return useMutation({
    mutationFn: (id: string) => avatarApi.deleteAvatar(id),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['avatars'] });
      toast.success('Avatar deleted successfully!');
    },
    onError: (error: any) => {
      toast.error(error.response?.data?.detail || 'Failed to delete avatar');
    },
  });
};

export const useSetActiveAvatar = () => {
  const queryClient = useQueryClient();
  
  return useMutation({
    mutationFn: (id: string) => avatarApi.setActive(id),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['avatars'] });
      toast.success('Active avatar updated!');
    },
    onError: (error: any) => {
      toast.error(error.response?.data?.detail || 'Failed to set active avatar');
    },
  });
};