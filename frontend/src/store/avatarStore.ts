import { create } from 'zustand';
import { devtools } from 'zustand/middleware';
import { Avatar } from '../api/types';
import { avatarApi } from '../api/avatars';

interface AvatarState {
  avatars: Avatar[];
  activeAvatar: Avatar | null;
  isLoading: boolean;
  error: string | null;
  
  // Actions
  fetchAvatars: () => Promise<void>;
  createAvatar: (data: Partial<Avatar>) => Promise<Avatar>;
  updateAvatar: (id: string, data: Partial<Avatar>) => Promise<void>;
  deleteAvatar: (id: string) => Promise<void>;
  setActiveAvatar: (id: string) => Promise<void>;
  generateFromPhoto: (avatarId: string, photo: File) => Promise<void>;
}

export const useAvatarStore = create<AvatarState>()(
  devtools(
    (set, _get) => ({
      avatars: [],
      activeAvatar: null,
      isLoading: false,
      error: null,
      
      fetchAvatars: async () => {
        set({ isLoading: true, error: null });
        try {
          const response = await avatarApi.getAvatars();
          const avatars = response.data.results;
          const activeAvatar = avatars.find(a => a.is_active) || null;
          
          set({
            avatars,
            activeAvatar,
            isLoading: false,
          });
        } catch (error: any) {
          set({
            error: error.response?.data?.detail || 'Failed to fetch avatars',
            isLoading: false,
          });
        }
      },
      
      createAvatar: async (data) => {
        set({ isLoading: true, error: null });
        try {
          const response = await avatarApi.createAvatar(data);
          const newAvatar = response.data;
          
          set(state => ({
            avatars: [...state.avatars, newAvatar],
            activeAvatar: newAvatar.is_active ? newAvatar : state.activeAvatar,
            isLoading: false,
          }));
          
          return newAvatar;
        } catch (error: any) {
          set({
            error: error.response?.data?.detail || 'Failed to create avatar',
            isLoading: false,
          });
          throw error;
        }
      },
      
      updateAvatar: async (id, data) => {
        set({ isLoading: true, error: null });
        try {
          const response = await avatarApi.updateAvatar(id, data);
          const updatedAvatar = response.data;
          
          set(state => ({
            avatars: state.avatars.map(a => a.id === id ? updatedAvatar : a),
            activeAvatar: state.activeAvatar?.id === id ? updatedAvatar : state.activeAvatar,
            isLoading: false,
          }));
        } catch (error: any) {
          set({
            error: error.response?.data?.detail || 'Failed to update avatar',
            isLoading: false,
          });
          throw error;
        }
      },
      
      deleteAvatar: async (id) => {
        set({ isLoading: true, error: null });
        try {
          await avatarApi.deleteAvatar(id);
          
          set(state => {
            const avatars = state.avatars.filter(a => a.id !== id);
            const activeAvatar = state.activeAvatar?.id === id 
              ? avatars.find(a => a.is_active) || null 
              : state.activeAvatar;
            
            return {
              avatars,
              activeAvatar,
              isLoading: false,
            };
          });
        } catch (error: any) {
          set({
            error: error.response?.data?.detail || 'Failed to delete avatar',
            isLoading: false,
          });
          throw error;
        }
      },
      
      setActiveAvatar: async (id) => {
        set({ isLoading: true, error: null });
        try {
          const response = await avatarApi.setActive(id);
          const updatedAvatar: Avatar = (response.data as any).avatar ?? response.data;
          
          set(state => ({
            avatars: state.avatars.map(a => ({
              ...a,
              is_active: a.id === id,
            })),
            activeAvatar: updatedAvatar,
            isLoading: false,
          }));
        } catch (error: any) {
          set({
            error: error.response?.data?.detail || 'Failed to set active avatar',
            isLoading: false,
          });
          throw error;
        }
      },
      
      generateFromPhoto: async (avatarId, photo) => {
        set({ isLoading: true, error: null });
        try {
          await avatarApi.generateFromPhoto(avatarId, photo);
          // Handle async generation task
          // You might want to poll for status or use websockets
          set({ isLoading: false });
        } catch (error: any) {
          set({
            error: error.response?.data?.detail || 'Failed to generate avatar',
            isLoading: false,
          });
          throw error;
        }
      },
    })
  )
);