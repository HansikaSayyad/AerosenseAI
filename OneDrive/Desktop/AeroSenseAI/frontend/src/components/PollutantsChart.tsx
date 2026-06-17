import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  Cell,
} from 'recharts'
import type { Pollutants } from '../types/aqi'

const POLLUTANT_COLORS: Record<string, string> = {
  pm25: '#f87171',
  pm10: '#fb923c',
  o3:   '#facc15',
  no2:  '#a78bfa',
  so2:  '#34d399',
  co:   '#60a5fa',
}

const LABELS: Record<string, string> = {
  pm25: 'PM2.5',
  pm10: 'PM10',
  o3:   'O₃',
  no2:  'NO₂',
  so2:  'SO₂',
  co:   'CO',
}

interface Props {
  pollutants: Pollutants
}

export default function PollutantsChart({ pollutants }: Props) {
  const data = Object.entries(pollutants)
    .filter(([, v]) => v != null && v > 0)
    .map(([key, value]) => ({
      name: LABELS[key] ?? key.toUpperCase(),
      value: value as number,
      color: POLLUTANT_COLORS[key] ?? '#94a3b8',
    }))

  if (data.length === 0) {
    return (
      <div className="bg-white/5 rounded-2xl p-6 border border-white/10 flex items-center justify-center h-48">
        <p className="text-slate-400 text-sm">No pollutant data available</p>
      </div>
    )
  }

  return (
    <div className="bg-white/5 rounded-2xl p-6 border border-white/10">
      <h3 className="text-white font-semibold mb-4 text-sm uppercase tracking-wide">
        Pollutant Levels
      </h3>
      <ResponsiveContainer width="100%" height={200}>
        <BarChart data={data} margin={{ top: 4, right: 8, left: -16, bottom: 0 }}>
          <CartesianGrid strokeDasharray="3 3" stroke="#334155" />
          <XAxis dataKey="name" tick={{ fill: '#94a3b8', fontSize: 12 }} axisLine={false} tickLine={false} />
          <YAxis tick={{ fill: '#94a3b8', fontSize: 11 }} axisLine={false} tickLine={false} />
          <Tooltip
            contentStyle={{ background: '#1e293b', border: '1px solid #334155', borderRadius: 8 }}
            labelStyle={{ color: '#e2e8f0' }}
            itemStyle={{ color: '#94a3b8' }}
          />
          <Bar dataKey="value" radius={[4, 4, 0, 0]}>
            {data.map((entry, i) => (
              <Cell key={i} fill={entry.color} />
            ))}
          </Bar>
        </BarChart>
      </ResponsiveContainer>
    </div>
  )
}
