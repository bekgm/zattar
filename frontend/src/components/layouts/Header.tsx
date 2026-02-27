import { Link } from 'react-router-dom'
import { useAuthStore } from '../../stores/authStore'
import { useUIStore } from '../../stores/uiStore'
import { Menu, LogOut, User } from 'lucide-react'

export default function Header() {
  const { user, logout, isAuthenticated } = useAuthStore()
  const { toggleSidebar } = useUIStore()

  return (
    <header className="sticky top-0 z-50 bg-white shadow-sm">
      <div className="max-w-7xl mx-auto px-4 py-4 flex items-center justify-between">
        {/* Logo */}
        <Link to="/" className="text-2xl font-bold text-primary">
          ZATTAR
        </Link>

        {/* Right side */}
        <div className="flex items-center gap-4">
          {isAuthenticated && user ? (
            <>
              <Link
                to="/chat"
                className="text-neutral-600 hover:text-primary transition-colors"
              >
                Messages
              </Link>
              <Link
                to={`/profile/${user.id}`}
                className="flex items-center gap-2 text-neutral-600 hover:text-primary transition-colors"
              >
                <User size={20} />
                {user.first_name || user.username}
              </Link>
              <button
                onClick={logout}
                className="text-neutral-600 hover:text-error transition-colors"
              >
                <LogOut size={20} />
              </button>
            </>
          ) : (
            <>
              <Link to="/login" className="text-primary hover:text-primary-dark">
                Login
              </Link>
              <Link
                to="/register"
                className="btn-primary"
              >
                Register
              </Link>
            </>
          )}
          <button
            onClick={toggleSidebar}
            className="md:hidden text-neutral-600"
          >
            <Menu size={24} />
          </button>
        </div>
      </div>
    </header>
  )
}
