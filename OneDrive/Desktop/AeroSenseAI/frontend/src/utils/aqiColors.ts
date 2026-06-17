// Maps AQI category → Tailwind color classes and hex for charts
export interface AQITheme {
  ring: string       // border/ring color class
  badge: string      // background + text badge
  text: string       // large number text color
  bg: string         // card background tint
  hex: string        // hex for recharts
  emoji: string
}

const themes: Record<string, AQITheme> = {
  Good: {
    ring: 'ring-green-400',
    badge: 'bg-green-500/20 text-green-300 border border-green-500/40',
    text: 'text-green-400',
    bg: 'from-green-900/30',
    hex: '#4ade80',
    emoji: '😊',
  },
  Moderate: {
    ring: 'ring-yellow-400',
    badge: 'bg-yellow-500/20 text-yellow-300 border border-yellow-500/40',
    text: 'text-yellow-400',
    bg: 'from-yellow-900/30',
    hex: '#facc15',
    emoji: '😐',
  },
  'Unhealthy for Sensitive Groups': {
    ring: 'ring-orange-400',
    badge: 'bg-orange-500/20 text-orange-300 border border-orange-500/40',
    text: 'text-orange-400',
    bg: 'from-orange-900/30',
    hex: '#fb923c',
    emoji: '😷',
  },
  Unhealthy: {
    ring: 'ring-red-400',
    badge: 'bg-red-500/20 text-red-300 border border-red-500/40',
    text: 'text-red-400',
    bg: 'from-red-900/30',
    hex: '#f87171',
    emoji: '🤢',
  },
  'Very Unhealthy': {
    ring: 'ring-purple-400',
    badge: 'bg-purple-500/20 text-purple-300 border border-purple-500/40',
    text: 'text-purple-400',
    bg: 'from-purple-900/30',
    hex: '#c084fc',
    emoji: '☠️',
  },
  Hazardous: {
    ring: 'ring-rose-600',
    badge: 'bg-rose-800/30 text-rose-300 border border-rose-600/40',
    text: 'text-rose-400',
    bg: 'from-rose-950/40',
    hex: '#e11d48',
    emoji: '💀',
  },
}

const fallback: AQITheme = {
  ring: 'ring-blue-400',
  badge: 'bg-blue-500/20 text-blue-300 border border-blue-500/40',
  text: 'text-blue-400',
  bg: 'from-blue-900/30',
  hex: '#60a5fa',
  emoji: '📊',
}

export function getAQITheme(category: string): AQITheme {
  return themes[category] ?? fallback
}
