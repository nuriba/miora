import { apiClient } from './client';
import type { PaginatedResponse } from './types';

interface SizeRecommendation {
  id: string;
  avatar_id: string;
  garment_id: string;
  recommended_size: string;
  confidence_score: number;
  alternative_size?: string;
  fit_preference: string;
  user_selected_size?: string;
  user_feedback?: string;
  created_at: string;
}

export const recommendationApi = {
  getRecommendation: (data: {
    avatar_id: string;
    garment_id: string;
    fit_preference?: 'slim' | 'regular' | 'relaxed';
  }) =>
    apiClient.post<{
      recommendation: SizeRecommendation;
      details: {
        recommended_size: string;
        fit_score: number;
        confidence_score: number;
        alternative_size?: string;
        size_scores: Record<string, number>;
      };
    }>('/recommendations/get/', data),
  
  provideFeedback: (data: {
    recommendation_id: string;
    user_selected_size: string;
    user_feedback: 'perfect' | 'too_small' | 'too_large' | 'too_short' | 'too_long';
  }) =>
    apiClient.post('/recommendations/feedback/', data),
  
  getHistory: () =>
    apiClient.get<PaginatedResponse<SizeRecommendation>>('/recommendations/history/'),
};