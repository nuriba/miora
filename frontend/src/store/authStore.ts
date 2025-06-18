import { create } from 'zustand';
import { devtools, persist } from 'zustand/middleware';
import { User, AuthTokens } from '../api/types';
import { authApi } from '../api/auth';
import { tokenManager } from '../api/client';

interface AuthState {
  user: User | null;
  tokens: AuthTokens | null;
  isAuthenticated: boolean;
  isLoading: boolean;
  error: string | null;
  
  // Actions
  login: (email: string, password: string) => Promise<void>;
  register: (email: string, password: string, password_confirm: string) => Promise<void>;
  logout: () => Promise<void>;
  refreshToken: () => Promise<void>;
  checkAuth: () => void;
}

export const useAuthStore = create<AuthState>()(
  devtools(
    persist(
      (set, get) => ({
        user: null,
        tokens: null,
        isAuthenticated: false,
        isLoading: false,
        error: null,
        
        login: async (email, password) => {
          set({ isLoading: true, error: null });
          try {
            const response = await authApi.login({ email, password });
            const { user, access, refresh } = response.data;
            
            const tokens = { access, refresh };
            tokenManager.setTokens(tokens);
            
            set({
              user,
              tokens,
              isAuthenticated: true,
              isLoading: false,
            });
          } catch (error: any) {
            set({
              error: error.response?.data?.detail || 'Login failed',
              isLoading: false,
            });
            throw error;
          }
        },
        
        register: async (email, password, password_confirm) => {
          set({ isLoading: true, error: null });
          try {
            const response = await authApi.register({ email, password, password_confirm });
            const { user, access, refresh } = response.data;
            
            const tokens = { access, refresh };
            tokenManager.setTokens(tokens);
            
            set({
              user,
              tokens,
              isAuthenticated: true,
              isLoading: false,
            });
          } catch (error: any) {
            set({
              error: error.response?.data?.detail || 'Registration failed',
              isLoading: false,
            });
            throw error;
          }
        },
        
        logout: async () => {
          set({ isLoading: true });
          try {
            const tokens = get().tokens;
            if (tokens?.refresh) {
              await authApi.logout(tokens.refresh);
            }
          } catch (error) {
            console.error('Logout error:', error);
          } finally {
            tokenManager.clearTokens();
            set({
              user: null,
              tokens: null,
              isAuthenticated: false,
              isLoading: false,
            });
          }
        },
        
        refreshToken: async () => {
          const tokens = get().tokens;
          if (!tokens?.refresh) {
            throw new Error('No refresh token available');
          }
          
          try {
            const response = await authApi.refreshToken(tokens.refresh);
            const newTokens = {
              access: response.data.access,
              refresh: tokens.refresh,
            };
            
            tokenManager.setTokens(newTokens);
            set({ tokens: newTokens });
          } catch (error) {
            get().logout();
            throw error;
          }
        },
        
        checkAuth: () => {
          const tokens = tokenManager.getTokens();
          if (tokens) {
            set({
              tokens,
              isAuthenticated: true,
            });
          }
        },
      }),
      {
        name: 'auth-storage',
        partialize: (state) => ({
          user: state.user,
          tokens: state.tokens,
          isAuthenticated: state.isAuthenticated,
        }),
      }
    )
  )
);