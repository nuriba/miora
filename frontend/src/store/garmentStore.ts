import { create } from 'zustand';
import { devtools } from 'zustand/middleware';
import type { Garment } from '../api/types';

interface GarmentState {
  selectedGarments: Garment[];
  wardrobeFilter: {
    category: string;
    brand: string;
    search: string;
  };
  
  // Actions
  addToSelection: (garment: Garment) => void;
  removeFromSelection: (garmentId: string) => void;
  clearSelection: () => void;
  setFilter: (filter: Partial<GarmentState['wardrobeFilter']>) => void;
}

export const useGarmentStore = create<GarmentState>()(
  devtools(
    (set) => ({
      selectedGarments: [],
      wardrobeFilter: {
        category: '',
        brand: '',
        search: '',
      },
      
      addToSelection: (garment) =>
        set((state) => ({
          selectedGarments: [...state.selectedGarments, garment],
        })),
      
      removeFromSelection: (garmentId) =>
        set((state) => ({
          selectedGarments: state.selectedGarments.filter(g => g.id !== garmentId),
        })),
      
      clearSelection: () =>
        set({ selectedGarments: [] }),
      
      setFilter: (filter) =>
        set((state) => ({
          wardrobeFilter: { ...state.wardrobeFilter, ...filter },
        })),
    })
  )
);