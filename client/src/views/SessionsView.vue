<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { NList, NListItem, NThing, NTag, NSpin, NEmpty, NInput, NCard } from 'naive-ui'
import client from '@/api/client'

const loading = ref(true)
const sessions = ref<any[]>([])
const search = ref('')

const filtered = computed(() => {
  if (!search.value) return sessions.value
  const q = search.value.toLowerCase()
  return sessions.value.filter(s => 
    (s.title || s.id || '').toLowerCase().includes(q)
  )
})

async function loadSessions() {
  try {
    const res = await client.get('/api/sessions')
    sessions.value = res.data.sessions || []
  } catch (e) {
    console.error('Failed to load sessions:', e)
  } finally { 
    loading.value = false 
  }
}

function formatDate(d: string) {
  if (!d) return '-'
  return new Date(d).toLocaleString('zh-CN')
}

onMounted(loadSessions)
</script>

<template>
  <div class="page-container">
    <div class="page-header">
      <div class="header-left">
        <h2>💬 会话历史</h2>
        <span class="header-desc">Hermes Agent 历史会话记录</span>
      </div>
      <n-tag size="medium" round>{{ sessions.length }} 个会话</n-tag>
    </div>
    <div class="page-body" v-if="!loading">
      <n-input v-model:value="search" placeholder="搜索会话..." clearable class="search-input" />
      <div v-if="filtered.length" class="sessions-list">
        <n-card v-for="s in filtered" :key="s.id" class="session-card" hoverable>
          <div class="session-header">
            <span class="session-title">{{ s.title || s.id }}</span>
            <n-tag size="small" type="info">{{ s.message_count || 0 }} 条消息</n-tag>
          </div>
          <div class="session-meta">
            <span v-if="s.created_at">创建: {{ formatDate(s.created_at) }}</span>
            <span v-if="s.updated_at">更新: {{ formatDate(s.updated_at) }}</span>
          </div>
        </n-card>
      </div>
      <div v-else class="empty-state">
        <n-empty description="暂无会话记录" />
      </div>
    </div>
    <div v-else class="loading-wrap"><n-spin size="large" /></div>
  </div>
</template>

<style scoped lang="scss">
.page-container { height: 100%; display: flex; flex-direction: column; overflow: hidden; }
.page-header { 
  display: flex; 
  align-items: center; 
  justify-content: space-between; 
  padding: 24px 32px; 
  border-bottom: 1px solid var(--border-color);
  flex-shrink: 0;
}
.header-left { display: flex; flex-direction: column; gap: 4px; }
h2 { margin: 0; font-size: 22px; font-weight: 600; }
.header-desc { font-size: 13px; color: var(--text-secondary); }
.page-body { flex: 1; overflow-y: auto; padding: 24px 32px; }
.loading-wrap { flex: 1; display: flex; align-items: center; justify-content: center; }
.search-input { margin-bottom: 20px; }
.sessions-list { display: flex; flex-direction: column; gap: 12px; }
.session-card { 
  cursor: pointer; 
  transition: all 0.2s;
  &:hover { transform: translateY(-2px); }
}
.session-header { 
  display: flex; 
  align-items: center; 
  justify-content: space-between; 
  margin-bottom: 8px; 
}
.session-title { font-weight: 600; font-size: 15px; }
.session-meta { 
  display: flex; 
  gap: 16px; 
  font-size: 12px; 
  color: var(--text-secondary); 
}
.empty-state { 
  display: flex; 
  align-items: center; 
  justify-content: center; 
  padding: 60px 0; 
}

@media (max-width: 768px) {
  .page-header { padding: 16px; }
  .page-body { padding: 16px; }
}
</style>