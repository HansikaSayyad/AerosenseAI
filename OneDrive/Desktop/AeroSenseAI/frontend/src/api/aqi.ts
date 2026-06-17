import { apiClient } from './client'
import type { AQIResponse, GPSRequest, HistoryEntry } from '../types/aqi'

interface HistoryResponse {
  success: boolean
  history: HistoryEntry[]
}

export const aqiApi = {
  getByCity: async (city: string): Promise<AQIResponse> => {
    const res = await apiClient.get<AQIResponse>('/api/v1/aqi/city', {
      params: { city },
    })
    return res.data
  },

  getByGPS: async (data: GPSRequest): Promise<AQIResponse> => {
    const res = await apiClient.post<AQIResponse>('/api/v1/aqi/gps', data)
    return res.data
  },

  getHistory: async (): Promise<HistoryEntry[]> => {
    const res = await apiClient.get<HistoryResponse>('/api/v1/aqi/history')
    return res.data.history
  },
}
