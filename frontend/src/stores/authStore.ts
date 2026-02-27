import { create } from 'zustand'
import { devtools } from 'zustand/middleware'
import { User } from '../types'
import { authAPI } from '../api/auth'

interface AuthState {
  user: User | null
  accessToken: string | null
  refreshToken: string | null
  isAuthenticated: boolean
  isLoading: boolean
  error: string | null

  // Actions
  login: (email: string, password: string) => Promise<void>
  register: (data: {
    email: string
    phone: string
    username: string
    password: string
  }) => Promise<void>
  logout: () => void
  loadUser: () => Promise<void>
  setError: (error: string | null) => void
}

export const useAuthStore = create<AuthState>()(
  devtools((set) => ({
    user: null,
    accessToken: localStorage.getItem('access_token'),
    refreshToken: localStorage.getItem('refresh_token'),
    isAuthenticated: !!localStorage.getItem('access_token'),
    isLoading: false,
    error: null,

    login: async (email: string, password: string) => {
      set({ isLoading: true, error: null })
      try {
        const response = await authAPI.login({ email, password })
        localStorage.setItem('access_token', response.access_token)
        localStorage.setItem('refresh_token', response.refresh_token)
        set({
          accessToken: response.access_token,
          refreshToken: response.refresh_token,
          isAuthenticated: true,
          isLoading: false,
        })
      } catch (error: any) {
        set({
          error: error.response?.data?.detail || 'Login failed',
          isLoading: false,
        })
        throw error
      }
    },

    register: async (data) => {
      set({ isLoading: true, error: null })
      try {
        const response = await authAPI.register(data)
        localStorage.setItem('access_token', response.access_token)
        localStorage.setItem('refresh_token', response.refresh_token)
        set({
          accessToken: response.access_token,
          refreshToken: response.refresh_token,
          isAuthenticated: true,
          isLoading: false,
        })
      } catch (error: any) {
        set({
          error: error.response?.data?.detail || 'Registration failed',
          isLoading: false,
        })
        throw error
      }
    },

    logout: () => {
      localStorage.removeItem('access_token')
      localStorage.removeItem('refresh_token')
      set({
        user: null,
        accessToken: null,
        refreshToken: null,
        isAuthenticated: false,
      })
    },

    loadUser: async () => {
      const token = localStorage.getItem('access_token')
      if (!token) {
        set({ isAuthenticated: false })
        return
      }

      try {
        const user = await authAPI.getMe()
        set({ user, isAuthenticated: true })
      } catch (error) {
        localStorage.removeItem('access_token')
        set({ isAuthenticated: false })
      }
    },

    setError: (error) => set({ error }),
  }))
)
