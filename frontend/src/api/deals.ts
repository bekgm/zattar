import apiClient from './client'
import { SafeDeal } from '../types'

export const dealAPI = {
  initiateDeal: async (
    listingId: string,
    sellerId: string,
    amount: number
  ): Promise<SafeDeal> => {
    const response = await apiClient.post('/api/v1/safe-deals', {
      listing_id: listingId,
      seller_id: sellerId,
      amount,
      currency: 'KZT',
    })
    return response.data
  },

  getDeal: async (dealId: string): Promise<SafeDeal> => {
    const response = await apiClient.get(`/api/v1/safe-deals/${dealId}`)
    return response.data
  },

  transitionDeal: async (
    dealId: string,
    status: string,
    metadata?: {
      shipping_number?: string
      dispatch_note?: string
      dispute_reason?: string
    }
  ): Promise<SafeDeal> => {
    const response = await apiClient.post(
      `/api/v1/safe-deals/${dealId}/transition`,
      {
        status,
        ...metadata,
      }
    )
    return response.data
  },

  getBuyerDeals: async (skip?: number, limit?: number): Promise<SafeDeal[]> => {
    const response = await apiClient.get('/api/v1/safe-deals/buyer/deals', {
      params: { skip: skip || 0, limit: limit || 50 },
    })
    return response.data
  },

  getSellerDeals: async (skip?: number, limit?: number): Promise<SafeDeal[]> => {
    const response = await apiClient.get('/api/v1/safe-deals/seller/deals', {
      params: { skip: skip || 0, limit: limit || 50 },
    })
    return response.data
  },
}
