import { motion } from 'framer-motion'

export default function SplashScreen() {
  return (
    <div className="fixed inset-0 bg-primary flex flex-col items-center justify-center">
      {/* Background Gradient */}
      <div className="absolute inset-0 bg-gradient-to-br from-primary to-primary-dark"></div>

      {/* Content */}
      <motion.div
        className="relative z-10 flex flex-col items-center"
        initial={{ opacity: 0, scale: 0.8 }}
        animate={{ opacity: 1, scale: 1 }}
        exit={{ opacity: 0 }}
        transition={{ duration: 0.6, ease: 'easeOut' }}
      >
        {/* Logo */}
        <motion.div
          className="mb-8"
          animate={{ scale: [1, 1.05, 1] }}
          transition={{ duration: 2, repeat: Infinity }}
        >
          <h1 className="text-6xl font-bold text-white text-center">ZATTAR</h1>
          <p className="text-white text-center mt-2 text-lg">Marketplace</p>
        </motion.div>

        {/* Loading Bar */}
        <motion.div
          className="w-64 h-1 bg-white bg-opacity-20 rounded-full overflow-hidden"
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.3 }}
        >
          <motion.div
            className="h-full bg-white rounded-full"
            initial={{ width: '0%' }}
            animate={{ width: '100%' }}
            transition={{ duration: 1.5, ease: 'easeInOut' }}
          ></motion.div>
        </motion.div>

        {/* Tagline */}
        <motion.p
          className="text-white text-sm mt-6 text-center opacity-80"
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 0.5 }}
        >
          The trusted marketplace for Kazakhstan
        </motion.p>
      </motion.div>

      {/* Decorative Elements */}
      <motion.div
        className="absolute bottom-10 left-10 w-32 h-32 bg-white opacity-5 rounded-full blur-3xl"
        animate={{
          x: [0, 20, 0],
          y: [0, -20, 0],
        }}
        transition={{ duration: 6, repeat: Infinity }}
      ></motion.div>

      <motion.div
        className="absolute top-20 right-10 w-40 h-40 bg-white opacity-5 rounded-full blur-3xl"
        animate={{
          x: [0, -20, 0],
          y: [0, 20, 0],
        }}
        transition={{ duration: 8, repeat: Infinity }}
      ></motion.div>
    </div>
  )
}
