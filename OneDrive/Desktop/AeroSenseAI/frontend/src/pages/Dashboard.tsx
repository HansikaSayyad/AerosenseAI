import { useState, type FormEvent } from 'react'
import { aqiApi } from '../api/aqi'
import type { AQIResponse } from '../types/aqi'
import AQICard from '../components/AQICard'
import PollutantsChart from '../components/PollutantsChart'
import RecommendationsCard from '../components/RecommendationsCard'

type SearchState = 'idle' | 'loading' | 'done' | 'error'

export default function Dashboard() {
  const [city, setCity] = useState('')
  const [data, setData] = useState<AQIResponse | null>(null)
  const [state, setState] = useState<SearchState>('idle')
  const [errorMsg, setErrorMsg] = useState('')
  const [gpsLoading, setGpsLoading] = useState(false)

  const fetchByCity = async (e: FormEvent) => {
    e.preventDefault()
    if (!city.trim()) return
    setState('loading')
    setErrorMsg('')
    try {
      const res = await aqiApi.getByCity(city.trim())
      if (res.success === false) {
        setErrorMsg(res.error ?? 'City not found. Try another name.')
        setState('error')
      } else {
        setData(res)
        setState('done')
      }
    } catch {
      setErrorMsg('Failed to reach the server. Is the backend running?')
      setState('error')
    }
  }

  const fetchByGPS = () => {
    if (!navigator.geolocation) {
      setErrorMsg('Geolocation is not supported by your browser.')
      setState('error')
      return
    }
    setGpsLoading(true)
    setErrorMsg('')
    navigator.geolocation.getCurrentPosition(
      async (pos) => {
        setState('loading')
        try {
          const res = await aqiApi.getByGPS({
            latitude: pos.coords.latitude,
            longitude: pos.coords.longitude,
          })
          if (res.success === false) {
            setErrorMsg(res.error ?? 'Could not get AQI for your location.')
            setState('error')
          } else {
            setData(res)
            setState('done')
          }
        } catch {
          setErrorMsg('Failed to reach the server.')
          setState('error')
        } finally {
          setGpsLoading(false)
        }
      },
      () => {
        setErrorMsg('Location permission denied. Please allow location access.')
        setState('error')
        setGpsLoading(false)
      }
    )
  }

  const hasData = state === 'done' && data

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-950 via-blue-950 to-slate-900">
      <div className="max-w-3xl mx-auto px-4 py-10">
        {/* Search section */}
        <div className="mb-8">
          <h1 className="text-2xl font-bold text-white mb-1">Air Quality Dashboard</h1>
          <p className="text-slate-400 text-sm mb-5">
            Search any city or use your GPS location for real-time AQI data.
          </p>

          <form onSubmit={fetchByCity} className="flex gap-2">
            <input
              type="text"
              value={city}
              onChange={(e) => setCity(e.target.value)}
              placeholder="Enter city name (e.g. Hyderabad, Delhi, Mumbai)"
              className="flex-1 px-4 py-2.5 rounded-xl bg-white/10 border border-white/20 text-white placeholder-white/30 focus:outline-none focus:ring-2 focus:ring-blue-400 transition"
            />
            <button
              type="submit"
              disabled={state === 'loading'}
              className="px-5 py-2.5 rounded-xl bg-blue-500 hover:bg-blue-400 disabled:opacity-60 text-white font-semibold transition-colors whitespace-nowrap"
            >
              {state === 'loading' ? '…' : 'Search'}
            </button>
            <button
              type="button"
              onClick={fetchByGPS}
              disabled={gpsLoading || state === 'loading'}
              title="Use my location"
              className="px-4 py-2.5 rounded-xl bg-white/10 hover:bg-white/20 disabled:opacity-60 text-white border border-white/20 transition-colors"
            >
              {gpsLoading ? '…' : '📍'}
            </button>
          </form>
        </div>

        {/* Error */}
        {state === 'error' && (
          <div className="mb-6 px-4 py-3 rounded-xl bg-red-500/15 border border-red-500/30 text-red-300 text-sm">
            {errorMsg}
          </div>
        )}

        {/* Loading skeleton */}
        {state === 'loading' && (
          <div className="space-y-4 animate-pulse">
            <div className="h-48 rounded-2xl bg-white/5" />
            <div className="h-56 rounded-2xl bg-white/5" />
            <div className="h-64 rounded-2xl bg-white/5" />
          </div>
        )}

        {/* Results */}
        {hasData && (
          <div className="space-y-4">
            <AQICard data={data} />
            {data.pollutants && Object.keys(data.pollutants).length > 0 && (
              <PollutantsChart pollutants={data.pollutants} />
            )}
            {data.recommendations && (
              <RecommendationsCard
                recommendations={data.recommendations}
                category={data.aqi_category ?? ''}
              />
            )}
          </div>
        )}

        {/* Empty state */}
        {state === 'idle' && (
          <div className="text-center py-20">
            <div className="text-6xl mb-4">🌍</div>
            <p className="text-slate-400">Search a city above to get started</p>
            <p className="text-slate-500 text-sm mt-1">or use 📍 for your current location</p>
          </div>
        )}
      </div>
    </div>
  )
}
