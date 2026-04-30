<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { NCard, NTag, NSpin, NDescriptions, NDescriptionsItem } from 'naive-ui'
import { fetchModels, fetchProviders } from '@/api/system'

const loading = ref(true)
const models = ref<any>({})
const providers = ref<any[]>([])
async function load() {
  try { const [m,p] = await Promise.all([fetchModels(), fetchProviders()]); models.value = m.data; providers.value = p.data }
  catch {} finally { loading.value = false }
}
onMounted(load)
</script>

<template>
  <div class="page"><div class="head"><h2>🤖 模型管理</h2><n-tag>{{ models.total_free || 0 }} 免费模型</n-tag></div>
    <div class="body" v-if="!loading">
      <n-card title="当前配置"><n-descriptions bordered :column="2">
        <n-descriptions-item label="模型"><n-tag type="info">{{ models.current?.default || '?' }}</n-tag></n-descriptions-item>
        <n-descriptions-item label="Provider"><n-tag type="success">{{ models.current?.provider || '?' }}</n-tag></n-descriptions-item>
        <n-descriptions-item label="URL" :span="2">{{ models.current?.base_url || 'N/A' }}</n-descriptions-item>
      </n-descriptions></n-card>
      <n-card title="Providers" style="margin-top:16px">
        <div class="list"><div v-for="p in providers" :key="p.name" class="item"><span class="name">{{ p.name }}</span><n-tag size="small" :type="p.type==='primary'?'success':'warning'">{{ p.type }}</n-tag><span class="model">{{ p.model }}</span></div></div>
      </n-card>
    </div>
    <div v-else class="loading"><n-spin size="large" /></div>
  </div>
</template>

<style scoped>
.page { height:100%; display:flex; flex-direction:column; overflow:hidden; }
.head { display:flex; align-items:center; justify-content:space-between; padding:20px 24px; border-bottom:1px solid var(--border-color); }
.head h2 { margin:0; font-size:20px; }
.body { flex:1; overflow-y:auto; padding:24px; display:flex; flex-direction:column; gap:16px; }
.loading { flex:1; display:flex; align-items:center; justify-content:center; }
.list { display:flex; flex-direction:column; gap:10px; }
.item { display:flex; align-items:center; gap:12px; padding:10px; background:var(--hover-color); border-radius:8px; }
.name { font-weight:500; min-width:80px; }
.model { color:var(--text-secondary); font-size:13px; }
</style>