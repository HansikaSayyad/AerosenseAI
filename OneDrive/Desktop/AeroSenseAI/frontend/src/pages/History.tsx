import { useEffect, useState } from 'react'
import { aqiApi } from '../api/aqi'
import { getAQITheme } from '../utils/aqiColors'
import type { HistoryEntry } from '../types/aqi'

export default function History() {
  const [history, setHistory] = useState<HistoryEntry[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')

  useEffect(() => {
    aqiApi.getHistory()
      .then(setHistory)
      .catch(() => setError('Failed to load history.'))
      .finally(() => setLoading(false))
  }, [])

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-950 via-blue-950 to-slate-900">
      <div className="max-w-3xl mx-auto px-4 py-10">
        <h1 className="text-2xl font-bold text-white mb-1">Search History</h1>
        <p className="text-slate-400 text-sm mb-6">
          Your past AQI searches — saved automatically when logged in.
        </p>

        {loading && (
          <div className="space-y-3 animate-pulse">
            {[1, 2, 3, 4, 5].map(i => (
              <div key={i} className="h-16 rounded-xl bg-white/5" />
            ))}
          </div>
        )}

        {error && (
          <div className="px-4 py-3 rounded-xl bg-red-500/15 border border-red-500/30 text-red-300 text-sm">
            {error}
          </div>
        )}

        {!loading && !error && history.length === 0 && (
          <div className="text-center py-20">
            <div className="text-5xl mb-4">📭</div>
            <p className="text-slate-400">No searches yet.</p>
            <p className="text-slate-500 text-sm mt-1">
              Search for a city on the Dashboard and it will appear here.
            </p>
          </div>
        )}

        {!loading && history.length > 0 && (
          <div className="space-y-3">
            {history.map((entry) => {
              const theme = getAQITheme(entry.aqi_category)
              const date = entry.recorded_at ?? entry.created_at
              return (
                <div
                  key={entry.id}
                  className="flex items-center justify-between bg-white/5 hover:bg-white/8 border border-white/10 rounded-xl px-5 py-4 transition-colors"
                >
                  {/* Left: city + date */}
                  <div>
                    <p className="text-white font-semibold">{entry.city}</p>
                    <p className="text-slate-400 text-xs mt-0.5">
                      {date ? new Date(date).toLocaleString() : '—'}
                    </p>
                  </div>

                  {/* Right: AQI value + category badge */}
                  <div className="flex items-center gap-3">
                    <span className={`text-2xl font-bold ${theme.text}`}>
                      {entry.aqi_value}
                    </span>
                    <span className={`text-xs px-2.5 py-1 rounded-full font-medium ${theme.badge}`}>
                      {theme.emoji} {entry.aqi_category}
                    </span>
                  </div>
                </div>
              )
            })}
          </div>
        )}
      </div>
    </div>
  )
}
