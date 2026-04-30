import client from './client'

export function fetchModels() {
  return client.get('/api/models')
}
