import axios, { AxiosError } from 'axios';
import { AuthTokens } from './types';

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api/v1';

// Create axios instance
export const apiClient = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Token management
const tokenManager = {
  getTokens(): AuthTokens | null {
    const tokens = localStorage.getItem('auth_tokens');
    return tokens ? JSON.parse(tokens) : null;
  },
  
  setTokens(tokens: AuthTokens) {
    localStorage.setItem('auth_tokens', JSON.stringify(tokens));
  },
  
  clearTokens() {
    localStorage.removeItem('auth_tokens');
  },
};

// Request interceptor
apiClient.interceptors.request.use(
  (config) => {
    const tokens = tokenManager.getTokens();
    if (tokens?.access) {
      config.headers.Authorization = `Bearer ${tokens.access}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

// Response interceptor
apiClient.interceptors.response.use(
  (response) => response,
  async (error: AxiosError) => {
    const originalRequest = error.config as any;
    
    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;
      
      try {
        const tokens = tokenManager.getTokens();
        if (tokens?.refresh) {
          const { data } = await axios.post(`${API_URL}/auth/token/refresh/`, {
            refresh: tokens.refresh,
          });
          
          tokenManager.setTokens({
            access: data.access,
            refresh: tokens.refresh,
          });
          
          originalRequest.headers.Authorization = `Bearer ${data.access}`;
          return apiClient(originalRequest);
        }
      } catch (refreshError) {
        tokenManager.clearTokens();
        window.location.href = '/login';
      }
    }
    
    return Promise.reject(error);
  }
);

export { tokenManager };