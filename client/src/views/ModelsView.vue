<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { NCard, NTag, NGrid, NGi, NEmpty, NSpin, NButton } from 'naive-ui'
import { fetchModels } from '@/api/models'

const loading = ref(true)
const models = ref<any[]>([])
const selectedModel = ref(localStorage.getItem('hermes_selected_model') || '')

async function loadModels() {
  loading.value = true
  try { const { data } = await fetchModels(); models.value = data.models || [] }
  catch { } finally { loading.value = false }
}

function selectModel(id: string) {
  selectedModel.value = id
  localStorage.setItem('hermes_selected_model', id)
}

const tierColors: Record<string, string> = { gold: 'warning', silver: 'default', free: 'success', paid: 'info' }

onMounted(loadModels)
</script>

<template>
  <div class="page-container">
    <div class="page-header">
      <h2>🤖 模型管理</h2>
      <n-button size="small" @click="loadModels">刷新</n-button>
    </div>
    <div class="page-body">
      <n-spin :show="loading">
        <n-grid :cols="3" :x-gap="12" :y-gap="12" responsive="screen" item-responsive v-if="models.length">
          <n-gi span="3 m:1" v-for="m in models" :key="m.id">
            <n-card size="small" :class="{ 'model-active': m.id === selectedModel }" @click="selectModel(m.id)" style="cursor:pointer">
              <div class="model-name">{{ m.name || m.id }}</div>
              <div class="model-meta">
                <n-tag size="tiny" :type="(tierColors[m.tier] as any) || 'default'">{{ m.tier || 'unknown' }}</n-tag>
                <n-tag size="tiny" type="info" v-if="m.provider">{{ m.provider }}</n-tag>
              </div>
              <div class="model-desc" v-if="m.description">{{ m.description }}</div>
            </n-card>
          </n-gi>
        </n-grid>
        <n-empty v-else description="暂无可用模型" />
      </n-spin>
    </div>
  </div>
</template>

<style scoped lang="scss">
.page-container { height: 100%; display: flex; flex-direction: column; overflow: hidden; }
.page-header { display: flex; align-items: center; justify-content: space-between; padding: 20px 24px; border-bottom: 1px solid var(--border-color); flex-shrink: 0; h2 { margin: 0; font-size: 18px; } }
.page-body { flex: 1; overflow-y: auto; padding: 24px; }
.model-active { border-color: #6366f1 !important; box-shadow: 0 0 0 2px rgba(99,102,241,0.3); }
.model-name { font-weight: 600; font-size: 14px; margin-bottom: 6px; }
.model-meta { display: flex; gap: 6px; margin-bottom: 6px; }
.model-desc { font-size: 12px; color: var(--text-secondary); line-height: 1.4; }
</style>
