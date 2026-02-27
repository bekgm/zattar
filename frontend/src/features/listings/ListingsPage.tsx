import { useState } from 'react'
import { useQuery } from '@tanstack/react-query'
import { listingAPI } from '../../api/listings'
import ListingCard from './ListingCard'
import { Search, Filter } from 'lucide-react'
import Input from '../../components/common/Input'
import Button from '../../components/common/Button'

const KAZAKHSTAN_CITIES = [
  'Almaty',
  'Astana',
  'Aktobe',
  'Atyrau',
  'Batys Qazaqstan',
  'Jambyl',
  'Mangystau',
  'Pavlodar',
  'Shyghys Qazaqstan',
  'Solustik Qazaqstan',
  'Nur-Sultan',
]

export default function ListingsPage() {
  const [search, setSearch] = useState('')
  const [city, setCity] = useState<string | undefined>()
  const [priceRange] = useState<[number, number] | undefined>()

  const { data: listings = [], isLoading } = useQuery({
    queryKey: ['listings', { search, city, priceRange }],
    queryFn: () =>
      listingAPI.searchListings({
        query: search || undefined,
        city: city || undefined,
        min_price: priceRange?.[0],
        max_price: priceRange?.[1],
        limit: 50,
      }),
  })

  return (
    <div className="max-w-7xl mx-auto px-4 py-8">
      {/* Search & Filters */}
      <div className="mb-8 space-y-4">
        <div className="flex gap-4">
          <Input
            placeholder="Search listings..."
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            icon={<Search size={20} />}
          />
          <Button variant="secondary">
            <Filter size={20} />
            Filters
          </Button>
        </div>

        {/* City Filter */}
        <div className="flex gap-2 flex-wrap">
          <button
            onClick={() => setCity(undefined)}
            className={`badge ${!city ? 'badge-primary' : 'bg-neutral-100'}`}
          >
            All Cities
          </button>
          {KAZAKHSTAN_CITIES.map((c) => (
            <button
              key={c}
              onClick={() => setCity(c)}
              className={`badge ${city === c ? 'badge-primary' : 'bg-neutral-100'}`}
            >
              {c}
            </button>
          ))}
        </div>
      </div>

      {/* Listings Grid */}
      {isLoading ? (
        <div className="text-center py-12">
          <p className="text-neutral-500">Loading...</p>
        </div>
      ) : listings.length === 0 ? (
        <div className="text-center py-12">
          <p className="text-neutral-500">No listings found</p>
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
          {listings.map((listing) => (
            <ListingCard key={listing.id} listing={listing} />
          ))}
        </div>
      )}
    </div>
  )
}
