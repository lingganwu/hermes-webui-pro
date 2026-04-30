<script setup lang="ts">
import { ref, onMounted, onUnmounted, computed } from 'vue'
import { NGrid, NGi, NCard, NTag, NSpin, NProgress } from 'naive-ui'
import { fetchDashboard } from '@/api/system'

const loading = ref(true)
const dashboard = ref<any>({})
let timer: ReturnType<typeof setInterval>

async function loadData() {
  try {
    const res = await fetchDashboard()
    dashboard.value = res.data
  } catch { } finally { loading.value = false }
}

onMounted(() => { loadData(); timer = setInterval(loadData, 15000) })
onUnmounted(() => clearInterval(timer))

function getPlatformIcon(name: string) {
  const icons: Record<string, string> = { telegram: '📱', discord: '💬', weixin: '💚', api_server: '🔌' }
  return icons[name] || '🌐'
}

function getPlatformLabel(name: string) {
  const labels: Record<string, string> = { telegram: 'Telegram', discord: 'Discord', weixin: '微信', api_server: 'API 服务器' }
  return labels[name] || name
}

function getProgressColor(value: number) {
  if (value > 90) return '#ef4444'
  if (value > 70) return '#f59e0b'
  return '#6366f1'
}

const connectedCount = computed(() => {
  const platforms = dashboard.value.gateway?.platforms || {}
  return Object.values(platforms).filter((info: any) => info.state === 'connected').length
})
</script>

<template>
  <div class="page-container">
    <div class="page-header">
      <h2>仪表盘</h2>
      <n-tag :type="dashboard.gateway?.state === 'running' ? 'success' : 'error'" size="medium" round>
        <span class="status-dot" :class="dashboard.gateway?.state === 'running' ? 'active' : 'inactive'"></span>
        {{ dashboard.gateway?.state === 'running' ? '运行中' : '离线' }}
      </n-tag>
    </div>
    <div class="page-body" v-if="!loading">
      <n-grid :cols="4" :x-gap="16" :y-gap="16" responsive="screen" item-responsive>
        <n-gi span="4 m:2 l:1">
          <n-card class="stat-card">
            <div class="stat-content">
              <div class="stat-info">
                <span class="stat-label">CPU 使用率</span>
                <span class="stat-value">{{ dashboard.health?.cpu_percent || 0 }}%</span>
              </div>
              <n-progress type="circle" :percentage="dashboard.health?.cpu_percent || 0" :color="getProgressColor(dashboard.health?.cpu_percent || 0)" :stroke-width="8" :size="60" />
            </div>
          </n-card>
        </n-gi>
        <n-gi span="4 m:2 l:1">
          <n-card class="stat-card">
            <div class="stat-content">
              <div class="stat-info">
                <span class="stat-label">内存使用率</span>
                <span class="stat-value">{{ dashboard.health?.memory?.percent || 0 }}%</span>
              </div>
              <n-progress type="circle" :percentage="dashboard.health?.memory?.percent || 0" :color="getProgressColor(dashboard.health?.memory?.percent || 0)" :stroke-width="8" :size="60" />
            </div>
          </n-card>
        </n-gi>
        <n-gi span="4 m:2 l:1">
          <n-card class="stat-card">
            <div class="stat-content">
              <div class="stat-info">
                <span class="stat-label">磁盘使用率</span>
                <span class="stat-value">{{ dashboard.health?.disk?.percent || 0 }}%</span>
              </div>
              <n-progress type="circle" :percentage="dashboard.health?.disk?.percent || 0" :color="getProgressColor(dashboard.health?.disk?.percent || 0)" :stroke-width="8" :size="60" />
            </div>
          </n-card>
        </n-gi>
        <n-gi span="4 m:2 l:1">
          <n-card class="stat-card summary-card">
            <div class="summary-grid">
              <div class="summary-item"><span class="summary-num">{{ dashboard.skills_count || 0 }}</span><span class="summary-label">技能</span></div>
              <div class="summary-item"><span class="summary-num">{{ dashboard.sessions_count || 0 }}</span><span class="summary-label">会话</span></div>
              <div class="summary-item"><span class="summary-num">{{ dashboard.jobs?.length || 0 }}</span><span class="summary-label">任务</span></div>
              <div class="summary-item"><span class="summary-num">{{ dashboard.memories_count || 0 }}</span><span class="summary-label">记忆</span></div>
            </div>
          </n-card>
        </n-gi>
      </n-grid>

      <n-grid :cols="2" :x-gap="16" :y-gap="16" style="margin-top:24px" responsive="screen" item-responsive>
        <n-gi span="2 l:1">
          <n-card class="status-card">
            <template #header><span>网关状态</span></template>
            <div class="platforms-grid">
              <div v-for="(info, name) in (dashboard.gateway?.platforms || {})" :key="name" class="platform-item" :class="{ connected: info.state === 'connected' }">
                <span class="platform-icon">{{ getPlatformIcon(String(name)) }}</span>
                <div class="platform-info">
                  <span class="platform-name">{{ getPlatformLabel(String(name)) }}</span>
                  <span class="platform-status" :class="info.state">{{ info.state === 'connected' ? '已连接' : info.state }}</span>
                </div>
              </div>
            </div>
          </n-card>
        </n-gi>
        <n-gi span="2 l:1">
          <n-card class="status-card">
            <template #header><span>模型配置</span></template>
            <div class="model-config">
              <div class="config-item"><span class="config-label">默认模型</span><n-tag type="info">{{ dashboard.models?.default_model || '未知' }}</n-tag></div>
              <div class="config-item"><span class="config-label">Provider</span><n-tag type="success">{{ dashboard.models?.default_provider || '未知' }}</n-tag></div>
              <div class="config-item"><span class="config-label">免费模型</span><n-tag type="warning">{{ dashboard.models?.free_models_count || 0 }}</n-tag></div>
            </div>
          </n-card>
        </n-gi>
      </n-grid>

      <n-card class="jobs-card" style="margin-top:24px">
        <template #header><span>定时任务</span></template>
        <div class="jobs-list" v-if="dashboard.jobs?.length">
          <div v-for="job in dashboard.jobs" :key="job.id" class="job-item">
            <div class="job-info"><span class="job-name">{{ job.name }}</span><span class="job-schedule">{{ job.schedule_display }}</span></div>
            <n-tag size="small" :type="job.enabled ? 'success' : 'default'">{{ job.enabled ? '启用' : '禁用' }}</n-tag>
          </div>
        </div>
        <div v-else class="empty">暂无定时任务</div>
      </n-card>
    </div>
    <div v-else class="loading-wrap"><n-spin size="large" /></div>
  </div>
</template>

<style scoped lang="scss">
.page-container { height: 100%; display: flex; flex-direction: column; overflow: hidden; }
.page-header { display: flex; align-items: center; justify-content: space-between; padding: 24px 32px; border-bottom: 1px solid var(--border-color); }
h2 { margin: 0; font-size: 24px; font-weight: 600; }
.status-dot { width: 8px; height: 8px; border-radius: 50%; display: inline-block; margin-right: 6px; &.active { background: #22c55e; box-shadow: 0 0 8px rgba(34,197,94,0.5); } &.inactive { background: #ef4444; } }
.page-body { flex: 1; overflow-y: auto; padding: 24px 32px; }
.loading-wrap { flex: 1; display: flex; align-items: center; justify-content: center; }
.stat-card { background: var(--card-bg); border-radius: 12px; &:hover { transform: translateY(-2px); box-shadow: 0 8px 24px rgba(0,0,0,0.1); } }
.stat-content { display: flex; align-items: center; justify-content: space-between; }
.stat-info { display: flex; flex-direction: column; gap: 8px; }
.stat-label { font-size: 14px; color: var(--text-secondary); }
.stat-value { font-size: 32px; font-weight: 700; }
.summary-card { background: linear-gradient(135deg, var(--primary-color) 0%, #818cf8 100%); }
.summary-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 16px; }
.summary-item { display: flex; flex-direction: column; align-items: center; }
.summary-num { font-size: 28px; font-weight: 700; color: white; }
.summary-label { font-size: 12px; color: rgba(255,255,255,0.8); }
.status-card { background: var(--card-bg); border-radius: 12px; }
.platforms-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(200px, 1fr)); gap: 12px; }
.platform-item { display: flex; align-items: center; gap: 12px; padding: 12px; background: var(--hover-color); border-radius: 8px; &.connected { background: rgba(34,197,94,0.1); } }
.platform-icon { font-size: 24px; }
.platform-info { display: flex; flex-direction: column; gap: 4px; }
.platform-name { font-weight: 500; }
.platform-status { font-size: 12px; &.connected { color: #22c55e; } }
.model-config { display: flex; flex-direction: column; gap: 12px; }
.config-item { display: flex; align-items: center; gap: 12px; }
.config-label { min-width: 80px; color: var(--text-secondary); }
.jobs-card { background: var(--card-bg); border-radius: 12px; }
.jobs-list { display: flex; flex-direction: column; gap: 12px; }
.job-item { display: flex; align-items: center; justify-content: space-between; padding: 12px; background: var(--hover-color); border-radius: 8px; }
.job-info { display: flex; flex-direction: column; gap: 4px; }
.job-name { font-weight: 600; }
.job-schedule { font-size: 12px; color: var(--text-secondary); }
.empty { text-align: center; padding: 24px; color: var(--text-secondary); }
</style>