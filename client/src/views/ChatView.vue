<script setup lang="ts">
import { ref, nextTick } from 'vue'
import { NInput, NButton, NSpin } from 'naive-ui'
import client from '@/api/client'

const msgs = ref<any[]>([{ role: 'system', content: '欢迎使用 Hermes 聊天！', time: new Date() }])
const input = ref('')
const loading = ref(false)
const box = ref<HTMLElement | null>(null)

function scroll() { nextTick(() => { if (box.value) box.value.scrollTop = box.value.scrollHeight }) }

async function send() {
  if (!input.value.trim() || loading.value) return
  const msg = input.value
  msgs.value.push({ role: 'user', content: msg, time: new Date() })
  input.value = ''
  loading.value = true
  scroll()
  try {
    const res = await client.post('/api/chat', { message: msg })
    msgs.value.push({ role: 'assistant', content: res.data.response || res.data.message || 'OK', time: new Date() })
  } catch (e: any) {
    msgs.value.push({ role: 'error', content: e.response?.data?.detail || '发送失败', time: new Date() })
  } finally { loading.value = false; scroll() }
}

function onKey(e: KeyboardEvent) { if (e.key === 'Enter' && !e.shiftKey) { e.preventDefault(); send() } }
</script>

<template>
  <div class="chat">
    <div class="chat-head"><h2>💬 聊天</h2></div>
    <div class="chat-body" ref="box">
      <div v-for="(m, i) in msgs" :key="i" class="msg" :class="m.role">
        <div class="avatar">{{ m.role === 'user' ? '👤' : m.role === 'error' ? '❌' : '🤖' }}</div>
        <div class="bubble">{{ m.content }}</div>
      </div>
      <div v-if="loading" class="msg assistant"><div class="avatar">🤖</div><div class="bubble"><n-spin size="small" /></div></div>
    </div>
    <div class="chat-foot">
      <n-input v-model:value="input" type="textarea" :rows="1" placeholder="输入消息... (Enter 发送)" @keydown="onKey" :disabled="loading" autosize />
      <n-button type="primary" circle @click="send" :loading="loading" :disabled="!input.trim()">➤</n-button>
    </div>
  </div>
</template>

<style scoped>
.chat { height: 100%; display: flex; flex-direction: column; overflow: hidden; }
.chat-head { padding: 20px 24px; border-bottom: 1px solid var(--border-color); flex-shrink: 0; }
.chat-head h2 { margin: 0; font-size: 20px; }
.chat-body { flex: 1; overflow-y: auto; padding: 20px; display: flex; flex-direction: column; gap: 14px; }
.msg { display: flex; gap: 10px; max-width: 80%; }
.msg.user { align-self: flex-end; flex-direction: row-reverse; }
.msg.user .bubble { background: var(--primary-color); color: #fff; border-radius: 16px 16px 4px 16px; }
.msg.assistant .bubble, msg.system .bubble { background: var(--card-bg); border: 1px solid var(--border-color); border-radius: 16px 16px 16px 4px; }
.msg.error .bubble { background: rgba(239,68,68,0.1); border: 1px solid rgba(239,68,68,0.2); color: #ef4444; border-radius: 16px 16px 16px 4px; }
.avatar { width: 32px; height: 32px; display: flex; align-items: center; justify-content: center; font-size: 18px; flex-shrink: 0; }
.bubble { padding: 10px 14px; font-size: 14px; line-height: 1.6; word-break: break-word; white-space: pre-wrap; }
.chat-foot { padding: 14px 20px; border-top: 1px solid var(--border-color); display: flex; gap: 10px; align-items: flex-end; flex-shrink: 0; }
.chat-foot .n-input { flex: 1; }
</style>