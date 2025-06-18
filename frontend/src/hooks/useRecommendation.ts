import { useMutation } from '@tanstack/react-query';
import { recommendationApi } from '../api/recommendations';
import toast from 'react-hot-toast';

export const useGetRecommendation = () => {
  return useMutation({
    mutationFn: recommendationApi.getRecommendation,
    onSuccess: (response) => {
      return response.data;
    },
    onError: (error: any) => {
      toast.error(error.response?.data?.detail || 'Failed to get recommendation');
    },
  });
};

export const useProvideFeedback = () => {
  return useMutation({
    mutationFn: recommendationApi.provideFeedback,
    onSuccess: () => {
      toast.success('Thank you for your feedback!');
    },
    onError: (error: any) => {
      toast.error(error.response?.data?.detail || 'Failed to submit feedback');
    },
  });
};