/* Types and Interfaces */

export interface User {
  id: string
  email: string
  username: string
  first_name?: string
  last_name?: string
  avatar_url?: string
  city?: string
  rating: number
  total_reviews: number
  is_verified: boolean
  created_at: string
}

export interface UserProfile extends User {
  phone: string
  bio?: string
  is_active: boolean
  updated_at: string
  last_login?: string
}

export interface Listing {
  id: string
  title: string
  description: string
  price: number
  city: string
  category_id: string
  condition: 'new' | 'used'
  status: 'active' | 'sold' | 'archived'
  view_count: number
  created_at: string
  updated_at: string
  seller: User
  images: ListingImage[]
}

export interface ListingImage {
  id: string
  image_url: string
  order: number
}

export interface Conversation {
  id: string
  listing_id: string
  buyer_id: string
  seller_id: string
  last_message_at: string
  created_at: string
  messages?: Message[]
}

export interface Message {
  id: string
  conversation_id: string
  sender_id: string
  content: string
  is_read: boolean
  created_at: string
}

export interface SafeDeal {
  id: string
  listing_id: string
  buyer_id: string
  seller_id: string
  amount: number
  currency: string
  status: 'pending' | 'shipped' | 'completed' | 'disputed' | 'cancelled'
  shipping_number?: string
  dispatch_note?: string
  dispute_reason?: string
  created_at: string
  shipped_at?: string
  completed_at?: string
  expires_at?: string
  disputed_at?: string
}

export interface Category {
  id: string
  name: string
  slug: string
  description?: string
  icon_url?: string
}

export interface AuthResponse {
  access_token: string
  refresh_token: string
  token_type: string
  expires_in: number
}
