import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { apiClient } from '../api/client';

export interface StyleAnalytics {
  id: number;
  user: number;
  dominant_colors: string[];
  color_frequency: Record<string, number>;
  favorite_color_combinations: string[][];
  preferred_styles: string[];
  style_evolution_timeline: Array<{
    period: string;
    dominant_style: string;
    style_diversity: number;
  }>;
  preferred_fits: Record<string, number>;
  size_consistency: Record<string, Record<string, number>>;
  top_brands: Array<{ brand: string; count: number }>;
  brand_loyalty_score: number;
  seasonal_preferences: Record<string, Record<string, number>>;
  weather_adaptation_score: number;
  garment_reuse_rate: number;
  cost_per_wear: Record<string, number>;
  sustainability_score: number;
  most_worn_items: string[];
  least_worn_items: string[];
  outfit_repetition_rate: number;
  last_updated: string;
  created_at: string;
}

export interface WearEvent {
  id: number;
  garment: number;
  garmentName: string;
  garmentCategory: string;
  dateWorn: string;
  occasion: string;
  weather: string;
  location: string;
  rating: number;
}

export interface StyleMilestone {
  id: number;
  milestoneType: string;
  title: string;
  description: string;
  achievedAt: string;
  data: Record<string, any>;
}

const fetchStyleAnalytics = async (): Promise<StyleAnalytics> => {
  const response = await apiClient.get('/insights/analytics/');
  return response.data;
};

const updateAnalytics = async (): Promise<{ status: string }> => {
  const response = await apiClient.post('/insights/analytics/update/');
  return response.data;
};

const fetchWearEvents = async (): Promise<WearEvent[]> => {
  const response = await apiClient.get('/insights/wear-events/');
  return response.data.results || response.data;
};

const createWearEvent = async (wearEvent: Partial<WearEvent>): Promise<WearEvent> => {
  const response = await apiClient.post('/insights/wear-events/', wearEvent);
  return response.data;
};

const fetchMilestones = async (): Promise<StyleMilestone[]> => {
  const response = await apiClient.get('/insights/milestones/');
  return response.data.results || response.data;
};

export const useStyleAnalytics = () => {
  return useQuery({
    queryKey: ['styleAnalytics'],
    queryFn: fetchStyleAnalytics,
    staleTime: 5 * 60 * 1000, // 5 minutes
  });
};

export const useUpdateAnalytics = () => {
  const queryClient = useQueryClient();
  
  return useMutation({
    mutationFn: updateAnalytics,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['styleAnalytics'] });
    },
  });
};

export const useWearEvents = () => {
  return useQuery({
    queryKey: ['wearEvents'],
    queryFn: fetchWearEvents,
  });
};

export const useCreateWearEvent = () => {
  const queryClient = useQueryClient();
  
  return useMutation({
    mutationFn: createWearEvent,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['wearEvents'] });
      queryClient.invalidateQueries({ queryKey: ['styleAnalytics'] });
    },
  });
};

export const useStyleMilestones = () => {
  return useQuery({
    queryKey: ['styleMilestones'],
    queryFn: fetchMilestones,
  });
}; 