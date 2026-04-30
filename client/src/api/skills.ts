import client from './client'

export function fetchSkills() {
  return client.get('/api/skills')
}
