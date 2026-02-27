import { ReactNode } from 'react'
import { motion } from 'framer-motion'

interface CardProps {
  children: ReactNode
  className?: string
  onClick?: () => void
  hoverable?: boolean
}

export default function Card({
  children,
  className = '',
  onClick,
  hoverable = false,
}: CardProps) {
  return (
    <motion.div
      className={`bg-white rounded-md shadow-sm p-4 ${hoverable ? 'cursor-pointer' : ''} ${className}`}
      whileHover={hoverable ? { shadow: '0 10px 15px -3px rgba(0, 0, 0, 0.1)' } : {}}
      onClick={onClick}
    >
      {children}
    </motion.div>
  )
}
