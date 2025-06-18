import { apiClient } from './client';
import type { Garment, PaginatedResponse } from './types';

interface GarmentFilters {
  category?: string;
  status?: string;
  search?: string;
  page?: number;
  page_size?: number;
}

export const garmentApi = {
  getGarments: (filters?: GarmentFilters) =>
    apiClient.get<PaginatedResponse<Garment>>('/garments/garments/', {
      params: filters,
    }),
  
  getGarment: (id: string, includeLog: boolean = false) =>
    apiClient.get<Garment>(`/garments/garments/${id}/`, {
      params: { include_logs: includeLog },
    }),
  
  uploadGarment: (data: {
    name: string;
    category: string;
    image: File;
    brand?: string;
    source_url?: string;
    price?: number;
    currency?: string;
    color?: string;
    gender?: string;
  }) => {
    const formData = new FormData();
    Object.entries(data).forEach(([key, value]) => {
      if (value !== undefined) {
        formData.append(key, value as string | Blob);
      }
    });
    
    return apiClient.post<{
      garment: Garment;
      task_id: string;
      detail: string;
    }>('/garments/garments/upload/', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
  },
  
  deleteGarment: (id: string) =>
    apiClient.delete(`/garments/garments/${id}/`),
  
  reprocessGarment: (id: string) =>
    apiClient.post(`/garments/garments/${id}/reprocess/`),
  
  getProcessingStatus: (id: string) =>
    apiClient.get(`/garments/garments/${id}/processing_status/`),
  
  getCategories: () =>
    apiClient.get<Array<{
      value: string;
      label: string;
      count: number;
    }>>('/garments/garments/categories/'),
  
  getSizeCharts: (filters?: {
    brand?: string;
    garment_type?: string;
    gender?: string;
  }) =>
    apiClient.get('/garments/size-charts/', { params: filters }),
  
  getBrands: () =>
    apiClient.get<string[]>('/garments/size-charts/brands/'),
};