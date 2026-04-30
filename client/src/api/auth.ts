import client from './client'

export interface LoginResponse {
  token: string
  expires_in: number
}

export function login(password: string) {
  return client.post<LoginResponse>('/api/auth/login', { password })
}

export function verify() {
  return client.get('/api/auth/verify')
}

export function logout() {
  localStorage.removeItem('hermes_token')
}
