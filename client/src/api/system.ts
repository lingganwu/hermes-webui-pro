import client from './client'

export function fetchDashboard() {
  return client.get('/api/dashboard')
}

export function fetchHealth() {
  return client.get('/api/health')
}

export function fetchConfig() {
  return client.get('/api/config')
}

export function updateConfig(updates: any) {
  return client.put('/api/config', { updates })
}

export function fetchLogs() {
  return client.get('/api/logs')
}

export function fetchLogContent(name: string, lines = 200) {
  return client.get('/api/logs/' + name, { params: { lines } })
}

export function fetchUsage() {
  return client.get('/api/usage')
}

export function fetchGateways() {
  return client.get('/api/gateways')
}

export function fetchProviders() {
  return client.get('/api/providers')
}

export function fetchModels() {
  return client.get('/api/models')
}

export function fetchJobs() {
  return client.get('/api/jobs')
}

export function fetchSkills() {
  return client.get('/api/skills')
}

export function fetchMemory() {
  return client.get('/api/memory')
}

export function fetchSessions() {
  return client.get('/api/sessions')
}