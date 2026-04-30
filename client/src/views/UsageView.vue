<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { NCard, NGrid, NGi, NStatistic, NDataTable, NSpin } from 'naive-ui'
import { fetchUsage } from '@/api/system'

const loading = ref(true)
const usage = ref<any>({})

const columns = [
  { title: '模型', key: 'model', ellipsis: { tooltip: true } },
  { title: '调用次数', key: 'calls', width: 100 },
  { title: '输入 Tokens', key: 'inputTokens', width: 120 },
  { title: '输出 Tokens', key: 'outputTokens', width: 120 },
]

async function loadUsage() {
  loading.value = true
  try { const { data } = await fetchUsage(); usage.value = data }
  catch { } finally { loading.value = false }
}

onMounted(loadUsage)
</script>

<template>
  <div class="page-container">
    <div class="page-header"><h2>📊 用量统计</h2></div>
    <div class="page-body">
      <n-spin :show="loading">
        <n-grid :cols="4" :x-gap="16" :y-gap="16" responsive="screen" item-responsive>
          <n-gi span="4 m:2 l:1"><n-card><n-statistic label="总调用" :value="usage.totalCalls || 0" /></n-card></n-gi>
          <n-gi span="4 m:2 l:1"><n-card><n-statistic label="输入 Tokens" :value="usage.totalInputTokens || 0" /></n-card></n-gi>
          <n-gi span="4 m:2 l:1"><n-card><n-statistic label="输出 Tokens" :value="usage.totalOutputTokens || 0" /></n-card></n-gi>
          <n-gi span="4 m:2 l:1"><n-card><n-statistic label="估算费用" :value="'$' + (usage.estimatedCost || '0.00')" /></n-card></n-gi>
        </n-grid>
        <n-card title="模型用量明细" style="margin-top:16px" size="small">
          <n-data-table :columns="columns" :data="usage.modelBreakdown || []" :bordered="false" size="small" />
        </n-card>
      </n-spin>
    </div>
  </div>
</template>

<style scoped lang="scss">
.page-container { height: 100%; display: flex; flex-direction: column; overflow: hidden; }
.page-header { display: flex; align-items: center; justify-content: space-between; padding: 20px 24px; border-bottom: 1px solid var(--border-color); flex-shrink: 0; h2 { margin: 0; font-size: 18px; } }
.page-body { flex: 1; overflow-y: auto; padding: 24px; }
</style>
