import apiClient from './client'
import { Listing } from '../types'

export const listingAPI = {
  createListing: async (data: FormData): Promise<Listing> => {
    const response = await apiClient.post('/api/v1/listings', data, {
      headers: { 'Content-Type': 'multipart/form-data' },
    })
    return response.data
  },

  getListing: async (listingId: string): Promise<Listing> => {
    const response = await apiClient.get(`/api/v1/listings/${listingId}`)
    return response.data
  },

  updateListing: async (
    listingId: string,
    data: Partial<Listing>
  ): Promise<Listing> => {
    const response = await apiClient.patch(`/api/v1/listings/${listingId}`, data)
    return response.data
  },

  deleteListing: async (listingId: string): Promise<void> => {
    await apiClient.delete(`/api/v1/listings/${listingId}`)
  },

  searchListings: async (filters: {
    query?: string
    city?: string
    category_id?: string
    min_price?: number
    max_price?: number
    skip?: number
    limit?: number
  }): Promise<Listing[]> => {
    const response = await apiClient.get('/api/v1/listings', {
      params: filters,
    })
    return response.data
  },

  getUserListings: async (userId: string): Promise<Listing[]> => {
    const response = await apiClient.get(`/api/v1/listings/user/${userId}`)
    return response.data
  },

  markAsSold: async (listingId: string): Promise<Listing> => {
    const response = await apiClient.post(
      `/api/v1/listings/${listingId}/mark-sold`
    )
    return response.data
  },
}
