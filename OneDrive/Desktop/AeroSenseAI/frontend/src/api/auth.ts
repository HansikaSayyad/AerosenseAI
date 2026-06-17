import { apiClient } from './client'
import type { LoginRequest, RegisterRequest, TokenResponse, User } from '../types/auth'

// Actual backend response shapes
interface AuthResponse {
  success: boolean
  tokens: TokenResponse
  user: User
}

interface MeResponse {
  success: boolean
  user: User
}

export const authApi = {
  register: async (data: RegisterRequest): Promise<TokenResponse> => {
    const res = await apiClient.post<AuthResponse>('/api/v1/auth/register', data)
    return res.data.tokens
  },

  login: async (data: LoginRequest): Promise<TokenResponse> => {
    const res = await apiClient.post<AuthResponse>('/api/v1/auth/login', data)
    return res.data.tokens
  },

  me: async (): Promise<User> => {
    const res = await apiClient.get<MeResponse>('/api/v1/auth/me')
    return res.data.user
  },

  refresh: async (refreshToken: string): Promise<TokenResponse> => {
    const res = await apiClient.post<TokenResponse>('/api/v1/auth/refresh', {
      refresh_token: refreshToken,
    })
    return res.data
  },
}
