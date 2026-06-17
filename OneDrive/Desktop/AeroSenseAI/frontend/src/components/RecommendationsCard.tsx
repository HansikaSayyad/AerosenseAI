interface BackendRecommendations {
  aqi_category?: string
  general_advice?: string
  outdoor_activity?: string
  mask_required?: string
  window_advice?: string
  sensitive_groups?: string[]
}

interface Props {
  recommendations: BackendRecommendations
  category: string
}

export default function RecommendationsCard({ recommendations, category }: Props) {
  const rows: { icon: string; label: string; value: string }[] = [
    { icon: '💡', label: 'General Advice',    value: recommendations.general_advice  ?? '—' },
    { icon: '🏃', label: 'Outdoor Activity',  value: recommendations.outdoor_activity ?? '—' },
    { icon: '😷', label: 'Mask Required',     value: recommendations.mask_required    ?? '—' },
    { icon: '🪟', label: 'Windows',           value: recommendations.window_advice    ?? '—' },
  ]

  const sensitiveGroups = Array.isArray(recommendations.sensitive_groups)
    ? recommendations.sensitive_groups
    : []

  return (
    <div className="bg-white/5 rounded-2xl p-6 border border-white/10">
      <div className="flex items-center gap-2 mb-5">
        <span className="text-xl">🤖</span>
        <h3 className="text-white font-semibold text-sm uppercase tracking-wide">
          AI Recommendations
        </h3>
        <span className="ml-auto text-xs text-slate-400 bg-white/5 px-2 py-0.5 rounded-full">
          {category}
        </span>
      </div>

      {/* Key-value rows */}
      <div className="space-y-3 mb-5">
        {rows.map(({ icon, label, value }) => (
          <div key={label} className="flex items-start justify-between gap-4">
            <span className="text-slate-400 text-sm flex items-center gap-1.5 shrink-0">
              {icon} {label}
            </span>
            <span className="text-white text-sm text-right capitalize">{value}</span>
          </div>
        ))}
      </div>

      {/* Sensitive groups list */}
      {sensitiveGroups.length > 0 && (
        <div className="border-t border-white/10 pt-4">
          <p className="text-slate-300 text-xs font-semibold mb-2 flex items-center gap-1">
            🏥 Sensitive Groups
          </p>
          <ul className="space-y-1.5">
            {sensitiveGroups.map((item, i) => (
              <li key={i} className="flex items-start gap-2 text-slate-400 text-sm">
                <span className="text-blue-400 mt-0.5 shrink-0">•</span>
                {item}
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  )
}
