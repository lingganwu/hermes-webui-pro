<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { NCard, NTag, NSpin, NEmpty } from 'naive-ui'
import client from '@/api/client'

const loading = ref(true)
const jobs = ref<any[]>([])
async function load() { try { jobs.value = (await client.get('/api/jobs')).data.jobs || [] } catch {} finally { loading.value = false } }
onMounted(load)
</script>

<template>
  <div class="page"><div class="head"><h2>⏰ 定时任务</h2><n-tag>{{ jobs.length }} 个</n-tag></div>
    <div class="body" v-if="!loading">
      <div v-if="jobs.length" class="grid">
        <n-card v-for="j in jobs" :key="j.id" class="card">
          <div class="row"><span class="name">{{ j.name }}</span><n-tag size="small" :type="j.enabled?'success':'default'">{{ j.enabled?'启用':'禁用' }}</n-tag></div>
          <div class="meta">调度: {{ j.schedule_display }}<span v-if="j.last_run_at"> | 上次: {{ new Date(j.last_run_at).toLocaleString('zh-CN') }}</span></div>
        </n-card>
      </div>
      <n-empty v-else description="暂无定时任务" />
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
.grid { display:grid; grid-template-columns:repeat(auto-fill,minmax(350px,1fr)); gap:14px; }
.row { display:flex; align-items:center; justify-content:space-between; margin-bottom:8px; }
.name { font-weight:600; }
.meta { font-size:12px; color:var(--text-secondary); }
</style>