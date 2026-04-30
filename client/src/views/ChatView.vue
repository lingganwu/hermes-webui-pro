<script setup lang="ts">
import { ref, onMounted, nextTick } from 'vue'
import { NInput, NButton, NSpin, NEmpty } from 'naive-ui'
import client from '@/api/client'

const messages = ref<any[]>([])
const input = ref('')
const loading = ref(false)
const chatContainer = ref<HTMLElement | null>(null)

function scrollToBottom() {
  nextTick(() => {
    if (chatContainer.value) {
      chatContainer.value.scrollTop = chatContainer.value.scrollHeight
    }
  })
}

async function sendMessage() {
  if (!input.value.trim() || loading.value) return
  
  const userMsg = { role: 'user', content: input.value, time: new Date() }
  messages.value.push(userMsg)
  const msg = input.value
  input.value = ''
  loading.value = true
  scrollToBottom()
  
  try {
    const res = await client.post('/api/chat', { message: msg })
    messages.value.push({ 
      role: 'assistant', 
      content: res.data.response || res.data.message || '收到消息', 
      time: new Date() 
    })
  } catch (e: any) {
    messages.value.push({ 
      role: 'error', 
      content: e.response?.data?.detail || '发送失败', 
      time: new Date() 
    })
  } finally {
    loading.value = false
    scrollToBottom()
  }
}

function handleKeydown(e: KeyboardEvent) {
  if (e.key === 'Enter' && !e.shiftKey) {
    e.preventDefault()
    sendMessage()
  }
}

onMounted(() => {
  messages.value.push({
    role: 'system',
    content: '欢迎使用 Hermes Agent 聊天功能！输入消息开始对话。',
    time: new Date()
  })
})
</script>

<template>
  <div class="chat-page">
    <div class="chat-header">
      <h2>💬 聊天</h2>
      <span class="chat-desc">与 Hermes Agent 实时对话</span>
    </div>
    
    <div class="chat-messages" ref="chatContainer">
      <div v-for="(msg, i) in messages" :key="i" class="message" :class="msg.role">
        <div class="message-avatar">
          {{ msg.role === 'user' ? '👤' : msg.role === 'error' ? '❌' : '🤖' }}
        </div>
        <div class="message-content">
          <div class="message-text">{{ msg.content }}</div>
          <div class="message-time">{{ msg.time?.toLocaleTimeString('zh-CN') }}</div>
        </div>
      </div>
      <div v-if="loading" class="message assistant">
        <div class="message-avatar">🤖</div>
        <div class="message-content">
          <n-spin size="small" />
        </div>
      </div>
      <div v-if="!messages.length" class="empty-state">
        <n-empty description="开始对话吧" />
      </div>
    </div>
    
    <div class="chat-input">
      <n-input 
        v-model:value="input" 
        type="textarea" 
        :rows="1" 
        placeholder="输入消息... (Enter 发送)" 
        @keydown="handleKeydown"
        :disabled="loading"
        autosize
        :maxlength="4000"
      />
      <n-button 
        type="primary" 
        @click="sendMessage" 
        :loading="loading"
        :disabled="!input.trim()"
        circle
      >
        <template #icon>
          <span style="font-size: 18px;">➤</span>
        </template>
      </n-button>
    </div>
  </div>
</template>

<style scoped lang="scss">
.chat-page {
  height: 100%;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.chat-header {
  padding: 20px 24px;
  border-bottom: 1px solid var(--border-color);
  flex-shrink: 0;
  
  h2 {
    margin: 0;
    font-size: 20px;
    font-weight: 600;
  }
  
  .chat-desc {
    font-size: 13px;
    color: var(--text-secondary);
  }
}

.chat-messages {
  flex: 1;
  overflow-y: auto;
  padding: 20px;
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.message {
  display: flex;
  gap: 12px;
  max-width: 85%;
  
  &.user {
    align-self: flex-end;
    flex-direction: row-reverse;
    
    .message-content {
      background: var(--primary-color);
      color: white;
      border-radius: 16px 16px 4px 16px;
    }
  }
  
  &.assistant, &.system {
    align-self: flex-start;
    
    .message-content {
      background: var(--card-bg);
      border: 1px solid var(--border-color);
      border-radius: 16px 16px 16px 4px;
    }
  }
  
  &.error {
    align-self: flex-start;
    
    .message-content {
      background: rgba(239, 68, 68, 0.1);
      border: 1px solid rgba(239, 68, 68, 0.2);
      border-radius: 16px 16px 16px 4px;
      color: #ef4444;
    }
  }
}

.message-avatar {
  width: 36px;
  height: 36px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 20px;
  flex-shrink: 0;
}

.message-content {
  padding: 12px 16px;
  max-width: 100%;
}

.message-text {
  font-size: 14px;
  line-height: 1.6;
  word-break: break-word;
  white-space: pre-wrap;
}

.message-time {
  font-size: 11px;
  color: var(--text-secondary);
  margin-top: 4px;
  opacity: 0.7;
}

.empty-state {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
}

.chat-input {
  padding: 16px 20px;
  border-top: 1px solid var(--border-color);
  display: flex;
  gap: 12px;
  align-items: flex-end;
  flex-shrink: 0;
  background: var(--body-color);
  
  :deep(.n-input) {
    flex: 1;
  }
}

/* 手机端适配 */
@media (max-width: 768px) {
  .chat-header {
    padding: 16px;
  }
  
  .chat-messages {
    padding: 12px;
  }
  
  .message {
    max-width: 90%;
  }
  
  .chat-input {
    padding: 12px;
  }
}
</style>