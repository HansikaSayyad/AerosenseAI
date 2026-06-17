import { useAuth } from '../context/AuthContext'
import { useNavigate } from 'react-router-dom'

const ROLE_BADGE: Record<string, string> = {
  admin:   'bg-purple-500/20 text-purple-300 border border-purple-500/40',
  premium: 'bg-yellow-500/20 text-yellow-300 border border-yellow-500/40',
  user:    'bg-blue-500/20 text-blue-300 border border-blue-500/40',
}

export default function Profile() {
  const { user, logout } = useAuth()
  const navigate = useNavigate()

  if (!user) return null

  const handleLogout = () => {
    logout()
    navigate('/login')
  }

  const joined = user.created_at
    ? new Date(user.created_at).toLocaleDateString('en-IN', {
        year: 'numeric', month: 'long', day: 'numeric',
      })
    : '—'

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-950 via-blue-950 to-slate-900">
      <div className="max-w-xl mx-auto px-4 py-10">
        <h1 className="text-2xl font-bold text-white mb-6">My Profile</h1>

        {/* Avatar card */}
        <div className="bg-white/5 border border-white/10 rounded-2xl p-6 mb-4 flex items-center gap-5">
          <div className="w-16 h-16 rounded-full bg-blue-500/30 border-2 border-blue-400/40 flex items-center justify-center text-2xl font-bold text-blue-300 shrink-0">
            {user.full_name?.charAt(0).toUpperCase() ?? '?'}
          </div>
          <div>
            <p className="text-white text-lg font-semibold">{user.full_name}</p>
            <p className="text-slate-400 text-sm">@{user.username}</p>
            <span className={`inline-block mt-1.5 text-xs px-2.5 py-0.5 rounded-full font-medium ${ROLE_BADGE[user.role] ?? ROLE_BADGE.user}`}>
              {user.role.charAt(0).toUpperCase() + user.role.slice(1)}
            </span>
          </div>
        </div>

        {/* Details */}
        <div className="bg-white/5 border border-white/10 rounded-2xl divide-y divide-white/5">
          <Row label="Email" value={user.email} />
          <Row label="Username" value={`@${user.username}`} />
          <Row label="Account Status" value={user.is_active ? '✅ Active' : '❌ Inactive'} />
          <Row label="Joined" value={joined} />
        </div>

        {/* Actions */}
        <div className="mt-6">
          <button
            onClick={handleLogout}
            className="w-full py-2.5 rounded-xl bg-red-500/20 hover:bg-red-500/30 border border-red-500/40 text-red-300 font-semibold transition-colors"
          >
            Sign Out
          </button>
        </div>
      </div>
    </div>
  )
}

function Row({ label, value }: { label: string; value: string }) {
  return (
    <div className="flex items-center justify-between px-5 py-3.5">
      <span className="text-slate-400 text-sm">{label}</span>
      <span className="text-white text-sm font-medium">{value}</span>
    </div>
  )
}
