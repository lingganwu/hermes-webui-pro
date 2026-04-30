<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { NCard, NTag, NGrid, NGi, NEmpty, NSpin, NButton } from 'naive-ui'
import { fetchGateways } from '@/api/system'

const loading = ref(true)
const gateways = ref<any[]>([])

async function loadGateways() {
  loading.value = true
  try { const { data } = await fetchGateways(); gateways.value = data.gateways || [] }
  catch { } finally { loading.value = false }
}

const iconMap: Record<string, string> = {
  telegram: '✈️', discord: '🎮', slack: '💬', whatsapp: '📱', weixin: '💚',
  sms: '📧', signal: '🔒', matrix: '🔗', feishu: '🐦', web: '🌐',
}

onMounted(loadGateways)
</script>

<template>
  <div class="page-container">
    <div class="page-header">
      <h2>🌐 网关</h2>
      <n-button size="small" @click="loadGateways">刷新</n-button>
    </div>
    <div class="page-body">
      <n-spin :show="loading">
        <n-grid :cols="3" :x-gap="12" :y-gap="12" responsive="screen" item-responsive v-if="gateways.length">
          <n-gi span="3 m:1" v-for="gw in gateways" :key="gw.name">
            <n-card size="small" class="gw-card">
              <div class="gw-header">
                <span class="gw-icon">{{ iconMap[gw.name] || '🔌' }}</span>
                <span class="gw-name">{{ gw.name }}</span>
                <n-tag size="small" :type="gw.connected ? 'success' : 'warning'">
                  {{ gw.connected ? '在线' : '离线' }}
                </n-tag>
              </div>
              <div class="gw-info" v-if="gw.platform">平台: {{ gw.platform }}</div>
            </n-card>
          </n-gi>
        </n-grid>
        <n-empty v-else description="暂无网关" />
      </n-spin>
    </div>
  </div>
</template>

<style scoped lang="scss">
.page-container { height: 100%; display: flex; flex-direction: column; overflow: hidden; }
.page-header { display: flex; align-items: center; justify-content: space-between; padding: 20px 24px; border-bottom: 1px solid var(--border-color); flex-shrink: 0; h2 { margin: 0; font-size: 18px; } }
.page-body { flex: 1; overflow-y: auto; padding: 24px; }
.gw-card { transition: transform 0.15s; &:hover { transform: translateY(-2px); } }
.gw-header { display: flex; align-items: center; gap: 10px; }
.gw-icon { font-size: 24px; }
.gw-name { font-weight: 600; font-size: 15px; flex: 1; }
.gw-info { font-size: 12px; color: var(--text-secondary); margin-top: 8px; }
</style>
