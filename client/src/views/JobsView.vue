<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { NCard, NTag, NSpin, NEmpty } from 'naive-ui'
import client from '@/api/client'

const loading = ref(true)
const jobs = ref<any[]>([])

async function loadJobs() {
  try {
    const res = await client.get('/api/jobs')
    jobs.value = res.data.jobs || []
  } catch { } finally { loading.value = false }
}

function getStatusColor(job: any) {
  if (!job.enabled) return 'default'
  if (job.state === 'running') return 'warning'
  return 'success'
}

function getStatusText(job: any) {
  if (!job.enabled) return '已禁用'
  if (job.state === 'running') return '运行中'
  return '已调度'
}

onMounted(loadJobs)
</script>

<template>
  <div class="page-container">
    <div class="page-header">
      <h2>定时任务</h2>
      <n-tag size="small">{{ jobs.length }} 个任务</n-tag>
    </div>
    <div class="page-body" v-if="!loading">
      <div v-if="jobs.length" class="jobs-grid">
        <n-card v-for="job in jobs" :key="job.id" class="job-card">
          <div class="job-header">
            <span class="job-name">{{ job.name || '未命名' }}</span>
            <n-tag size="small" :type="getStatusColor(job)">{{ getStatusText(job) }}</n-tag>
          </div>
          <div class="job-body">
            <div class="job-row">
              <span class="label">调度</span>
              <span>{{ job.schedule_display }}</span>
            </div>
            <div class="job-row" v-if="job.next_run_at">
              <span class="label">下次运行</span>
              <span>{{ new Date(job.next_run_at).toLocaleString('zh-CN') }}</span>
            </div>
            <div class="job-row" v-if="job.last_run_at">
              <span class="label">上次运行</span>
              <span>{{ new Date(job.last_run_at).toLocaleString('zh-CN') }}</span>
            </div>
            <div class="job-row" v-if="job.skills?.length">
              <span class="label">技能</span>
              <div class="skills">
                <n-tag v-for="s in job.skills" :key="s" size="small" type="info">{{ s }}</n-tag>
              </div>
            </div>
          </div>
        </n-card>
      </div>
      <n-empty v-else description="暂无定时任务" />
    </div>
    <div v-else class="loading-wrap"><n-spin size="large" /></div>
  </div>
</template>

<style scoped>
.page-container { height: 100%; display: flex; flex-direction: column; overflow: hidden; }
.page-header { display: flex; align-items: center; justify-content: space-between; padding: 20px 24px; border-bottom: 1px solid var(--border-color); }
.page-body { flex: 1; overflow-y: auto; padding: 24px; }
.loading-wrap { flex: 1; display: flex; align-items: center; justify-content: center; }
.jobs-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(400px, 1fr)); gap: 16px; }
.job-card { border: 1px solid var(--border-color); }
.job-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px; }
.job-name { font-weight: 600; font-size: 16px; }
.job-body { display: flex; flex-direction: column; gap: 8px; }
.job-row { display: flex; align-items: center; gap: 12px; font-size: 13px; }
.label { min-width: 70px; color: var(--text-secondary); }
.skills { display: flex; gap: 6px; flex-wrap: wrap; }
</style>