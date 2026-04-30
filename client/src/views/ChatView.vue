<script setup lang="ts">
import { ref, computed, nextTick, onMounted } from 'vue'
import { NInput, NButton, NIcon, NTag, NEmpty, NScrollbar, NDropdown } from 'naive-ui'
import { useChatStore } from '@/stores/chat'
import { useAppStore } from '@/stores/app'
import ChatMessage from '@/components/chat/ChatMessage.vue'

const chatStore = useChatStore()
const appStore = useAppStore()
const inputMsg = ref('')
const scrollRef = ref<InstanceType<typeof NScrollbar>>()
const inputRef = ref()

function scrollToBottom() {
  nextTick(() => { scrollRef.value?.scrollTo({ top: 999999, behavior: 'smooth' }) })
}

async function sendMessage() {
  const text = inputMsg.value.trim()
  if (!text || chatStore.loading) return
  inputMsg.value = ''
  await chatStore.sendMessage(text)
  scrollToBottom()
}

async function selectSession(id: string) {
  await chatStore.loadSession(id)
  scrollToBottom()
}

onMounted(() => { chatStore.loadSessions() })
</script>

<template>
  <div class="chat-view">
    <!-- Session sidebar -->
    <aside class="chat-sidebar">
      <div class="sidebar-header">
        <span>💬 会话</span>
        <n-button size="tiny" quaternary @click="chatStore.createSession()">+ 新建</n-button>
      </div>
      <n-scrollbar class="session-list">
        <div v-for="s in chatStore.sessions" :key="s.id" class="session-item" :class="{ active: s.id === chatStore.activeSessionId }" @click="selectSession(s.id)">
          <div class="session-title">{{ s.title || '新对话' }}</div>
          <div class="session-meta">{{ s.messageCount || 0 }} 条</div>
        </div>
        <n-empty v-if="!chatStore.sessions.length" description="暂无会话" size="small" />
      </n-scrollbar>
    </aside>

    <!-- Chat main -->
    <div class="chat-main">
      <div class="chat-header">
        <span>{{ chatStore.activeSession?.title || 'Hermes Chat' }}</span>
        <n-tag size="small" type="info">{{ appStore.selectedModel || 'default' }}</n-tag>
      </div>

      <n-scrollbar ref="scrollRef" class="chat-messages">
        <div class="messages-inner">
          <ChatMessage v-for="msg in chatStore.messages" :key="msg.id" :message="msg" />
          <div v-if="chatStore.loading" class="typing-indicator">
            <span></span><span></span><span></span>
          </div>
        </div>
      </n-scrollbar>

      <div class="chat-input-bar">
        <n-input ref="inputRef" v-model:value="inputMsg" type="textarea" :rows="1" :autosize="{ minRows: 1, maxRows: 5 }" placeholder="输入消息... (Enter 发送, Shift+Enter 换行)" @keydown.enter.exact.prevent="sendMessage" :disabled="chatStore.loading" />
        <n-button type="primary" :disabled="!inputMsg.trim() || chatStore.loading" @click="sendMessage">
          发送
        </n-button>
      </div>
    </div>
  </div>
</template>

<style scoped lang="scss">
.chat-view { display: flex; height: 100%; overflow: hidden; }
.chat-sidebar { width: 260px; border-right: 1px solid var(--border-color); display: flex; flex-direction: column; flex-shrink: 0; }
.sidebar-header { display: flex; align-items: center; justify-content: space-between; padding: 16px; font-weight: 600; border-bottom: 1px solid var(--border-color); }
.session-list { flex: 1; }
.session-item { padding: 12px 16px; cursor: pointer; border-bottom: 1px solid var(--border-color); transition: background 0.15s;
  &:hover { background: var(--hover-color); }
  &.active { background: rgba(99, 102, 241, 0.1); border-left: 3px solid #6366f1; }
}
.session-title { font-size: 13px; font-weight: 500; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
.session-meta { font-size: 11px; color: var(--text-secondary); margin-top: 2px; }
.chat-main { flex: 1; display: flex; flex-direction: column; min-width: 0; }
.chat-header { padding: 12px 20px; border-bottom: 1px solid var(--border-color); display: flex; align-items: center; justify-content: space-between; font-weight: 600; flex-shrink: 0; }
.chat-messages { flex: 1; }
.messages-inner { padding: 20px; display: flex; flex-direction: column; gap: 12px; min-height: 100%; }
.chat-input-bar { padding: 12px 20px; border-top: 1px solid var(--border-color); display: flex; gap: 10px; align-items: flex-end; flex-shrink: 0; }
.typing-indicator { display: flex; gap: 4px; padding: 12px 16px;
  span { width: 8px; height: 8px; border-radius: 50%; background: var(--text-secondary); animation: bounce 1.4s infinite;
    &:nth-child(2) { animation-delay: 0.2s; }
    &:nth-child(3) { animation-delay: 0.4s; }
  }
}
@keyframes bounce { 0%,80%,100% { transform: scale(0); } 40% { transform: scale(1); } }
</style>
