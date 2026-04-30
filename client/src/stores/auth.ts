import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { login as apiLogin, verify as apiVerify, logout as apiLogout } from '@/api/auth'

export const useAuthStore = defineStore('auth', () => {
  const token = ref(localStorage.getItem('hermes_token') || '')
  const isAuthenticated = ref(!!token.value)
  const loading = ref(false)
  const error = ref('')

  async function login(password: string) {
    loading.value = true
    error.value = ''
    try {
      const { data } = await apiLogin(password)
      token.value = data.token
      localStorage.setItem('hermes_token', data.token)
      isAuthenticated.value = true
    } catch (e: any) {
      error.value = e.response?.data?.detail || 'Login failed'
      throw e
    } finally {
      loading.value = false
    }
  }

  async function verify() {
    if (!token.value) {
      isAuthenticated.value = false
      return false
    }
    try {
      await apiVerify()
      isAuthenticated.value = true
      return true
    } catch {
      isAuthenticated.value = false
      token.value = ''
      localStorage.removeItem('hermes_token')
      return false
    }
  }

  function logout() {
    apiLogout()
    token.value = ''
    isAuthenticated.value = false
  }

  return { token, isAuthenticated, loading, error, login, verify, logout }
})
