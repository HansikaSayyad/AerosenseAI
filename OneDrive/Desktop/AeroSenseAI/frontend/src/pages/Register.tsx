import { useState, type FormEvent } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'

export default function Register() {
  const { register } = useAuth()
  const navigate = useNavigate()

  const [fullName, setFullName] = useState('')
  const [username, setUsername] = useState('')
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [confirm, setConfirm] = useState('')
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault()
    setError('')

    if (password !== confirm) {
      setError('Passwords do not match.')
      return
    }
    if (password.length < 8) {
      setError('Password must be at least 8 characters.')
      return
    }
    if (!/[A-Z]/.test(password)) {
      setError('Password must contain at least one uppercase letter.')
      return
    }
    if (!/[0-9]/.test(password)) {
      setError('Password must contain at least one number.')
      return
    }
    if (username.length < 3 || !/^[a-zA-Z0-9]+$/.test(username)) {
      setError('Username must be 3+ characters, letters and numbers only.')
      return
    }

    setLoading(true)
    try {
      await register({ email, password, full_name: fullName, username })
      navigate('/dashboard')
    } catch (err: unknown) {
      const e = err as { response?: { status?: number; data?: { detail?: unknown } }; message?: string }
      const detail = e?.response?.data?.detail
      let msg = 'Registration failed.'
      if (typeof detail === 'string') {
        msg = detail
      } else if (Array.isArray(detail)) {
        msg = detail.map((d: { msg?: string }) => d.msg ?? JSON.stringify(d)).join(' | ')
      } else if (e?.message) {
        msg = e.message
      }
      msg += ` (HTTP ${e?.response?.status ?? 'no response'})`
      setError(msg)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-950 via-blue-900 to-slate-900 flex items-center justify-center px-4">
      <div className="w-full max-w-md">
        <div className="text-center mb-8">
          <div className="text-5xl mb-3">🌬️</div>
          <h1 className="text-3xl font-bold text-white">AirGuard AI</h1>
          <p className="text-blue-300 mt-1 text-sm">Real-time Air Quality Intelligence</p>
        </div>

        <div className="bg-white/10 backdrop-blur-md border border-white/20 rounded-2xl p-8 shadow-2xl">
          <h2 className="text-xl font-semibold text-white mb-6">Create your account</h2>

          {error && (
            <div className="mb-4 px-4 py-3 rounded-lg bg-red-500/20 border border-red-500/40 text-red-300 text-sm">
              {error}
            </div>
          )}

          <form onSubmit={handleSubmit} className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-blue-200 mb-1">Full Name</label>
              <input
                type="text"
                required
                value={fullName}
                onChange={(e) => setFullName(e.target.value)}
                placeholder="Your Name"
                className="w-full px-4 py-2.5 rounded-lg bg-white/10 border border-white/20 text-white placeholder-white/40 focus:outline-none focus:ring-2 focus:ring-blue-400 transition"
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-blue-200 mb-1">Username</label>
              <input
                type="text"
                required
                value={username}
                onChange={(e) => setUsername(e.target.value)}
                placeholder="e.g. hansika123"
                className="w-full px-4 py-2.5 rounded-lg bg-white/10 border border-white/20 text-white placeholder-white/40 focus:outline-none focus:ring-2 focus:ring-blue-400 transition"
              />
              <p className="text-white/30 text-xs mt-1">Letters and numbers only, min 3 chars</p>
            </div>

            <div>
              <label className="block text-sm font-medium text-blue-200 mb-1">Email</label>
              <input
                type="email"
                required
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                placeholder="you@example.com"
                className="w-full px-4 py-2.5 rounded-lg bg-white/10 border border-white/20 text-white placeholder-white/40 focus:outline-none focus:ring-2 focus:ring-blue-400 transition"
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-blue-200 mb-1">Password</label>
              <input
                type="password"
                required
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                placeholder="Min 8 chars, 1 uppercase, 1 number"
                className="w-full px-4 py-2.5 rounded-lg bg-white/10 border border-white/20 text-white placeholder-white/40 focus:outline-none focus:ring-2 focus:ring-blue-400 transition"
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-blue-200 mb-1">Confirm Password</label>
              <input
                type="password"
                required
                value={confirm}
                onChange={(e) => setConfirm(e.target.value)}
                placeholder="Repeat password"
                className="w-full px-4 py-2.5 rounded-lg bg-white/10 border border-white/20 text-white placeholder-white/40 focus:outline-none focus:ring-2 focus:ring-blue-400 transition"
              />
            </div>

            <button
              type="submit"
              disabled={loading}
              className="w-full py-2.5 rounded-lg bg-blue-500 hover:bg-blue-400 disabled:opacity-60 text-white font-semibold transition-colors mt-2"
            >
              {loading ? 'Creating account…' : 'Create Account'}
            </button>
          </form>

          <p className="mt-6 text-center text-sm text-blue-300">
            Already have an account?{' '}
            <Link to="/login" className="text-blue-400 hover:text-white font-medium transition-colors">
              Sign in
            </Link>
          </p>
        </div>
      </div>
    </div>
  )
}
