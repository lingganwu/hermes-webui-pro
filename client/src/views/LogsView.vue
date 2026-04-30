<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { NInput, NButton, NScrollbar, NTag } from 'naive-ui'
import { fetchLogs } from '@/api/system'

const logs = ref<string[]>([])
const filter = ref('')
const loading = ref(false)

async function loadLogs() {
  loading.value = true
  try { const { data } = await fetchLogs(); logs.value = data.lines || [] }
  catch { } finally { loading.value = false }
}

const filtered = () => {
  if (!filter.value.trim()) return logs.value
  const q = filter.value.toLowerCase()
  return logs.value.filter(l => l.toLowerCase().includes(q))
}

onMounted(loadLogs)
</script>

<template>
  <div class="page-container">
    <div class="page-header">
      <h2>📋 日志</h2>
      <div style="display:flex;gap:8px">
        <n-input v-model:value="filter" placeholder="过滤..." size="small" clearable style="width:200px" />
        <n-button size="small" @click="loadLogs">刷新</n-button>
      </div>
    </div>
    <div class="logs-body">
      <n-scrollbar>
        <div class="log-lines">
          <div v-for="(line, i) in filtered()" :key="i" class="log-line" :class="{ error: line.includes('ERROR'), warn: line.includes('WARN') }">{{ line }}</div>
          <div v-if="!filtered().length" style="color:var(--text-secondary);text-align:center;padding:40px">暂无日志</div>
        </div>
      </n-scrollbar>
    </div>
  </div>
</template>

<style scoped lang="scss">
.page-container { height: 100%; display: flex; flex-direction: column; overflow: hidden; }
.page-header { display: flex; align-items: center; justify-content: space-between; padding: 20px 24px; border-bottom: 1px solid var(--border-color); flex-shrink: 0; h2 { margin: 0; font-size: 18px; } }
.logs-body { flex: 1; overflow: hidden; background: #0d1117; }
.log-lines { padding: 16px; font-family: 'JetBrains Mono', monospace; font-size: 12px; line-height: 1.8; }
.log-line { color: #c9d1d9; white-space: pre-wrap; word-break: break-all;
  &.error { color: #f85149; }
  &.warn { color: #d29922; }
}
</style>
