<script setup lang="ts">
import { computed } from 'vue'
import { marked } from 'marked'
import hljs from 'highlight.js'

const props = defineProps<{ message: { role: string; content: string; timestamp?: number } }>()

// Simple marked config
marked.setOptions({ breaks: true, gfm: true })

// Post-process: highlight code blocks
function highlightCode(html: string): string {
  return html.replace(/<pre><code class="language-(\w+)">([\s\S]*?)<\/code><\/pre>/g, (_, lang, code) => {
    try {
      const decoded = code.replace(/&amp;/g, '&').replace(/&lt;/g, '<').replace(/&gt;/g, '>').replace(/&quot;/g, '"')
      const result = hljs.getLanguage(lang) ? hljs.highlight(decoded, { language: lang }).value : hljs.highlightAuto(decoded).value
      return `<pre><code class="hljs language-${lang}">${result}</code></pre>`
    } catch { return `<pre><code class="hljs">${code}</code></pre>` }
  })
}

const html = computed(() => {
  const raw = marked.parse(props.message.content || '') as string
  return highlightCode(raw)
})
const isUser = computed(() => props.message.role === 'user')
const time = computed(() => {
  if (!props.message.timestamp) return ''
  return new Date(props.message.timestamp).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
})
</script>

<template>
  <div class="chat-msg" :class="[message.role]">
    <div class="msg-avatar">{{ isUser ? '👤' : '⚡' }}</div>
    <div class="msg-body">
      <div class="msg-content markdown-body" v-html="html"></div>
      <div class="msg-time">{{ time }}</div>
    </div>
  </div>
</template>

<style scoped lang="scss">
.chat-msg { display: flex; gap: 10px; max-width: 85%;
  &.user { margin-left: auto; flex-direction: row-reverse;
    .msg-body { align-items: flex-end; }
    .msg-content { background: rgba(99, 102, 241, 0.15); border-radius: 16px 4px 16px 16px; }
  }
  &.assistant {
    .msg-content { background: var(--card-color, #1e1e1e); border: 1px solid var(--border-color); border-radius: 4px 16px 16px 16px; }
  }
}
.msg-avatar { width: 32px; height: 32px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 16px; background: var(--hover-color); flex-shrink: 0; }
.msg-body { display: flex; flex-direction: column; gap: 4px; min-width: 0; }
.msg-content { padding: 10px 14px; font-size: 14px; line-height: 1.6; word-break: break-word;
  :deep(pre) { background: #1a1a2e; padding: 12px; border-radius: 8px; overflow-x: auto; margin: 8px 0; }
  :deep(code) { font-family: 'JetBrains Mono', monospace; font-size: 13px; }
  :deep(p) { margin: 0 0 8px; &:last-child { margin: 0; } }
  :deep(ul), :deep(ol) { padding-left: 20px; margin: 4px 0; }
  :deep(blockquote) { border-left: 3px solid #6366f1; padding-left: 12px; margin: 8px 0; opacity: 0.85; }
  :deep(table) { border-collapse: collapse; margin: 8px 0; width: 100%; }
  :deep(th), :deep(td) { border: 1px solid var(--border-color); padding: 6px 10px; text-align: left; }
  :deep(a) { color: #6366f1; }
}
.msg-time { font-size: 11px; color: var(--text-secondary); padding: 0 4px; }
</style>
