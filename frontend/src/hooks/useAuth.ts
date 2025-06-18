import { useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuthStore } from '../store/authStore';

export const useAuth = (requireAuth: boolean = true) => {
  const navigate = useNavigate();
  const { isAuthenticated, user, checkAuth } = useAuthStore();
  
  useEffect(() => {
    checkAuth();
    
    if (requireAuth && !isAuthenticated) {
      navigate('/login');
    }
  }, [requireAuth, isAuthenticated, navigate, checkAuth]);
  
  return { isAuthenticated, user };
};