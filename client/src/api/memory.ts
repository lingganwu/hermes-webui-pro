import client from './client'

export function fetchMemory() {
  return client.get('/api/memory')
}

export function updateMemory(id: string | null, content: string) {
  if (id) return client.put(`/api/memory/${id}`, { content })
  return client.post('/api/memory', { content })
}

export function deleteMemory(id: string) {
  return client.delete(`/api/memory/${id}`)
}
