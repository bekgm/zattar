import apiClient from './client'
import { Conversation, Message } from '../types'

export const chatAPI = {
  startConversation: async (
    listingId: string,
    sellerId: string
  ): Promise<Conversation> => {
    const response = await apiClient.post(
      `/api/v1/chat/conversations/${listingId}/${sellerId}`
    )
    return response.data
  },

  getConversations: async (skip?: number, limit?: number): Promise<Conversation[]> => {
    const response = await apiClient.get('/api/v1/chat/conversations', {
      params: { skip: skip || 0, limit: limit || 50 },
    })
    return response.data
  },

  getConversation: async (conversationId: string): Promise<Conversation> => {
    const response = await apiClient.get(
      `/api/v1/chat/conversations/${conversationId}`
    )
    return response.data
  },

  sendMessage: async (
    conversationId: string,
    content: string
  ): Promise<Message> => {
    const response = await apiClient.post(
      `/api/v1/chat/conversations/${conversationId}/messages`,
      { content }
    )
    return response.data
  },

  getMessages: async (
    conversationId: string,
    skip?: number,
    limit?: number
  ): Promise<Message[]> => {
    const response = await apiClient.get(
      `/api/v1/chat/conversations/${conversationId}/messages`,
      {
        params: { skip: skip || 0, limit: limit || 50 },
      }
    )
    return response.data
  },

  markAsRead: async (conversationId: string): Promise<void> => {
    await apiClient.post(`/api/v1/chat/conversations/${conversationId}/mark-read`)
  },
}
