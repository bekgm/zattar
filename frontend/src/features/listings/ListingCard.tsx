import { useState } from 'react'
import { Listing } from '../../types'
import Card from '../../components/common/Card'
import { MapPin, TrendingUp } from 'lucide-react'

export default function ListingCard({ listing }: { listing: Listing }) {
  const [isHovered, setIsHovered] = useState(false)

  return (
    <div 
      onMouseEnter={() => setIsHovered(true)}
      onMouseLeave={() => setIsHovered(false)}
    >
      <Card
        className="overflow-hidden cursor-pointer"
        hoverable
      >
      {/* Image */}
      <div className="relative h-48 bg-neutral-200 rounded-md overflow-hidden mb-3">
        {listing.images.length > 0 ? (
          <img
            src={listing.images[0].image_url}
            alt={listing.title}
            className={`w-full h-full object-cover transition-transform ${isHovered ? 'scale-105' : ''}`}
          />
        ) : (
          <div className="w-full h-full flex items-center justify-center text-neutral-400">
            No image
          </div>
        )}
        {listing.status === 'sold' && (
          <div className="absolute inset-0 bg-black bg-opacity-50 flex items-center justify-center">
            <span className="badge badge-error">Sold</span>
          </div>
        )}
      </div>

      {/* Content */}
      <h3 className="font-semibold text-neutral-900 line-clamp-2 mb-2">
        {listing.title}
      </h3>

      {/* Price */}
      <p className="text-2xl font-bold text-primary mb-3">
        ₸{listing.price.toLocaleString()}
      </p>

      {/* Meta */}
      <div className="flex items-center justify-between text-sm text-neutral-500 mb-3">
        <div className="flex items-center gap-1">
          <MapPin size={16} />
          {listing.city}
        </div>
        <div className="flex items-center gap-1">
          <TrendingUp size={16} />
          {listing.view_count}
        </div>
      </div>

      {/* Condition Badge */}
      <div className="flex gap-2">
        <span className={`badge ${listing.condition === 'new' ? 'badge-success' : ''}`}>
          {listing.condition === 'new' ? 'New' : 'Used'}
        </span>
      </div>
    </Card>
    </div>
  )
}
