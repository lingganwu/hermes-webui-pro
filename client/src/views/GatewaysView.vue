<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { NCard, NTag, NSpin, NDescriptions, NDescriptionsItem } from 'naive-ui'
import { fetchGateways } from '@/api/system'

const loading = ref(true)
const gateway = ref<any>({})

function getPlatformIcon(name: string) {
  const icons: Record<string, string> = { telegram: '📱', discord: '💬', weixin: '💚', api_server: '🔌' }
  return icons[name] || '🌐'
}

function getPlatformLabel(name: string) {
  const labels: Record<string, string> = { telegram: 'Telegram', discord: 'Discord', weixin: '微信', api_server: 'API 服务器' }
  return labels[name] || name
}

async function loadGateway() {
  try { gateway.value = (await fetchGateways()).data } catch { } finally { loading.value = false }
}

onMounted(loadGateway)
</script>

<template>
  <div class="page-container">
    <div class="page-header">
      <h2>网关状态</h2>
      <n-tag :type="gateway.state === 'running' ? 'success' : 'error'">{{ gateway.state === 'running' ? '运行中' : '离线' }}</n-tag>
    </div>
    <div class="page-body" v-if="!loading">
      <n-card title="概览">
        <n-descriptions bordered :column="2">
          <n-descriptions-item label="状态"><n-tag :type="gateway.state === 'running' ? 'success' : 'error'">{{ gateway.state }}</n-tag></n-descriptions-item>
          <n-descriptions-item label="PID">{{ gateway.pid || 'N/A' }}</n-descriptions-item>
          <n-descriptions-item label="活跃 Agents">{{ gateway.active_agents || 0 }}</n-descriptions-item>
        </n-descriptions>
      </n-card>
      <n-card title="平台" style="margin-top:16px">
        <div class="platforms">
          <div v-for="(info, name) in gateway.platforms" :key="name" class="platform">
            <span class="icon">{{ getPlatformIcon(name as string) }}</span>
            <span class="name">{{ getPlatformLabel(name as string) }}</span>
            <n-tag size="small" :type="info.state === 'connected' ? 'success' : 'warning'">{{ info.state === 'connected' ? '已连接' : info.state }}</n-tag>
          </div>
        </div>
      </n-card>
    </div>
    <div v-else class="loading-wrap"><n-spin size="large" /></div>
  </div>
</template>

<style scoped>
.page-container { height: 100%; display: flex; flex-direction: column; overflow: hidden; }
.page-header { display: flex; align-items: center; justify-content: space-between; padding: 20px 24px; border-bottom: 1px solid var(--border-color); }
.page-body { flex: 1; overflow-y: auto; padding: 24px; display: flex; flex-direction: column; gap: 16px; }
.loading-wrap { flex: 1; display: flex; align-items: center; justify-content: center; }
.platforms { display: flex; flex-direction: column; gap: 12px; }
.platform { display: flex; align-items: center; gap: 12px; padding: 12px; background: var(--hover-color); border-radius: 8px; }
.icon { font-size: 24px; }
.name { flex: 1; font-weight: 500; }
</style>