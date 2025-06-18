import { apiClient } from './client';
import type { TryOnSession, Outfit, PaginatedResponse } from './types';

export const tryOnApi = {
  // Sessions
  getSessions: () =>
    apiClient.get<PaginatedResponse<TryOnSession>>('/try-on/sessions/'),
  
  getSession: (id: string) =>
    apiClient.get<TryOnSession>(`/try-on/sessions/${id}/`),
  
  createSession: (data: {
    avatar_id: string;
    garments: Array<{
      garment_id: string;
      layer_order: number;
      selected_size?: string;
    }>;
    session_name?: string;
  }) =>
    apiClient.post<TryOnSession>('/try-on/sessions/', data),
  
  updateGarmentSize: (sessionId: string, garmentId: string, size: string) =>
    apiClient.post(`/try-on/sessions/${sessionId}/update_garment_size/`, {
      garment_id: garmentId,
      size,
    }),
  
  saveAsOutfit: (sessionId: string, data: {
    name: string;
    description?: string;
    privacy_level?: 'private' | 'friends' | 'public';
    is_favorite?: boolean;
  }) =>
    apiClient.post<Outfit>(`/try-on/sessions/${sessionId}/save_as_outfit/`, data),
  
  // Outfits
  getOutfits: (filters?: {
    privacy?: string;
    favorites?: boolean;
  }) =>
    apiClient.get<PaginatedResponse<Outfit>>('/try-on/outfits/', {
      params: filters,
    }),
  
  getOutfit: (id: string) =>
    apiClient.get<Outfit>(`/try-on/outfits/${id}/`),
  
  updateOutfit: (id: string, data: Partial<Outfit>) =>
    apiClient.patch<Outfit>(`/try-on/outfits/${id}/`, data),
  
  deleteOutfit: (id: string) =>
    apiClient.delete(`/try-on/outfits/${id}/`),
  
  toggleFavorite: (id: string) =>
    apiClient.post(`/try-on/outfits/${id}/toggle_favorite/`),
  
  duplicateOutfit: (id: string) =>
    apiClient.post<Outfit>(`/try-on/outfits/${id}/duplicate/`),
  
  tryOnOutfit: (id: string) =>
    apiClient.post<{ session_id: string }>(`/try-on/outfits/${id}/try_on/`),
};