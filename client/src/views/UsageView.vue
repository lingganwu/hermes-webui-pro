<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { NGrid, NGi, NCard, NStatistic, NSpin, NEmpty } from 'naive-ui'
import client from '@/api/client'

const loading = ref(true)
const usage = ref<any>({})

async function loadUsage() {
  try { usage.value = (await client.get('/api/usage')).data || {} } catch { } finally { loading.value = false }
}

onMounted(loadUsage)
</script>

<template>
  <div class="page-container">
    <div class="page-header"><h2>使用统计</h2></div>
    <div class="page-body" v-if="!loading">
      <n-grid :cols="3" :x-gap="16" responsive="screen" item-responsive>
        <n-gi span="3 m:1"><n-card><n-statistic label="总请求" :value="usage.total_requests || 0" /></n-card></n-gi>
        <n-gi span="3 m:1"><n-card><n-statistic label="总 Token" :value="usage.total_tokens || 0" /></n-card></n-gi>
        <n-gi span="3 m:1"><n-card><n-statistic label="平均响应" :value="(usage.avg_response_time || 0) + 'ms'" /></n-card></n-gi>
      </n-grid>
      <n-empty v-if="!Object.keys(usage).length" description="暂无统计" style="margin-top:20px" />
    </div>
    <div v-else class="loading-wrap"><n-spin size="large" /></div>
  </div>
</template>

<style scoped>
.page-container { height: 100%; display: flex; flex-direction: column; overflow: hidden; }
.page-header { display: flex; align-items: center; justify-content: space-between; padding: 20px 24px; border-bottom: 1px solid var(--border-color); }
.page-body { flex: 1; overflow-y: auto; padding: 24px; }
.loading-wrap { flex: 1; display: flex; align-items: center; justify-content: center; }
</style>