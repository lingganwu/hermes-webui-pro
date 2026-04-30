<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { NGrid, NGi, NCard, NStatistic, NSpin, NTag, NProgress } from 'naive-ui'
import client from '@/api/client'

const loading = ref(true)
const dashboard = ref<any>({})
const sessions = ref<any[]>([])
const jobs = ref<any[]>([])

async function loadData() {
  try {
    const [dRes, sRes, jRes] = await Promise.all([
      client.get('/api/dashboard'),
      client.get('/api/sessions'),
      client.get('/api/jobs')
    ])
    dashboard.value = dRes.data || {}
    sessions.value = sRes.data.sessions || []
    jobs.value = jRes.data.jobs || []
  } catch (e) {
    console.error('Failed to load data:', e)
  } finally { 
    loading.value = false 
  }
}

function formatBytes(bytes: number) {
  if (!bytes) return '0 B'
  const k = 1024
  const sizes = ['B', 'KB', 'MB', 'GB']
  const i = Math.floor(Math.log(bytes) / Math.log(k))
  return parseFloat((bytes / Math.pow(k, i)).toFixed(1)) + ' ' + sizes[i]
}

function getProgressColor(value: number) {
  if (value > 90) return '#ef4444'
  if (value > 70) return '#f59e0b'
  return '#6366f1'
}

onMounted(loadData)
</script>

<template>
  <div class="page-container">
    <div class="page-header">
      <div class="header-left">
        <h2>📊 使用统计</h2>
        <span class="header-desc">Hermes Agent 运行状态和数据概览</span>
      </div>
    </div>
    <div class="page-body" v-if="!loading">
      <!-- 系统资源 -->
      <div class="section">
        <div class="section-title">
          <span class="section-icon">💻</span>
          系统资源
        </div>
        <n-grid :cols="3" :x-gap="16" :y-gap="16" responsive="screen" item-responsive>
          <n-gi span="3 m:1">
            <n-card class="resource-card">
              <div class="resource-header">
                <span class="resource-label">CPU 使用率</span>
                <span class="resource-value">{{ dashboard.health?.cpu_percent || 0 }}%</span>
              </div>
              <n-progress 
                type="line" 
                :percentage="dashboard.health?.cpu_percent || 0" 
                :color="getProgressColor(dashboard.health?.cpu_percent || 0)"
                :show-indicator="false"
                :height="8"
                :border-radius="4"
              />
            </n-card>
          </n-gi>
          <n-gi span="3 m:1">
            <n-card class="resource-card">
              <div class="resource-header">
                <span class="resource-label">内存使用率</span>
                <span class="resource-value">{{ dashboard.health?.memory?.percent || 0 }}%</span>
              </div>
              <n-progress 
                type="line" 
                :percentage="dashboard.health?.memory?.percent || 0" 
                :color="getProgressColor(dashboard.health?.memory?.percent || 0)"
                :show-indicator="false"
                :height="8"
                :border-radius="4"
              />
              <div class="resource-detail">
                {{ formatBytes(dashboard.health?.memory?.used) }} / {{ formatBytes(dashboard.health?.memory?.total) }}
              </div>
            </n-card>
          </n-gi>
          <n-gi span="3 m:1">
            <n-card class="resource-card">
              <div class="resource-header">
                <span class="resource-label">磁盘使用率</span>
                <span class="resource-value">{{ dashboard.health?.disk?.percent || 0 }}%</span>
              </div>
              <n-progress 
                type="line" 
                :percentage="dashboard.health?.disk?.percent || 0" 
                :color="getProgressColor(dashboard.health?.disk?.percent || 0)"
                :show-indicator="false"
                :height="8"
                :border-radius="4"
              />
              <div class="resource-detail">
                {{ formatBytes(dashboard.health?.disk?.used) }} / {{ formatBytes(dashboard.health?.disk?.total) }}
              </div>
            </n-card>
          </n-gi>
        </n-grid>
      </div>

      <!-- Agent 数据 -->
      <div class="section">
        <div class="section-title">
          <span class="section-icon">🤖</span>
          Agent 数据
        </div>
        <n-grid :cols="4" :x-gap="16" :y-gap="16" responsive="screen" item-responsive>
          <n-gi span="4 m:2 l:1">
            <n-card class="stat-card gradient-purple">
              <div class="stat-icon">🛠️</div>
              <div class="stat-content">
                <div class="stat-value">{{ dashboard.skills_count || 0 }}</div>
                <div class="stat-label">技能</div>
              </div>
            </n-card>
          </n-gi>
          <n-gi span="4 m:2 l:1">
            <n-card class="stat-card gradient-blue">
              <div class="stat-icon">💬</div>
              <div class="stat-content">
                <div class="stat-value">{{ sessions.length }}</div>
                <div class="stat-label">会话</div>
              </div>
            </n-card>
          </n-gi>
          <n-gi span="4 m:2 l:1">
            <n-card class="stat-card gradient-green">
              <div class="stat-icon">⏰</div>
              <div class="stat-content">
                <div class="stat-value">{{ jobs.length }}</div>
                <div class="stat-label">定时任务</div>
              </div>
            </n-card>
          </n-gi>
          <n-gi span="4 m:2 l:1">
            <n-card class="stat-card gradient-orange">
              <div class="stat-icon">🧠</div>
              <div class="stat-content">
                <div class="stat-value">{{ dashboard.memories_count || 0 }}</div>
                <div class="stat-label">记忆</div>
              </div>
            </n-card>
          </n-gi>
        </n-grid>
      </div>

      <!-- 模型配置 -->
      <div class="section">
        <div class="section-title">
          <span class="section-icon">⚙️</span>
          模型配置
        </div>
        <n-card class="config-card">
          <div class="config-grid">
            <div class="config-item">
              <span class="config-label">默认模型</span>
              <n-tag type="info" size="large">{{ dashboard.models?.default_model || '未知' }}</n-tag>
            </div>
            <div class="config-item">
              <span class="config-label">Provider</span>
              <n-tag type="success" size="large">{{ dashboard.models?.default_provider || '未知' }}</n-tag>
            </div>
            <div class="config-item">
              <span class="config-label">免费模型库</span>
              <n-tag type="warning" size="large">{{ dashboard.models?.free_models_count || 0 }} 个</n-tag>
            </div>
          </div>
        </n-card>
      </div>

      <!-- 网关状态 -->
      <div class="section">
        <div class="section-title">
          <span class="section-icon">🌐</span>
          网关状态
        </div>
        <n-card class="gateway-card">
          <div class="gateway-header">
            <span class="gateway-status" :class="dashboard.gateway?.state">
              <span class="status-dot"></span>
              {{ dashboard.gateway?.state === 'running' ? '运行中' : '离线' }}
            </span>
            <span class="gateway-agents">{{ dashboard.gateway?.active_agents || 0 }} 个活跃 Agent</span>
          </div>
          <div class="platforms-grid">
            <div 
              v-for="(info, name) in (dashboard.gateway?.platforms || {})" 
              :key="name" 
              class="platform-item"
              :class="{ connected: info.state === 'connected' }"
            >
              <span class="platform-name">{{ name }}</span>
              <n-tag size="small" :type="info.state === 'connected' ? 'success' : 'warning'">
                {{ info.state === 'connected' ? '已连接' : info.state }}
              </n-tag>
            </div>
          </div>
        </n-card>
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

.section { margin-bottom: 32px; }
.section-title {
  display: flex;
  align-items: center;
  gap: 10px;
  font-size: 18px;
  font-weight: 600;
  margin-bottom: 16px;
  color: var(--text-primary);
}
.section-icon { font-size: 24px; }

.resource-card {
  background: var(--card-bg);
  border-radius: 14px;
  padding: 20px;
}
.resource-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 12px;
}
.resource-label { font-size: 14px; color: var(--text-secondary); }
.resource-value { font-size: 24px; font-weight: 700; }
.resource-detail { font-size: 12px; color: var(--text-secondary); margin-top: 8px; }

.stat-card {
  border-radius: 14px;
  padding: 24px;
  display: flex;
  align-items: center;
  gap: 20px;
  transition: transform 0.2s, box-shadow 0.2s;
  
  &:hover {
    transform: translateY(-4px);
    box-shadow: 0 12px 32px rgba(0, 0, 0, 0.15);
  }
  
  &.gradient-purple { background: linear-gradient(135deg, #6366f1, #8b5cf6); }
  &.gradient-blue { background: linear-gradient(135deg, #3b82f6, #06b6d4); }
  &.gradient-green { background: linear-gradient(135deg, #22c55e, #10b981); }
  &.gradient-orange { background: linear-gradient(135deg, #f59e0b, #f97316); }
}
.stat-icon { font-size: 40px; }
.stat-content { flex: 1; }
.stat-value { font-size: 36px; font-weight: 800; color: white; }
.stat-label { font-size: 14px; color: rgba(255, 255, 255, 0.85); }

.config-card {
  background: var(--card-bg);
  border-radius: 14px;
}
.config-grid {
  display: flex;
  flex-wrap: wrap;
  gap: 24px;
}
.config-item {
  display: flex;
  align-items: center;
  gap: 12px;
}
.config-label { font-size: 14px; color: var(--text-secondary); min-width: 80px; }

.gateway-card {
  background: var(--card-bg);
  border-radius: 14px;
}
.gateway-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 20px;
}
.gateway-status {
  display: flex;
  align-items: center;
  gap: 8px;
  font-weight: 600;
  
  &.running .status-dot { background: #22c55e; box-shadow: 0 0 8px rgba(34, 197, 94, 0.5); }
  &.stopped .status-dot { background: #ef4444; }
}
.status-dot { width: 10px; height: 10px; border-radius: 50%; }
.gateway-agents { font-size: 13px; color: var(--text-secondary); }

.platforms-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(150px, 1fr));
  gap: 12px;
}
.platform-item {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 12px 16px;
  background: var(--hover-color);
  border-radius: 10px;
  
  &.connected { border: 1px solid rgba(34, 197, 94, 0.3); }
}
.platform-name { font-weight: 500; text-transform: capitalize; }

@media (max-width: 768px) {
  .page-header { padding: 16px; }
  .page-body { padding: 16px; }
  .stat-card { padding: 16px; }
  .stat-value { font-size: 28px; }
}
</style>