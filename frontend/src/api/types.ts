// Auth types
export interface AuthTokens {
    access: string;
    refresh: string;
  }
  
  export interface User {
    id: string;
    email: string;
    is_verified: boolean;
    created_at: string;
    last_login: string | null;
  }
  
  export interface LoginCredentials {
    email: string;
    password: string;
  }
  
  export interface RegisterData extends LoginCredentials {
    password_confirm: string;
  }
  
  // Avatar types
  export interface Avatar {
    id: string;
    name: string;
    is_active: boolean;
    height: number;
    weight?: number;
    chest: number;
    waist: number;
    hips: number;
    shoulder_width?: number;
    arm_length?: number;
    inseam?: number;
    neck?: number;
    skin_tone?: string;
    hair_color?: string;
    hair_style?: string;
    body_type: string;
    model_file_url?: string;
    thumbnail_url?: string;
    created_at: string;
    updated_at: string;
  }
  
  // Garment types
  export interface Garment {
    id: string;
    name: string;
    brand?: string;
    category: string;
    subcategory?: string;
    gender: 'male' | 'female' | 'unisex';
    original_image_url: string;
    thumbnail_url?: string;
    model_3d_url?: string;
    texture_urls: string[];
    source_url?: string;
    price?: number;
    currency: string;
    size_chart?: Record<string, any>;
    available_sizes: string[];
    material_properties?: Record<string, any>;
    color?: string;
    pattern?: string;
    is_private: boolean;
    processing_status: 'pending' | 'processing' | 'completed' | 'failed';
    created_at: string;
    updated_at: string;
  }
  
  // Try-on types
  export interface TryOnSession {
    id: string;
    avatar: Avatar;
    session_name?: string;
    fit_score?: number;
    recommended_size?: string;
    confidence_level?: number;
    garments: TryOnSessionGarment[];
    created_at: string;
    updated_at: string;
  }
  
  export interface TryOnSessionGarment {
    id: string;
    garment: Garment;
    layer_order: number;
    selected_size?: string;
    fit_score?: number;
  }
  
  export interface Outfit {
    id: string;
    avatar: Avatar;
    name: string;
    description?: string;
    thumbnail_url?: string;
    is_favorite: boolean;
    privacy_level: 'private' | 'friends' | 'public';
    garments: OutfitGarment[];
    created_at: string;
    updated_at: string;
  }
  
  export interface OutfitGarment {
    id: string;
    garment: Garment;
    layer_order: number;
    selected_size?: string;
  }
  
  // API Response types
  export interface ApiResponse<T> {
    success: boolean;
    message?: string;
    data?: T;
    errors?: Record<string, string[]>;
  }
  
  export interface PaginatedResponse<T> {
    count: number;
    next: string | null;
    previous: string | null;
    results: T[];
  }