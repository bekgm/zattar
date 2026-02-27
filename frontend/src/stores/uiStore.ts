import { create } from 'zustand'
import { devtools } from 'zustand/middleware'

interface UIState {
  isSidebarOpen: boolean
  isSearchOpen: boolean
  isFilterOpen: boolean
  selectedCategory: string | null

  // Actions
  toggleSidebar: () => void
  toggleSearch: () => void
  toggleFilter: () => void
  setCategory: (category: string | null) => void
  closeSidebar: () => void
}

export const useUIStore = create<UIState>()(
  devtools((set) => ({
    isSidebarOpen: false,
    isSearchOpen: false,
    isFilterOpen: false,
    selectedCategory: null,

    toggleSidebar: () => set((state) => ({ isSidebarOpen: !state.isSidebarOpen })),
    toggleSearch: () => set((state) => ({ isSearchOpen: !state.isSearchOpen })),
    toggleFilter: () => set((state) => ({ isFilterOpen: !state.isFilterOpen })),
    setCategory: (category) => set({ selectedCategory: category }),
    closeSidebar: () => set({ isSidebarOpen: false }),
  }))
)
