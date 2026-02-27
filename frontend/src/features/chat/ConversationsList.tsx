import { useQuery } from '@tanstack/react-query'
import { chatAPI } from '../../api/chat'
import { useAuthStore } from '../../stores/authStore'
import Card from '../../components/common/Card'
import { Link } from 'react-router-dom'

export default function ConversationsList() {
  const { user } = useAuthStore()

  const { data: conversations = [], isLoading } = useQuery({
    queryKey: ['conversations', user?.id],
    queryFn: () => chatAPI.getConversations(0, 50),
    enabled: !!user,
  })

  if (isLoading) return <div>Loading conversations...</div>

  return (
    <div className="max-w-4xl mx-auto px-4 py-8">
      <h1 className="text-3xl font-bold mb-6">Messages</h1>

      <div className="space-y-3">
        {conversations.length === 0 ? (
          <Card>
            <p className="text-neutral-500 text-center py-8">
              No conversations yet
            </p>
          </Card>
        ) : (
          conversations.map((conv) => (
            <Link
              key={conv.id}
              to={`/chat/${conv.id}`}
              className="block"
            >
              <Card hoverable>
                <div className="flex justify-between items-start">
                  <div className="flex-1">
                    <h3 className="font-semibold">
                      {/* Show seller or buyer name depending on user role */}
                      {conv.buyer_id === user?.id
                        ? `Seller - ${conv.listing_id}`
                        : `Buyer - ${conv.listing_id}`}
                    </h3>
                    <p className="text-sm text-neutral-500">
                      {new Date(conv.last_message_at).toLocaleDateString()}
                    </p>
                  </div>
                </div>
              </Card>
            </Link>
          ))
        )}
      </div>
    </div>
  )
}
