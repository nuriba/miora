import { create } from 'zustand';
import { devtools } from 'zustand/middleware';
import type { TryOnSession, Outfit } from '../api/types';

interface TryOnState {
  currentSession: TryOnSession | null;
  savedOutfits: Outfit[];
  fitScore: number;
  recommendedSize: string;
  
  // Actions
  setCurrentSession: (session: TryOnSession | null) => void;
  updateFitScore: (score: number) => void;
  setRecommendedSize: (size: string) => void;
  addSavedOutfit: (outfit: Outfit) => void;
}

export const useTryOnStore = create<TryOnState>()(
  devtools(
    (set) => ({
      currentSession: null,
      savedOutfits: [],
      fitScore: 0,
      recommendedSize: 'M',
      
      setCurrentSession: (session) =>
        set({ currentSession: session }),
      
      updateFitScore: (score) =>
        set({ fitScore: score }),
      
      setRecommendedSize: (size) =>
        set({ recommendedSize: size }),
      
      addSavedOutfit: (outfit) =>
        set((state) => ({
          savedOutfits: [...state.savedOutfits, outfit],
        })),
    })
  )
);