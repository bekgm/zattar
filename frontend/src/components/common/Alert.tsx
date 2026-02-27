import { motion } from 'framer-motion'
import { AlertCircle, CheckCircle, XCircle, Info } from 'lucide-react'

interface AlertProps {
  type?: 'success' | 'error' | 'warning' | 'info'
  title?: string
  message: string
  onClose?: () => void
}

export default function Alert({
  type = 'info',
  title,
  message,
  onClose,
}: AlertProps) {
  const colors = {
    success: 'bg-success bg-opacity-10 border-success text-success',
    error: 'bg-error bg-opacity-10 border-error text-error',
    warning: 'bg-warning bg-opacity-10 border-warning text-warning',
    info: 'bg-info bg-opacity-10 border-info text-info',
  }

  const icons = {
    success: <CheckCircle size={20} />,
    error: <XCircle size={20} />,
    warning: <AlertCircle size={20} />,
    info: <Info size={20} />,
  }

  return (
    <motion.div
      initial={{ opacity: 0, y: -10 }}
      animate={{ opacity: 1, y: 0 }}
      exit={{ opacity: 0, y: -10 }}
      className={`border border-current rounded-md p-4 flex items-start gap-3 ${colors[type]}`}
    >
      <div className="flex-shrink-0 mt-0.5">{icons[type]}</div>
      <div className="flex-1">
        {title && <h3 className="font-semibold">{title}</h3>}
        <p className="text-sm">{message}</p>
      </div>
      {onClose && (
        <button
          onClick={onClose}
          className="text-current opacity-60 hover:opacity-100 transition-opacity"
        >
          ×
        </button>
      )}
    </motion.div>
  )
}
