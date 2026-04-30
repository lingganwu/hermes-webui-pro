<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { NCard, NTag, NSpin, NDescriptions, NDescriptionsItem } from 'naive-ui'
import { fetchModels, fetchProviders } from '@/api/system'

const loading = ref(true)
const models = ref<any>({})
const providers = ref<any[]>([])

async function loadData() {
  try {
    const [mRes, pRes] = await Promise.all([fetchModels(), fetchProviders()])
    models.value = mRes.data
    providers.value = pRes.data
  } catch { } finally { loading.value = false }
}

onMounted(loadData)
</script>

<template>
  <div class="page-container">
    <div class="page-header">
      <h2>模型管理</h2>
      <n-tag size="small">{{ models.total_free || 0 }} 免费模型</n-tag>
    </div>
    <div class="page-body" v-if="!loading">
      <n-card title="当前配置">
        <n-descriptions bordered :column="2">
          <n-descriptions-item label="默认模型"><n-tag type="info">{{ models.current?.default || '未知' }}</n-tag></n-descriptions-item>
          <n-descriptions-item label="Provider"><n-tag type="success">{{ models.current?.provider || '未知' }}</n-tag></n-descriptions-item>
          <n-descriptions-item label="Base URL" :span="2">{{ models.current?.base_url || 'N/A' }}</n-descriptions-item>
        </n-descriptions>
      </n-card>
      <n-card title="Providers" style="margin-top:16px">
        <div class="providers">
          <div v-for="p in providers" :key="p.name" class="provider">
            <span class="name">{{ p.name }}</span>
            <n-tag size="small" :type="p.type === 'primary' ? 'success' : 'warning'">{{ p.type }}</n-tag>
            <span class="model">{{ p.model }}</span>
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
.providers { display: flex; flex-direction: column; gap: 12px; }
.provider { display: flex; align-items: center; gap: 12px; padding: 12px; background: var(--hover-color); border-radius: 8px; }
.name { font-weight: 500; min-width: 100px; }
.model { color: var(--text-secondary); }
</style>