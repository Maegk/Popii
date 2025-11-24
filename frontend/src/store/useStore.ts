import { create } from 'zustand'
import { AdSet, FatigueScore } from '@/types'

interface AppState {
  // Theme
  darkMode: boolean
  toggleDarkMode: () => void

  // Ad Sets
  adSets: AdSet[]
  setAdSets: (adSets: AdSet[]) => void
  selectedAdSet: AdSet | null
  setSelectedAdSet: (adSet: AdSet | null) => void

  // Fatigue Scores
  fatigueScores: Record<number, FatigueScore>
  setFatigueScore: (adSetId: number, score: FatigueScore) => void

  // Loading states
  isLoading: boolean
  setIsLoading: (loading: boolean) => void
}

export const useStore = create<AppState>((set) => ({
  // Theme
  darkMode: localStorage.getItem('darkMode') === 'true',
  toggleDarkMode: () =>
    set((state) => {
      const newDarkMode = !state.darkMode
      localStorage.setItem('darkMode', String(newDarkMode))
      if (newDarkMode) {
        document.documentElement.classList.add('dark')
      } else {
        document.documentElement.classList.remove('dark')
      }
      return { darkMode: newDarkMode }
    }),

  // Ad Sets
  adSets: [],
  setAdSets: (adSets) => set({ adSets }),
  selectedAdSet: null,
  setSelectedAdSet: (adSet) => set({ selectedAdSet: adSet }),

  // Fatigue Scores
  fatigueScores: {},
  setFatigueScore: (adSetId, score) =>
    set((state) => ({
      fatigueScores: { ...state.fatigueScores, [adSetId]: score },
    })),

  // Loading
  isLoading: false,
  setIsLoading: (loading) => set({ isLoading: loading }),
}))

// Initialize dark mode on app load
if (localStorage.getItem('darkMode') === 'true') {
  document.documentElement.classList.add('dark')
}
