import { motion } from 'framer-motion'
import { ReactNode } from 'react'

interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: 'primary' | 'secondary' | 'ghost'
  size?: 'sm' | 'md' | 'lg'
  isLoading?: boolean
  children: ReactNode
}

export default function Button({
  variant = 'primary',
  size = 'md',
  isLoading = false,
  disabled,
  children,
  ...props
}: ButtonProps) {
  const baseStyles =
    'font-medium rounded-base transition-colors flex items-center justify-center gap-2'

  const variants = {
    primary: 'bg-primary text-white hover:bg-primary-dark disabled:bg-neutral-300',
    secondary: 'border border-neutral-300 text-neutral-900 hover:bg-neutral-50 disabled:bg-neutral-100',
    ghost: 'text-primary hover:bg-primary hover:bg-opacity-5 disabled:text-neutral-400',
  }

  const sizes = {
    sm: 'px-3 py-1.5 text-sm',
    md: 'px-4 py-2 text-base',
    lg: 'px-6 py-3 text-lg',
  }

  return (
    <motion.button
      className={`${baseStyles} ${variants[variant]} ${sizes[size]}`}
      disabled={disabled || isLoading}
      whileHover={{ scale: disabled ? 1 : 1.02 }}
      whileTap={{ scale: disabled ? 1 : 0.98 }}
      {...(props as any)}
    >
      {isLoading && (
        <motion.div
          className="w-4 h-4 border-2 border-current border-t-transparent rounded-full"
          animate={{ rotate: 360 }}
          transition={{ duration: 1, repeat: Infinity }}
        />
      )}
      {children}
    </motion.button>
  )
}
