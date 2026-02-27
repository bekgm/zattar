import { Routes, Route } from 'react-router-dom'
import MainLayout from '../components/layouts/MainLayout'
import ListingsPage from '../features/listings/ListingsPage'
import ListingDetailPage from '../features/listings/ListingDetailPage'
import ConversationsList from '../features/chat/ConversationsList'
import ChatWindow from '../features/chat/ChatWindow'
import SafeDealPage from '../features/deals/SafeDealPage'
import RegisterPage from '../features/auth/RegisterPage'
import LoginPage from '../features/auth/LoginPage'
import VerifyEmailPage from '../features/auth/VerifyEmailPage'

export default function AppRouter() {
  return (
    <Routes>
      {/* Auth Routes (without layout) */}
      <Route path="/register" element={<RegisterPage />} />
      <Route path="/login" element={<LoginPage />} />
      <Route path="/verify-email" element={<VerifyEmailPage />} />

      {/* App Routes (with layout) */}
      <Route element={<MainLayout />}>
        {/* Listings */}
        <Route path="/" element={<ListingsPage />} />
        <Route path="/listings/:listingId" element={<ListingDetailPage />} />

        {/* Chat */}
        <Route path="/chat" element={<ConversationsList />} />
        <Route path="/chat/:conversationId" element={<ChatWindow />} />

        {/* Safe Deals */}
        <Route path="/deals/:dealId" element={<SafeDealPage />} />
      </Route>

      {/* 404 */}
      <Route path="*" element={<div>Page not found</div>} />
    </Routes>
  )
}
