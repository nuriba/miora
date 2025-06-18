import { apiClient } from './client';
import type { 
  LoginCredentials, 
  RegisterData,  
  User,
} from './types';

export const authApi = {
  login: (credentials: LoginCredentials) => 
    apiClient.post<{ user: User; access: string; refresh: string }>(
      '/auth/login/', 
      credentials
    ),
  
  register: (data: RegisterData) =>
    apiClient.post<{ user: User; access: string; refresh: string }>(
      '/auth/register/',
      data
    ),
  
  logout: (refreshToken: string) =>
    apiClient.post('/auth/logout/', { refresh: refreshToken }),
  
  refreshToken: (refreshToken: string) =>
    apiClient.post<{ access: string }>('/auth/token/refresh/', {
      refresh: refreshToken,
    }),
  
  getProfile: () =>
    apiClient.get<User>('/auth/me/'),
  
  changePassword: (data: { 
    old_password: string; 
    new_password: string; 
    new_password_confirm: string; 
  }) =>
    apiClient.post('/auth/password/change/', data),
  
  resetPassword: (email: string) =>
    apiClient.post('/auth/password/reset/', { email }),
  
  confirmPasswordReset: (data: {
    token: string;
    new_password: string;
    new_password_confirm: string;
  }) =>
    apiClient.post('/auth/password/reset/confirm/', data),
};