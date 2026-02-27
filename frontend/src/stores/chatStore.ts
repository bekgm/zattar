import { create } from 'zustand'
import { devtools } from 'zustand/middleware'
import { Conversation, Message } from '../types'

interface ChatState {
  conversations: Conversation[]
  currentConversation: Conversation | null
  messages: Message[]
  isLoading: boolean
  error: string | null

  // Actions
  setConversations: (conversations: Conversation[]) => void
  setCurrentConversation: (conversation: Conversation) => void
  addMessage: (message: Message) => void
  setMessages: (messages: Message[]) => void
  clearError: () => void
}

export const useChatStore = create<ChatState>()(
  devtools((set) => ({
    conversations: [],
    currentConversation: null,
    messages: [],
    isLoading: false,
    error: null,

    setConversations: (conversations) => set({ conversations }),
    setCurrentConversation: (conversation) => set({ currentConversation: conversation }),
    addMessage: (message) =>
      set((state) => ({
        messages: [...state.messages, message],
      })),
    setMessages: (messages) => set({ messages }),
    clearError: () => set({ error: null }),
  }))
)
