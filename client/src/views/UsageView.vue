<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { NGrid, NGi, NCard, NStatistic, NSpin, NEmpty, NTag } from 'naive-ui'
import client from '@/api/client'

const loading = ref(true)
const usage = ref<any>({})
const dashboard = ref<any>({})

async function loadData() {
  try {
    const [uRes, dRes] = await Promise.all([
      client.get('/api/usage'),
      client.get('/api/dashboard')
    ])
    usage.value = uRes.data || {}
    dashboard.value = dRes.data || {}
  } catch (e) {
    console.error('Failed to load usage:', e)
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

onMounted(loadData)
</script>

<template>
  <div class="page-container">
    <div class="page-header">
      <div class="header-left">
        <h2>📊 使用统计</h2>
        <span class="header-desc">系统资源和 API 使用情况</span>
      </div>
    </div>
    <div class="page-body" v-if="!loading">
      <!-- 系统资源 -->
      <div class="section-title">系统资源</div>
      <n-grid :cols="3" :x-gap="16" :y-gap="16" responsive="screen" item-responsive>
        <n-gi span="3 m:1">
          <n-card class="stat-card">
            <n-statistic label="CPU 使用率" :value="(dashboard.health?.cpu_percent || 0) + '%'" />
          </n-card>
        </n-gi>
        <n-gi span="3 m:1">
          <n-card class="stat-card">
            <n-statistic label="内存使用率" :value="(dashboard.health?.memory?.percent || 0) + '%'" />
            <div class="stat-detail">
              {{ formatBytes(dashboard.health?.memory?.used) }} / {{ formatBytes(dashboard.health?.memory?.total) }}
            </div>
          </n-card>
        </n-gi>
        <n-gi span="3 m:1">
          <n-card class="stat-card">
            <n-statistic label="磁盘使用率" :value="(dashboard.health?.disk?.percent || 0) + '%'" />
            <div class="stat-detail">
              {{ formatBytes(dashboard.health?.disk?.used) }} / {{ formatBytes(dashboard.health?.disk?.total) }}
            </div>
          </n-card>
        </n-gi>
      </n-grid>

      <!-- Agent 统计 -->
      <div class="section-title" style="margin-top: 24px;">Agent 统计</div>
      <n-grid :cols="4" :x-gap="16" :y-gap="16" responsive="screen" item-responsive>
        <n-gi span="4 m:2 l:1">
          <n-card class="stat-card accent">
            <n-statistic label="技能数量" :value="dashboard.skills_count || 0" />
          </n-card>
        </n-gi>
        <n-gi span="4 m:2 l:1">
          <n-card class="stat-card accent">
            <n-statistic label="会话数量" :value="dashboard.sessions_count || 0" />
          </n-card>
        </n-gi>
        <n-gi span="4 m:2 l:1">
          <n-card class="stat-card accent">
            <n-statistic label="定时任务" :value="dashboard.jobs?.length || 0" />
          </n-card>
        </n-gi>
        <n-gi span="4 m:2 l:1">
          <n-card class="stat-card accent">
            <n-statistic label="记忆数量" :value="dashboard.memories_count || 0" />
          </n-card>
        </n-gi>
      </n-grid>

      <!-- 模型信息 -->
      <div class="section-title" style="margin-top: 24px;">模型配置</div>
      <n-card class="info-card">
        <div class="info-grid">
          <div class="info-item">
            <span class="info-label">默认模型</span>
            <n-tag type="info" size="medium">{{ dashboard.models?.default_model || '未知' }}</n-tag>
          </div>
          <div class="info-item">
            <span class="info-label">Provider</span>
            <n-tag type="success" size="medium">{{ dashboard.models?.default_provider || '未知' }}</n-tag>
          </div>
          <div class="info-item">
            <span class="info-label">免费模型</span>
            <n-tag type="warning" size="medium">{{ dashboard.models?.free_models_count || 0 }}</n-tag>
          </div>
        </div>
      </n-card>

      <!-- API 统计 -->
      <div v-if="Object.keys(usage).length > 0" style="margin-top: 24px;">
        <div class="section-title">API 使用</div>
        <n-grid :cols="3" :x-gap="16" :y-gap="16" responsive="screen" item-responsive>
          <n-gi span="3 m:1">
            <n-card class="stat-card">
              <n-statistic label="总请求数" :value="usage.total_requests || 0" />
            </n-card>
          </n-gi>
          <n-gi span="3 m:1">
            <n-card class="stat-card">
              <n-statistic label="总 Token 数" :value="usage.total_tokens || 0" />
            </n-card>
          </n-gi>
          <n-gi span="3 m:1">
            <n-card class="stat-card">
              <n-statistic label="平均响应" :value="(usage.avg_response_time || 0) + 'ms'" />
            </n-card>
          </n-gi>
        </n-grid>
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

.section-title {
  font-size: 16px;
  font-weight: 600;
  margin-bottom: 16px;
  color: var(--text-primary);
}

.stat-card {
  background: var(--card-bg);
  border-radius: 12px;
  transition: all 0.2s;
  
  &:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 24px rgba(0, 0, 0, 0.1);
  }
  
  &.accent {
    background: linear-gradient(135deg, var(--primary-color), #818cf8);
    
    :deep(.n-statistic .n-statistic__label) {
      color: rgba(255, 255, 255, 0.8);
    }
    
    :deep(.n-statistic .n-statistic-value__content) {
      color: white;
    }
  }
}

.stat-detail {
  font-size: 12px;
  color: var(--text-secondary);
  margin-top: 4px;
}

.info-card {
  background: var(--card-bg);
  border-radius: 12px;
}

.info-grid {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.info-item {
  display: flex;
  align-items: center;
  gap: 12px;
}

.info-label {
  min-width: 80px;
  color: var(--text-secondary);
}

@media (max-width: 768px) {
  .page-header { padding: 16px; }
  .page-body { padding: 16px; }
}
</style>