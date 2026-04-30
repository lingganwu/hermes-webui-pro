import { defineStore } from 'pinia'
import { ref } from 'vue'
import { sendChatMessage, fetchSessions, fetchSessionMessages } from '@/api/chat'

export interface Message {
  id: string
  role: 'user' | 'assistant' | 'system'
  content: string
  timestamp: number
}

export interface Session {
  id: string
  title: string
  messageCount: number
  model?: string
}

export const useChatStore = defineStore('chat', () => {
  const messages = ref<Message[]>([])
  const sessions = ref<Session[]>([])
  const activeSessionId = ref<string | null>(null)
  const activeSession = ref<Session | null>(null)
  const loading = ref(false)

  async function loadSessions() {
    try {
      const { data } = await fetchSessions()
      sessions.value = data.sessions || []
    } catch { sessions.value = [] }
  }

  async function loadSession(id: string) {
    activeSessionId.value = id
    activeSession.value = sessions.value.find(s => s.id === id) || null
    try {
      const { data } = await fetchSessionMessages(id)
      messages.value = (data.messages || []).map((m: any, i: number) => ({
        id: `${id}-${i}`,
        role: m.role || 'assistant',
        content: m.content || '',
        timestamp: m.timestamp || Date.now(),
      }))
    } catch { messages.value = [] }
  }

  async function createSession() {
    activeSessionId.value = null
    activeSession.value = null
    messages.value = []
  }

  async function sendMessage(content: string) {
    const userMsg: Message = { id: `u-${Date.now()}`, role: 'user', content, timestamp: Date.now() }
    messages.value.push(userMsg)
    loading.value = true
    try {
      const { data } = await sendChatMessage(content)
      const assistantMsg: Message = {
        id: `a-${Date.now()}`,
        role: 'assistant',
        content: data.response || '(empty)',
        timestamp: Date.now(),
      }
      messages.value.push(assistantMsg)
    } catch (e: any) {
      messages.value.push({
        id: `e-${Date.now()}`,
        role: 'system',
        content: `Error: ${e.response?.data?.detail || e.message || 'Unknown'}`,
        timestamp: Date.now(),
      })
    } finally {
      loading.value = false
    }
  }

  return { messages, sessions, activeSessionId, activeSession, loading, loadSessions, loadSession, createSession, sendMessage }
})
