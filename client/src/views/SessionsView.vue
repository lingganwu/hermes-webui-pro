<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { NList, NListItem, NThing, NTag, NSpin, NEmpty, NInput } from 'naive-ui'
import client from '@/api/client'

const loading = ref(true)
const sessions = ref<any[]>([])
const search = ref('')

const filtered = computed(() => {
  if (!search.value) return sessions.value
  return sessions.value.filter(s => s.title?.toLowerCase().includes(search.value.toLowerCase()))
})

async function loadSessions() {
  try { sessions.value = (await client.get('/api/sessions')).data.sessions || [] } catch { } finally { loading.value = false }
}

onMounted(loadSessions)
</script>

<template>
  <div class="page-container">
    <div class="page-header"><h2>会话历史</h2><n-tag size="small">{{ sessions.length }} 个</n-tag></div>
    <div class="page-body" v-if="!loading">
      <n-input v-model:value="search" placeholder="搜索..." clearable style="margin-bottom:16px" />
      <n-list hoverable v-if="filtered.length">
        <n-list-item v-for="s in filtered" :key="s.id">
          <n-thing :title="s.title || s.id" :description="'消息: ' + (s.message_count || 0)">
            <template #header-extra><span class="date">{{ s.updated_at ? new Date(s.updated_at).toLocaleString('zh-CN') : '' }}</span></template>
          </n-thing>
        </n-list-item>
      </n-list>
      <n-empty v-else description="暂无会话" />
    </div>
    <div v-else class="loading-wrap"><n-spin size="large" /></div>
  </div>
</template>

<style scoped>
.page-container { height: 100%; display: flex; flex-direction: column; overflow: hidden; }
.page-header { display: flex; align-items: center; justify-content: space-between; padding: 20px 24px; border-bottom: 1px solid var(--border-color); }
.page-body { flex: 1; overflow-y: auto; padding: 24px; }
.loading-wrap { flex: 1; display: flex; align-items: center; justify-content: center; }
.date { font-size: 12px; color: var(--text-secondary); }
</style>