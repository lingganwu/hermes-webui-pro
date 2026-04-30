<script setup lang="ts">
import { ref, onMounted, onUnmounted, computed } from 'vue'
import { NGrid, NGi, NCard, NStatistic, NTag, NSpin, NProgress, NSpace } from 'naive-ui'
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
  const icons: Record<string, string> = {
    telegram: '📱', discord: '💬', slack: '💼', weixin: '💚', 
    whatsapp: '📞', api_server: '🔌', sms: '✉️'
  }
  return icons[name] || '🌐'
}

function getPlatformLabel(name: string) {
  const labels: Record<string, string> = {
    telegram: 'Telegram', discord: 'Discord', slack: 'Slack', 
    weixin: '微信', whatsapp: 'WhatsApp', api_server: 'API 服务器', sms: '短信'
  }
  return labels[name] || name
}

function getProgressColor(value: number) {
  if (value > 90) return '#ef4444'
  if (value > 70) return '#f59e0b'
  return '#6366f1'
}

const connectedPlatforms = computed(() => {
  const platforms = dashboard.value.gateway?.platforms || {}
  return Object.entries(platforms).filter(([_, info]: any) => info.state === 'connected')
})

const totalPlatforms = computed(() => Object.keys(dashboard.value.gateway?.platforms || {}).length)
</script>

<template>
  <div class="page-container">
    <div class="page-header">
      <div class="header-left">
        <h2>仪表盘</h2>
        <span class="header-desc">系统概览和实时监控</span>
      </div>
      <n-tag :type="dashboard.gateway?.state === 'running' ? 'success' : 'error'" size="medium" round>
        <template #icon>
          <span class="status-dot" :class="dashboard.gateway?.state === 'running' ? 'active' : 'inactive'"></span>
        </template>
        {{ dashboard.gateway?.state === 'running' ? '运行中' : '离线' }}
      </n-tag>
    </div>

    <div class="page-body" v-if="!loading">
      <!-- 系统资源卡片 -->
      <div class="section-title">
        <span class="section-icon">📊</span>
        系统资源
      </div>
      <n-grid :cols="4" :x-gap="16" :y-gap="16" responsive="screen" item-responsive>
        <n-gi span="4 m:2 l:1">
          <n-card class="stat-card" :bordered="false">
            <div class="stat-content">
              <div class="stat-info">
                <span class="stat-label">CPU 使用率</span>
                <span class="stat-value">{{ dashboard.health?.cpu_percent || 0 }}%</span>
              </div>
              <n-progress 
                type="circle" 
                :percentage="dashboard.health?.cpu_percent || 0" 
                :color="getProgressColor(dashboard.health?.cpu_percent || 0)"
                :stroke-width="8"
                :size="60"
              />
            </div>
          </n-card>
        </n-gi>
        <n-gi span="4 m:2 l:1">
          <n-card class="stat-card" :bordered="false">
            <div class="stat-content">
              <div class="stat-info">
                <span class="stat-label">内存使用率</span>
                <span class="stat-value">{{ dashboard.health?.memory?.percent || 0 }}%</span>
              </div>
              <n-progress 
                type="circle" 
                :percentage="dashboard.health?.memory?.percent || 0" 
                :color="getProgressColor(dashboard.health?.memory?.percent || 0)"
                :stroke-width="8"
                :size="60"
              />
            </div>
          </n-card>
        </n-gi>
        <n-gi span="4 m:2 l:1">
          <n-card class="stat-card" :bordered="false">
            <div class="stat-content">
              <div class="stat-info">
                <span class="stat-label">磁盘使用率</span>
                <span class="stat-value">{{ dashboard.health?.disk?.percent || 0 }}%</span>
              </div>
              <n-progress 
                type="circle" 
                :percentage="dashboard.health?.disk?.percent || 0" 
                :color="getProgressColor(dashboard.health?.disk?.percent || 0)"
                :stroke-width="8"
                :size="60"
              />
            </div>
          </n-card>
        </n-gi>
        <n-gi span="4 m:2 l:1">
          <n-card class="stat-card summary-card" :bordered="false">
            <div class="summary-grid">
              <div class="summary-item">
                <span class="summary-num">{{ dashboard.skills_count || 0 }}</span>
                <span class="summary-label">技能</span>
              </div>
              <div class="summary-item">
                <span class="summary-num">{{ dashboard.sessions_count || 0 }}</span>
                <span class="summary-label">会话</span>
              </div>
              <div class="summary-item">
                <span class="summary-num">{{ dashboard.jobs?.length || 0 }}</span>
                <span class="summary-label">任务</span>
              </div>
              <div class="summary-item">
                <span class="summary-num">{{ dashboard.memories_count || 0 }}</span>
                <span class="summary-label">记忆</span>
              </div>
            </div>
          </n-card>
        </n-gi>
      </n-grid>

      <!-- 网关和模型 -->
      <div class="section-title" style="margin-top: 24px;">
        <span class="section-icon">🌐</span>
        连接状态
      </div>
      <n-grid :cols="2" :x-gap="16" :y-gap="16" responsive="screen" item-responsive>
        <n-gi span="2 l:1">
          <n-card class="status-card" :bordered="false">
            <template #header>
              <div class="card-header">
                <span>网关状态</span>
                <n-tag size="small" type="info">{{ connectedPlatforms.length }}/{{ totalPlatforms }} 已连接</n-tag>
              </div>
            </template>
            <div class="platforms-grid">
              <div 
                v-for="(info, name) in (dashboard.gateway?.platforms || {})" 
                :key="name" 
                class="platform-item"
                :class="{ connected: info.state === 'connected' }"
              >
                <div class="platform-icon">{{ getPlatformIcon(name as string) }}</div>
                <div class="platform-info">
                  <span class="platform-name">{{ getPlatformLabel(name as string) }}</span>
                  <span class="platform-status" :class="info.state">
                    {{ info.state === 'connected' ? '已连接' : info.state }}
                  </span>
                </div>
              </div>
            </div>
          </n-card>
        </n-gi>
        <n-gi span="2 l:1">
          <n-card class="status-card" :bordered="false">
            <template #header>
              <div class="card-header">
                <span>模型配置</span>
                <n-tag size="small" type="success">{{ dashboard.models?.free_models_count || 0 }} 免费模型</n-tag>
              </div>
            </template>
            <div class="model-config">
              <div class="config-item">
                <span class="config-label">默认模型</span>
                <n-tag type="info" size="medium">{{ dashboard.models?.default_model || '未知' }}</n-tag>
              </div>
              <div class="config-item">
                <span class="config-label">Provider</span>
                <n-tag type="success" size="medium">{{ dashboard.models?.default_provider || '未知' }}</n-tag>
              </div>
              <div class="config-item">
                <span class="config-label">Base URL</span>
                <span class="config-value">{{ dashboard.models?.base_url || 'N/A' }}</span>
              </div>
            </div>
          </n-card>
        </n-gi>
      </n-grid>

      <!-- 定时任务 -->
      <div class="section-title" style="margin-top: 24px;">
        <span class="section-icon">⏰</span>
        定时任务
      </div>
      <n-card class="jobs-card" :bordered="false">
        <div class="jobs-list" v-if="dashboard.jobs?.length">
          <div v-for="job in dashboard.jobs" :key="job.id" class="job-item">
            <div class="job-left">
              <div class="job-icon" :class="{ active: job.enabled }">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <circle cx="12" cy="12" r="10"/>
                  <polyline points="12 6 12 12 16 14"/>
                </svg>
              </div>
              <div class="job-info">
                <span class="job-name">{{ job.name }}</span>
                <span class="job-schedule">{{ job.schedule_display }}</span>
              </div>
            </div>
            <div class="job-right">
              <n-tag size="small" :type="job.enabled ? 'success' : 'default'">
                {{ job.enabled ? '启用' : '禁用' }}
              </n-tag>
              <span class="job-last" v-if="job.last_run_at">
                上次: {{ new Date(job.last_run_at).toLocaleString('zh-CN') }}
              </span>
            </div>
          </div>
        </div>
        <div v-else class="empty-state">
          <span class="empty-icon">📋</span>
          <span class="empty-text">暂无定时任务</span>
        </div>
      </n-card>
    </div>

    <div v-else class="loading-wrap">
      <n-spin size="large" />
    </div>
  </div>
</template>

<style scoped lang="scss">
.page-container {
  height: 100%;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.page-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 24px 32px;
  border-bottom: 1px solid var(--border-color);
  flex-shrink: 0;
}

.header-left {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

h2 {
  margin: 0;
  font-size: 24px;
  font-weight: 600;
}

.header-desc {
  font-size: 14px;
  color: var(--text-secondary);
}

.status-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  display: inline-block;
  margin-right: 6px;
  
  &.active {
    background: #22c55e;
    box-shadow: 0 0 8px rgba(34, 197, 94, 0.5);
  }
  
  &.inactive {
    background: #ef4444;
  }
}

.page-body {
  flex: 1;
  overflow-y: auto;
  padding: 24px 32px;
}

.section-title {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 16px;
  font-weight: 600;
  margin-bottom: 16px;
  color: var(--text-primary);
}

.section-icon {
  font-size: 20px;
}

.stat-card {
  background: var(--card-bg);
  border-radius: 12px;
  transition: transform 0.2s, box-shadow 0.2s;
  
  &:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 24px rgba(0, 0, 0, 0.1);
  }
}

.stat-content {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.stat-info {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.stat-label {
  font-size: 14px;
  color: var(--text-secondary);
}

.stat-value {
  font-size: 32px;
  font-weight: 700;
  color: var(--text-primary);
}

.summary-card {
  background: linear-gradient(135deg, var(--primary-color) 0%, #818cf8 100%);
  
  .summary-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 16px;
  }
  
  .summary-item {
    display: flex;
    flex-direction: column;
    align-items: center;
  }
  
  .summary-num {
    font-size: 28px;
    font-weight: 700;
    color: white;
  }
  
  .summary-label {
    font-size: 12px;
    color: rgba(255, 255, 255, 0.8);
  }
}

.status-card {
  background: var(--card-bg);
  border-radius: 12px;
}

.card-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  width: 100%;
}

.platforms-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: 12px;
}

.platform-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px;
  background: var(--hover-color);
  border-radius: 8px;
  transition: all 0.2s;
  
  &.connected {
    background: rgba(34, 197, 94, 0.1);
    border: 1px solid rgba(34, 197, 94, 0.2);
  }
}

.platform-icon {
  font-size: 24px;
}

.platform-info {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.platform-name {
  font-weight: 500;
  font-size: 14px;
}

.platform-status {
  font-size: 12px;
  
  &.connected {
    color: #22c55e;
  }
  
  &.disconnected, &.error {
    color: #ef4444;
  }
}

.model-config {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.config-item {
  display: flex;
  align-items: center;
  gap: 12px;
}

.config-label {
  min-width: 80px;
  font-size: 14px;
  color: var(--text-secondary);
}

.config-value {
  font-size: 14px;
  color: var(--text-primary);
  word-break: break-all;
}

.jobs-card {
  background: var(--card-bg);
  border-radius: 12px;
}

.jobs-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.job-item {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 16px;
  background: var(--hover-color);
  border-radius: 8px;
  transition: all 0.2s;
  
  &:hover {
    background: var(--active-color);
  }
}

.job-left {
  display: flex;
  align-items: center;
  gap: 12px;
}

.job-icon {
  width: 40px;
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: var(--card-bg);
  border-radius: 8px;
  color: var(--text-secondary);
  
  &.active {
    color: #22c55e;
    background: rgba(34, 197, 94, 0.1);
  }
  
  svg {
    width: 20px;
    height: 20px;
  }
}

.job-info {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.job-name {
  font-weight: 600;
  font-size: 14px;
}

.job-schedule {
  font-size: 12px;
  color: var(--text-secondary);
}

.job-right {
  display: flex;
  align-items: center;
  gap: 12px;
}

.job-last {
  font-size: 12px;
  color: var(--text-secondary);
}

.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 48px 0;
  gap: 12px;
}

.empty-icon {
  font-size: 48px;
  opacity: 0.5;
}

.empty-text {
  font-size: 14px;
  color: var(--text-secondary);
}

.loading-wrap {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
}
</style>