<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { NCard, NTag, NSpin, NEmpty, NInput } from 'naive-ui'
import client from '@/api/client'

const loading = ref(true)
const sessions = ref<any[]>([])
const q = ref('')
const filtered = computed(() => q.value ? sessions.value.filter(s => (s.title||s.id||'').toLowerCase().includes(q.value.toLowerCase())) : sessions.value)
async function load() { try { sessions.value = (await client.get('/api/sessions')).data.sessions || [] } catch {} finally { loading.value = false } }
function fmtDate(d: string) { return d ? new Date(d).toLocaleString('zh-CN') : '-' }
onMounted(load)
</script>

<template>
  <div class="page"><div class="head"><h2>💬 会话</h2><n-tag>{{ sessions.length }} 个</n-tag></div>
    <div class="body" v-if="!loading">
      <n-input v-model:value="q" placeholder="搜索..." clearable style="margin-bottom:16px" />
      <div v-if="filtered.length" class="list">
        <n-card v-for="s in filtered" :key="s.id" class="card">
          <div class="row"><span class="title">{{ s.title || s.id }}</span><n-tag size="small" type="info">{{ s.message_count || 0 }} 条</n-tag></div>
          <div class="meta">{{ fmtDate(s.updated_at || s.created_at) }}</div>
        </n-card>
      </div>
      <n-empty v-else description="暂无会话" />
    </div>
    <div v-else class="loading"><n-spin size="large" /></div>
  </div>
</template>

<style scoped>
.page { height:100%; display:flex; flex-direction:column; overflow:hidden; }
.head { display:flex; align-items:center; justify-content:space-between; padding:20px 24px; border-bottom:1px solid var(--border-color); }
.head h2 { margin:0; font-size:20px; }
.body { flex:1; overflow-y:auto; padding:24px; }
.loading { flex:1; display:flex; align-items:center; justify-content:center; }
.list { display:flex; flex-direction:column; gap:10px; }
.row { display:flex; align-items:center; justify-content:space-between; margin-bottom:4px; }
.title { font-weight:600; }
.meta { font-size:12px; color:var(--text-secondary); }
</style>