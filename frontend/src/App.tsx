import { useEffect, useState } from 'react'
import { BrowserRouter } from 'react-router-dom'
import { QueryClientProvider, QueryClient } from '@tanstack/react-query'
import AppRouter from './router'
import SplashScreen from './components/common/SplashScreen.tsx'
import './App.css'

const queryClient = new QueryClient()

function App() {
  const [showSplash, setShowSplash] = useState(true)

  useEffect(() => {
    // Check if splash screen has been shown before
    const splashShown = localStorage.getItem('zattar_splash_shown')

    if (splashShown) {
      setShowSplash(false)
    } else {
      // Show splash for 2 seconds
      const timer = setTimeout(() => {
        setShowSplash(false)
        localStorage.setItem('zattar_splash_shown', 'true')
      }, 2000)

      return () => clearTimeout(timer)
    }
  }, [])

  if (showSplash) {
    return <SplashScreen />
  }

  return (
    <QueryClientProvider client={queryClient}>
      <BrowserRouter>
        <AppRouter />
      </BrowserRouter>
    </QueryClientProvider>
  )
}

export default App
