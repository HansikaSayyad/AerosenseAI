export interface Pollutants {
  pm25?: number
  pm10?: number
  o3?: number
  no2?: number
  so2?: number
  co?: number
  [key: string]: number | undefined
}

export interface Weather {
  temperature?: number
  humidity?: number
  wind_speed?: number
  [key: string]: number | undefined
}

export interface Recommendations {
  general: string[]
  outdoor_activity: string[]
  sensitive_groups: string[]
  [key: string]: string[]
}

export interface AQIData {
  city: string
  aqi_value: number
  aqi_category: string
  aqi_color: string
  dominant_pollutant: string
  health_risk_level: string
  pollutants: Pollutants
  weather: Weather
  recommendations: Recommendations
  recorded_at: string
}

export interface AQIResponse {
  success: boolean
  error?: string
  city?: string
  aqi_value?: number
  aqi_category?: string
  aqi_color?: string
  dominant_pollutant?: string
  health_risk_level?: string
  pollutants?: Pollutants
  weather?: Weather
  recommendations?: Recommendations
  recorded_at?: string
}

export interface GPSRequest {
  latitude: number
  longitude: number
}

export interface HistoryEntry {
  id: string
  city: string
  aqi_value: number
  aqi_category: string
  dominant_pollutant: string
  recorded_at: string | null
  created_at: string | null
}
