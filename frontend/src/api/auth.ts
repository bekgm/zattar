import apiClient from './client'
import { AuthResponse, User, UserProfile } from '../types'

export const authAPI = {
  register: async (data: {
    email: string
    phone: string
    username: string
    password: string
  }): Promise<AuthResponse> => {
    const response = await apiClient.post('/api/v1/users/register', data)
    return response.data
  },

  login: async (data: {
    email: string
    password: string
  }): Promise<AuthResponse> => {
    const response = await apiClient.post('/api/v1/users/login', data)
    return response.data
  },

  getMe: async (): Promise<UserProfile> => {
    const response = await apiClient.get('/api/v1/users/me')
    return response.data
  },

  getUser: async (userId: string): Promise<User> => {
    const response = await apiClient.get(`/api/v1/users/${userId}`)
    return response.data
  },

  updateProfile: async (data: Partial<UserProfile>): Promise<UserProfile> => {
    const response = await apiClient.patch('/api/v1/users/me/profile', data)
    return response.data
  },
}
