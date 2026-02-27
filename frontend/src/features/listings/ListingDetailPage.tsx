import { useState } from 'react'
import { useParams } from 'react-router-dom'
import { useQuery, useMutation } from '@tanstack/react-query'
import { chatAPI } from '../../api/chat'
import { dealAPI } from '../../api/deals'
import { listingAPI } from '../../api/listings'
import { useAuthStore } from '../../stores/authStore'
import Card from '../../components/common/Card'
import Button from '../../components/common/Button'
import { Star, MapPin, Shield } from 'lucide-react'

export default function ListingDetailPage() {
  const { listingId } = useParams()
  const { user } = useAuthStore()
  const [activeImageIndex, setActiveImageIndex] = useState(0)

  const { data: listing, isLoading } = useQuery({
    queryKey: ['listing', listingId],
    queryFn: () => listingAPI.getListing(listingId!),
    enabled: !!listingId,
  })

  const { mutate: startConversation } = useMutation({
    mutationFn: () =>
      chatAPI.startConversation(listingId!, listing!.seller.id),
    onSuccess: (conversation) => {
      window.location.href = `/chat/${conversation.id}`
    },
  })

  const { mutate: initiateDeal } = useMutation({
    mutationFn: () =>
      dealAPI.initiateDeal(listingId!, listing!.seller.id, listing!.price),
    onSuccess: (deal) => {
      window.location.href = `/deals/${deal.id}`
    },
  })

  if (isLoading) return <div>Loading...</div>
  if (!listing) return <div>Listing not found</div>

  const isSeller = user?.id === listing.seller.id

  return (
    <div className="max-w-6xl mx-auto px-4 py-8">
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        {/* Images */}
        <div className="lg:col-span-2">
          <Card className="p-0 overflow-hidden">
            <div className="relative h-96">
              {listing.images.length > 0 ? (
                <img
                  src={listing.images[activeImageIndex].image_url}
                  alt={listing.title}
                  className="w-full h-full object-cover"
                />
              ) : (
                <div className="w-full h-full bg-neutral-200 flex items-center justify-center">
                  No image
                </div>
              )}
            </div>

            {/* Thumbnails */}
            {listing.images.length > 1 && (
              <div className="flex gap-2 p-4 overflow-x-auto">
                {listing.images.map((img, idx) => (
                  <button
                    key={img.id}
                    onClick={() => setActiveImageIndex(idx)}
                    className={`flex-shrink-0 h-20 w-20 rounded-md overflow-hidden border-2 ${
                      idx === activeImageIndex ? 'border-primary' : 'border-neutral-200'
                    }`}
                  >
                    <img
                      src={img.image_url}
                      alt={`View ${idx + 1}`}
                      className="w-full h-full object-cover"
                    />
                  </button>
                ))}
              </div>
            )}
          </Card>

          {/* Description */}
          <Card className="mt-6">
            <h2 className="text-2xl font-bold mb-4">{listing.title}</h2>
            <p className="text-neutral-600 whitespace-pre-wrap">
              {listing.description}
            </p>
          </Card>
        </div>

        {/* Sidebar */}
        <div className="space-y-4">
          {/* Price & Status */}
          <Card>
            <p className="text-4xl font-bold text-primary mb-4">
              ₸{listing.price.toLocaleString()}
            </p>
            <div className="flex gap-2 mb-4">
              <span
                className={`badge ${listing.condition === 'new' ? 'badge-success' : ''}`}
              >
                {listing.condition === 'new' ? 'New' : 'Used'}
              </span>
              <span
                className={`badge ${listing.status === 'active' ? 'badge-primary' : 'badge-error'}`}
              >
                {listing.status}
              </span>
            </div>
          </Card>

          {/* Location */}
          <Card>
            <div className="flex items-center gap-2 mb-4">
              <MapPin size={20} className="text-primary" />
              <div>
                <p className="font-semibold">{listing.city}</p>
                <p className="text-sm text-neutral-500">Posted {listing.created_at}</p>
              </div>
            </div>
          </Card>

          {/* Seller Info */}
          <Card>
            <h3 className="font-semibold mb-3">Seller</h3>
            <div className="flex items-center gap-3 mb-4">
              {listing.seller.avatar_url && (
                <img
                  src={listing.seller.avatar_url}
                  alt={listing.seller.username}
                  className="w-12 h-12 rounded-full"
                />
              )}
              <div>
                <p className="font-semibold">{listing.seller.username}</p>
                <div className="flex items-center gap-1">
                  <Star size={16} className="text-yellow-500" />
                  <span className="text-sm">{listing.seller.rating.toFixed(1)}</span>
                </div>
              </div>
            </div>
          </Card>

          {/* Actions */}
          {!isSeller && listing.status === 'active' && (
            <Card className="space-y-3">
              <Button
                className="w-full"
                onClick={() => startConversation()}
              >
                Contact Seller
              </Button>
              <Button
                variant="secondary"
                className="w-full"
                onClick={() => initiateDeal()}
              >
                <Shield size={20} />
                Safe Deal
              </Button>
            </Card>
          )}

          {isSeller && (
            <Card className="space-y-3">
              <Button className="w-full" variant="secondary">
                Edit Listing
              </Button>
              <Button className="w-full" variant="secondary">
                Mark as Sold
              </Button>
            </Card>
          )}
        </div>
      </div>
    </div>
  )
}
