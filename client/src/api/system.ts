import client from './client'

export function fetchHealth() {
  return client.get('/api/health')
}

export function fetchMetrics() {
  return client.get('/api/metrics')
}

export function fetchConfig() {
  return client.get('/api/config')
}

export function updateConfig(data: any) {
  return client.put('/api/config', data)
}

export function fetchLogs() {
  return client.get('/api/logs')
}

export function fetchUsage() {
  return client.get('/api/usage')
}

export function fetchGateways() {
  return client.get('/api/gateways')
}
