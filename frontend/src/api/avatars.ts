import { apiClient } from './client';
import type { Avatar, PaginatedResponse, ApiResponse } from './types';

export const avatarApi = {
  getAvatars: () =>
    apiClient.get<PaginatedResponse<Avatar>>('/avatars/'),
  
  getAvatar: (id: string) =>
    apiClient.get<Avatar>(`/avatars/${id}/`),
  
  createAvatar: (data: Partial<Avatar>) =>
    apiClient.post<Avatar>('/avatars/', data),
  
  updateAvatar: (id: string, data: Partial<Avatar>) =>
    apiClient.patch<Avatar>(`/avatars/${id}/`, data),
  
  deleteAvatar: (id: string) =>
    apiClient.delete(`/avatars/${id}/`),
  
  setActive: (id: string) =>
    apiClient.post<ApiResponse<{ avatar: Avatar }>>(`/avatars/${id}/set_active/`),
  
  getActive: () =>
    apiClient.get<Avatar>('/avatars/active/'),
  
  generateFromPhoto: (avatarId: string, photo: File) => {
    const formData = new FormData();
    formData.append('photo', photo);
    
    return apiClient.post<{
      task_id: string;
      log_id: string;
      detail: string;
    }>(`/avatars/${avatarId}/generate_from_photo/`, formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
  },
  
  getGenerationLogs: (avatarId: string) =>
    apiClient.get(`/avatars/${avatarId}/generation_logs/`),
};