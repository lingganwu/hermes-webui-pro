<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue'
import { NGrid, NGi, NCard, NStatistic, NTag, NSpin, NProgress } from 'naive-ui'
import { fetchHealth, fetchMetrics } from '@/api/system'

const loading = ref(true)
const health = ref<any>({})
const metrics = ref<any>({})
let timer: ReturnType<typeof setInterval>

async function loadData() {
  try {
    const [h, m] = await Promise.all([fetchHealth(), fetchMetrics()])
    health.value = h.data
    metrics.value = m.data
  } catch { } finally { loading.value = false }
}

onMounted(() => { loadData(); timer = setInterval(loadData, 15000) })
onUnmounted(() => clearInterval(timer))
</script>

<template>
  <div class="page-container">
    <div class="page-header">
      <h2>📊 Dashboard</h2>
      <n-tag :type="health.status === 'ok' ? 'success' : 'error'" size="small">
        {{ health.status === 'ok' ? '🟢 Connected' : '🔴 Disconnected' }}
      </n-tag>
    </div>
    <div class="page-body" v-if="!loading">
      <n-grid :cols="4" :x-gap="16" :y-gap="16" responsive="screen" item-responsive>
        <n-gi span="4 m:2 l:1">
          <n-card>
            <n-statistic label="CPU" :value="metrics.cpu + '%'" />
            <n-progress type="line" :percentage="metrics.cpu || 0" :show-indicator="false" :height="4" :border-radius="2" />
          </n-card>
        </n-gi>
        <n-gi span="4 m:2 l:1">
          <n-card>
            <n-statistic label="内存" :value="metrics.memory + '%'" />
            <n-progress type="line" :percentage="metrics.memory || 0" :show-indicator="false" :height="4" :color="metrics.memory > 80 ? '#ef4444' : '#6366f1'" />
          </n-card>
        </n-gi>
        <n-gi span="4 m:2 l:1">
          <n-card>
            <n-statistic label="磁盘" :value="metrics.disk + '%'" />
            <n-progress type="line" :percentage="metrics.disk || 0" :show-indicator="false" :height="4" />
          </n-card>
        </n-gi>
        <n-gi span="4 m:2 l:1">
          <n-card>
            <n-statistic label="运行时间" :value="health.uptime || 'N/A'" />
          </n-card>
        </n-gi>
      </n-grid>

      <n-grid :cols="2" :x-gap="16" :y-gap="16" style="margin-top:16px" responsive="screen" item-responsive>
        <n-gi span="2 l:1">
          <n-card title="🤖 模型状态">
            <div class="info-list">
              <div class="info-item" v-for="m in (health.models || [])" :key="m">
                <span>{{ m }}</span>
                <n-tag size="small" type="info">active</n-tag>
              </div>
              <div v-if="!health.models?.length" class="empty-hint">暂无模型信息</div>
            </div>
          </n-card>
        </n-gi>
        <n-gi span="2 l:1">
          <n-card title="🌐 网关状态">
            <div class="info-list">
              <div class="info-item" v-for="g in (health.gateways || [])" :key="g.name">
                <span>{{ g.name }}</span>
                <n-tag size="small" :type="g.connected ? 'success' : 'warning'">
                  {{ g.connected ? '在线' : '离线' }}
                </n-tag>
              </div>
              <div v-if="!health.gateways?.length" class="empty-hint">暂无网关信息</div>
            </div>
          </n-card>
        </n-gi>
      </n-grid>
    </div>
    <div v-else class="loading-wrap"><n-spin size="large" /></div>
  </div>
</template>

<style scoped lang="scss">
.page-container { height: 100%; display: flex; flex-direction: column; overflow: hidden; }
.page-header { display: flex; align-items: center; justify-content: space-between; padding: 20px 24px; border-bottom: 1px solid var(--border-color); flex-shrink: 0; h2 { margin: 0; font-size: 18px; } }
.page-body { flex: 1; overflow-y: auto; padding: 24px; }
.loading-wrap { flex: 1; display: flex; align-items: center; justify-content: center; }
.info-list { display: flex; flex-direction: column; gap: 10px; }
.info-item { display: flex; align-items: center; justify-content: space-between; padding: 6px 0; border-bottom: 1px solid var(--border-color); &:last-child { border-bottom: none; } }
.empty-hint { color: var(--text-secondary); font-size: 13px; text-align: center; padding: 16px 0; }
</style>
