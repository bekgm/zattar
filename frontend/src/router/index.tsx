import { Routes, Route } from 'react-router-dom'
import MainLayout from '../components/layouts/MainLayout'
import ListingsPage from '../features/listings/ListingsPage'
import ListingDetailPage from '../features/listings/ListingDetailPage'
import ConversationsList from '../features/chat/ConversationsList'
import ChatWindow from '../features/chat/ChatWindow'
import SafeDealPage from '../features/deals/SafeDealPage'

export default function AppRouter() {
  return (
    <MainLayout>
      <Routes>
        {/* Listings */}
        <Route path="/" element={<ListingsPage />} />
        <Route path="/listings/:listingId" element={<ListingDetailPage />} />

        {/* Chat */}
        <Route path="/chat" element={<ConversationsList />} />
        <Route path="/chat/:conversationId" element={<ChatWindow />} />

        {/* Safe Deals */}
        <Route path="/deals/:dealId" element={<SafeDealPage />} />

        {/* 404 */}
        <Route path="*" element={<div>Page not found</div>} />
      </Routes>
    </MainLayout>
  )
}
