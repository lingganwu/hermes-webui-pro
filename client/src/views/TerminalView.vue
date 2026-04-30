<script setup lang="ts">
import { ref, onMounted, onUnmounted, nextTick } from 'vue'
import { NInput, NButton, NScrollbar } from 'naive-ui'

const command = ref('')
const output = ref<Array<{type: string, text: string}>>([])
const history = ref<string[]>([])
const historyIdx = ref(-1)
const scrollRef = ref()
let ws: WebSocket | null = null

function connect() {
  const proto = location.protocol === 'https:' ? 'wss:' : 'ws:'
  ws = new WebSocket(`${proto}//${location.host}/ws/terminal`)
  ws.onmessage = (e) => {
    output.value.push({ type: 'stdout', text: e.data })
    scrollToBottom()
  }
  ws.onclose = () => { setTimeout(connect, 3000) }
}

async function sendCommand() {
  const cmd = command.value.trim()
  if (!cmd) return
  output.value.push({ type: 'cmd', text: `$ ${cmd}` })
  history.value.unshift(cmd)
  historyIdx.value = -1
  command.value = ''
  ws?.send(JSON.stringify({ command: cmd }))
  scrollToBottom()
}

function scrollToBottom() {
  nextTick(() => { scrollRef.value?.scrollTo({ top: 999999 }) })
}

function handleKey(e: KeyboardEvent) {
  if (e.key === 'ArrowUp') {
    e.preventDefault()
    if (historyIdx.value < history.value.length - 1) { historyIdx.value++; command.value = history.value[historyIdx.value] }
  } else if (e.key === 'ArrowDown') {
    e.preventDefault()
    if (historyIdx.value > 0) { historyIdx.value--; command.value = history.value[historyIdx.value] }
    else { historyIdx.value = -1; command.value = '' }
  }
}

function clearOutput() { output.value = [] }

onMounted(connect)
onUnmounted(() => ws?.close())
</script>

<template>
  <div class="page-container">
    <div class="page-header">
      <h2>💻 Terminal</h2>
      <n-button size="small" @click="clearOutput">清屏</n-button>
    </div>
    <div class="terminal-body">
      <n-scrollbar ref="scrollRef" class="terminal-scroll">
        <div class="terminal-output">
          <div v-for="(line, i) in output" :key="i" :class="['term-line', line.type]">{{ line.text }}</div>
        </div>
      </n-scrollbar>
      <div class="terminal-input">
        <span class="prompt">$</span>
        <n-input v-model:value="command" placeholder="输入命令..." size="small" :bordered="false" @keydown.enter="sendCommand" @keydown="handleKey" />
      </div>
    </div>
  </div>
</template>

<style scoped lang="scss">
.page-container { height: 100%; display: flex; flex-direction: column; overflow: hidden; }
.page-header { display: flex; align-items: center; justify-content: space-between; padding: 20px 24px; border-bottom: 1px solid var(--border-color); flex-shrink: 0; h2 { margin: 0; font-size: 18px; } }
.terminal-body { flex: 1; display: flex; flex-direction: column; background: #0d1117; font-family: 'JetBrains Mono', monospace; }
.terminal-scroll { flex: 1; }
.terminal-output { padding: 16px; }
.term-line { font-size: 13px; line-height: 1.6; white-space: pre-wrap; word-break: break-all;
  &.cmd { color: #7ee787; }
  &.stdout { color: #c9d1d9; }
  &.stderr { color: #f85149; }
}
.terminal-input { display: flex; align-items: center; padding: 8px 16px; border-top: 1px solid #21262d; }
.prompt { color: #7ee787; margin-right: 8px; font-weight: 600; }
:deep(.n-input) { --n-color: transparent; --n-border: none; color: #c9d1d9; }
</style>
