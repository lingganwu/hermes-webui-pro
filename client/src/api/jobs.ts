import client from './client'

export function fetchJobs() {
  return client.get('/api/jobs')
}

export function runJob(id: string) {
  return client.post(`/api/jobs/${id}/run`)
}

export function toggleJob(id: string, enabled: boolean) {
  return client.post(`/api/jobs/${id}/toggle`, { enabled })
}
