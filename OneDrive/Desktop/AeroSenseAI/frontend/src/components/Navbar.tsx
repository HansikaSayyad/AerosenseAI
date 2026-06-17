import { NavLink, useNavigate } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'

export default function Navbar() {
  const { user, isAuthenticated, logout } = useAuth()
  const navigate = useNavigate()

  const handleLogout = () => {
    logout()
    navigate('/login')
  }

  const linkClass = ({ isActive }: { isActive: boolean }) =>
    `text-sm transition-colors ${isActive ? 'text-white font-semibold' : 'text-slate-400 hover:text-white'}`

  return (
    <nav className="bg-slate-900/80 backdrop-blur border-b border-white/10 sticky top-0 z-50">
      <div className="max-w-5xl mx-auto px-4 h-14 flex items-center justify-between">
        {/* Logo */}
        <NavLink to="/dashboard" className="flex items-center gap-2 text-white font-bold text-lg">
          <span>🌬️</span>
          <span>AirGuard AI</span>
        </NavLink>

        {/* Nav links — only when logged in */}
        {isAuthenticated && (
          <div className="hidden sm:flex items-center gap-6">
            <NavLink to="/dashboard" className={linkClass}>Dashboard</NavLink>
            <NavLink to="/history"   className={linkClass}>History</NavLink>
            <NavLink to="/profile"   className={linkClass}>Profile</NavLink>
          </div>
        )}

        {/* Auth controls */}
        <div className="flex items-center gap-3">
          {isAuthenticated ? (
            <>
              <span className="text-slate-400 text-sm hidden sm:block">
                {user?.full_name}
              </span>
              <button
                onClick={handleLogout}
                className="text-sm text-slate-300 hover:text-white border border-white/20 hover:border-white/40 px-3 py-1.5 rounded-lg transition-colors"
              >
                Sign Out
              </button>
            </>
          ) : (
            <>
              <NavLink to="/login"    className="text-sm text-slate-300 hover:text-white transition-colors">Sign In</NavLink>
              <NavLink to="/register" className="text-sm bg-blue-500 hover:bg-blue-400 text-white px-3 py-1.5 rounded-lg transition-colors">Register</NavLink>
            </>
          )}
        </div>
      </div>
    </nav>
  )
}
