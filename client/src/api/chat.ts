import client from './client'

export function sendChatMessage(message: string, model?: string) {
  return client.post('/api/chat', { message, model })
}

export function fetchSessions() {
  return client.get('/api/sessions')
}

export function fetchSessionMessages(sessionId: string) {
  return client.get(`/api/sessions/${sessionId}`)
}
