import { InputHTMLAttributes } from 'react'
import { motion } from 'framer-motion'

interface InputProps extends InputHTMLAttributes<HTMLInputElement> {
  label?: string
  error?: string
  icon?: React.ReactNode
}

export default function Input({
  label,
  error,
  icon,
  ...props
}: InputProps) {
  return (
    <motion.div className="w-full">
      {label && (
        <label className="block text-sm font-medium text-neutral-700 mb-2">
          {label}
        </label>
      )}
      <div className="relative">
        <input
          className={`input-base ${error ? 'border-error focus:ring-error' : ''} ${icon ? 'pl-10' : ''}`}
          {...props}
        />
        {icon && <div className="absolute left-3 top-1/2 transform -translate-y-1/2">{icon}</div>}
      </div>
      {error && <p className="text-error text-xs mt-1">{error}</p>}
    </motion.div>
  )
}
