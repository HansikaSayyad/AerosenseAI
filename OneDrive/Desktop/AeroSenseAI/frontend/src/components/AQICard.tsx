import { getAQITheme } from '../utils/aqiColors'
import type { AQIResponse } from '../types/aqi'

interface Props {
  data: AQIResponse
}

export default function AQICard({ data }: Props) {
  const theme = getAQITheme(data.aqi_category ?? '')

  return (
    <div
      className={`bg-gradient-to-br ${theme.bg} to-slate-800/60 border ${theme.ring.replace('ring-', 'border-')}/40 rounded-2xl p-6 shadow-xl`}
    >
      {/* City + timestamp */}
      <div className="flex items-start justify-between mb-4">
        <div>
          <h2 className="text-2xl font-bold text-white">{data.city}</h2>
          <p className="text-slate-400 text-xs mt-0.5">
            {data.recorded_at ? new Date(data.recorded_at).toLocaleString() : '—'}
          </p>
        </div>
        <span className={`text-xs px-3 py-1 rounded-full font-medium ${theme.badge}`}>
          {theme.emoji} {data.aqi_category}
        </span>
      </div>

      {/* Big AQI number */}
      <div className="flex items-end gap-3 mb-4">
        <span className={`text-7xl font-extrabold leading-none ${theme.text}`}>
          {data.aqi_value}
        </span>
        <div className="pb-2">
          <p className="text-slate-300 text-sm font-medium">AQI</p>
          <p className="text-slate-400 text-xs">US EPA Standard</p>
        </div>
      </div>

      {/* Stats row */}
      <div className="grid grid-cols-3 gap-3 mt-4">
        <Stat label="Dominant Pollutant" value={data.dominant_pollutant ?? '—'} />
        <Stat label="Health Risk" value={data.health_risk_level ?? '—'} />
        <Stat label="Humidity" value={data.weather?.humidity != null ? `${data.weather.humidity}%` : '—'} />
      </div>
    </div>
  )
}

function Stat({ label, value }: { label: string; value: string }) {
  return (
    <div className="bg-white/5 rounded-xl p-3 text-center">
      <p className="text-slate-400 text-xs mb-1">{label}</p>
      <p className="text-white text-sm font-semibold">{value}</p>
    </div>
  )
}
