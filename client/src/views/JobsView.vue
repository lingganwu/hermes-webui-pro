<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { NCard, NButton, NTag, NEmpty, NSpin, NDataTable, useMessage } from 'naive-ui'
import { fetchJobs, runJob, toggleJob } from '@/api/jobs'

const message = useMessage()
const loading = ref(true)
const jobs = ref<any[]>([])

const columns = [
  { title: '名称', key: 'name', ellipsis: { tooltip: true } },
  { title: '计划', key: 'schedule', width: 120 },
  { title: '状态', key: 'enabled', width: 80, render: (row: any) => row.enabled ? '✅ 启用' : '⏸ 禁用' },
  { title: '上次运行', key: 'lastRun', width: 160, render: (row: any) => row.lastRun ? new Date(row.lastRun).toLocaleString() : '从未' },
  { title: '操作', key: 'actions', width: 180, render: (row: any) => [
    h(NButton, { size: 'tiny', onClick: () => handleToggle(row) }, { default: () => row.enabled ? '禁用' : '启用' }),
    h(NButton, { size: 'tiny', type: 'primary', onClick: () => handleRun(row), style: 'margin-left:6px' }, { default: () => '运行' }),
  ] },
]

import { h } from 'vue'

async function loadJobs() {
  loading.value = true
  try { const { data } = await fetchJobs(); jobs.value = data.jobs || [] }
  catch { } finally { loading.value = false }
}

async function handleRun(job: any) {
  try { await runJob(job.id); message.success(`运行: ${job.name}`) } catch { message.error('运行失败') }
}

async function handleToggle(job: any) {
  try { await toggleJob(job.id, !job.enabled); await loadJobs() } catch { message.error('切换失败') }
}

onMounted(loadJobs)
</script>

<template>
  <div class="page-container">
    <div class="page-header">
      <h2>⏰ 定时任务</h2>
      <n-button size="small" @click="loadJobs">刷新</n-button>
    </div>
    <div class="page-body">
      <n-spin :show="loading">
        <n-data-table v-if="jobs.length" :columns="columns" :data="jobs" :bordered="false" size="small" />
        <n-empty v-else description="暂无定时任务" />
      </n-spin>
    </div>
  </div>
</template>

<style scoped lang="scss">
.page-container { height: 100%; display: flex; flex-direction: column; overflow: hidden; }
.page-header { display: flex; align-items: center; justify-content: space-between; padding: 20px 24px; border-bottom: 1px solid var(--border-color); flex-shrink: 0; h2 { margin: 0; font-size: 18px; } }
.page-body { flex: 1; overflow-y: auto; padding: 24px; }
</style>
