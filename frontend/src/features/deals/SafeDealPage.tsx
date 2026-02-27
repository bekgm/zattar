import { useParams } from 'react-router-dom'
import { useState } from 'react'
import { useQuery, useMutation } from '@tanstack/react-query'
import { dealAPI } from '../../api/deals'
import { useAuthStore } from '../../stores/authStore'
import Card from '../../components/common/Card'
import Button from '../../components/common/Button'
import InputField from '../../components/common/Input'
import { Shield, CheckCircle, Truck, AlertCircle } from 'lucide-react'

const STATUS_STEPS = [
  { status: 'pending', label: 'Deal Initiated', icon: Shield },
  { status: 'shipped', label: 'Item Shipped', icon: Truck },
  { status: 'completed', label: 'Delivered', icon: CheckCircle },
]

export default function SafeDealPage() {
  const { dealId } = useParams()
  const { user } = useAuthStore()

  const { data: deal, refetch } = useQuery({
    queryKey: ['deal', dealId],
    queryFn: () => dealAPI.getDeal(dealId!),
    enabled: !!dealId,
  })

  const { mutate: transitionDeal } = useMutation({
    mutationFn: (newStatus: string) =>
      dealAPI.transitionDeal(dealId!, newStatus),
    onSuccess: () => refetch(),
  })

  const [trackingNumber, setTrackingNumber] = useState('')

  if (!deal) return <div>Loading...</div>

  const isBuyer = user?.id === deal.buyer_id
  const isSeller = user?.id === deal.seller_id
  const currentStepIndex = STATUS_STEPS.findIndex((s) => s.status === deal.status)

  return (
    <div className="max-w-4xl mx-auto px-4 py-8">
      <Card className="mb-8">
        <h1 className="text-3xl font-bold mb-6">Safe Deal</h1>

        {/* Status Timeline */}
        <div className="mb-8">
          <div className="flex justify-between items-center">
            {STATUS_STEPS.map((step, idx) => {
              const Icon = step.icon
              const isCompleted = idx <= currentStepIndex

              return (
                <div key={step.status} className="flex-1 flex flex-col items-center">
                  <div
                    className={`w-12 h-12 rounded-full flex items-center justify-center mb-2 ${
                      isCompleted ? 'bg-success text-white' : 'bg-neutral-200 text-neutral-500'
                    }`}
                  >
                    <Icon size={24} />
                  </div>
                  <p className="text-sm font-medium text-center">{step.label}</p>
                  {idx < STATUS_STEPS.length - 1 && (
                    <div
                      className={`flex-1 w-1 mt-2 ${
                        idx <= currentStepIndex - 1 ? 'bg-success' : 'bg-neutral-200'
                      }`}
                    ></div>
                  )}
                </div>
              )
            })}
          </div>
        </div>

        {/* Deal Details */}
        <div className="grid grid-cols-2 gap-4 mb-8">
          <div>
            <p className="text-neutral-500 text-sm">Amount</p>
            <p className="text-2xl font-bold text-primary">
              ₸{deal.amount.toLocaleString()}
            </p>
          </div>
          <div>
            <p className="text-neutral-500 text-sm">Status</p>
            <p className="text-lg font-bold capitalize">{deal.status}</p>
          </div>
          {deal.shipping_number && (
            <div>
              <p className="text-neutral-500 text-sm">Tracking Number</p>
              <p className="font-mono">{deal.shipping_number}</p>
            </div>
          )}
          {deal.expires_at && (
            <div>
              <p className="text-neutral-500 text-sm">Expires</p>
              <p>{new Date(deal.expires_at).toLocaleDateString()}</p>
            </div>
          )}
        </div>

        {/* Actions */}
        <div className="space-y-3">
          {isSeller && deal.status === 'pending' && (
            <>
              <InputField
                label="Tracking Number"
                placeholder="Enter tracking number..."
                value={trackingNumber}
                onChange={(e: React.ChangeEvent<HTMLInputElement>) => setTrackingNumber(e.target.value)}
              />
              <Button
                className="w-full"
                onClick={() => transitionDeal('shipped')}
              >
                Mark as Shipped
              </Button>
            </>
          )}

          {isBuyer && deal.status === 'shipped' && (
            <Button
              className="w-full"
              onClick={() => transitionDeal('completed')}
            >
              Confirm Delivery
            </Button>
          )}

          {(isBuyer || isSeller) && deal.status !== 'completed' && deal.status !== 'disputed' && (
            <Button
              className="w-full"
              variant="secondary"
              onClick={() => transitionDeal('disputed')}
            >
              <AlertCircle size={20} />
              Report Issue
            </Button>
          )}
        </div>
      </Card>

      {deal.status === 'completed' && (
        <Card className="bg-success bg-opacity-10 border border-success text-success flex items-center gap-3">
          <CheckCircle size={24} />
          <div>
            <p className="font-semibold">Deal Completed</p>
            <p className="text-sm">
              The funds have been released. Thank you for using Zattar Safe Deal!
            </p>
          </div>
        </Card>
      )}
    </div>
  )
}
