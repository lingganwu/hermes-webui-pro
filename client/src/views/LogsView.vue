<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { NList, NListItem, NThing, NSpin, NEmpty, NModal, NInput } from 'naive-ui'
import client from '@/api/client'

const loading = ref(true)
const logs = ref<any[]>([])
const showModal = ref(false)
const content = ref('')

async function loadLogs() {
  try { logs.value = (await client.get('/api/logs')).data.logs || [] } catch { } finally { loading.value = false }
}

async function viewLog(name: string) {
  try { content.value = (await client.get('/api/logs/' + name)).data.content || ''; showModal.value = true } catch { }
}

onMounted(loadLogs)
</script>

<template>
  <div class="page-container">
    <div class="page-header"><h2>日志</h2><n-tag size="small">{{ logs.length }} 个</n-tag></div>
    <div class="page-body" v-if="!loading">
      <n-list hoverable v-if="logs.length">
        <n-list-item v-for="l in logs" :key="l.name" @click="viewLog(l.name)" style="cursor:pointer">
          <n-thing :title="l.name" :description="new Date(l.modified).toLocaleString('zh-CN')" />
        </n-list-item>
      </n-list>
      <n-empty v-else description="暂无日志" />
    </div>
    <div v-else class="loading-wrap"><n-spin size="large" /></div>
    <n-modal v-model:show="showModal" preset="card" title="日志内容" style="width:90%">
      <n-input v-model:value="content" type="textarea" :rows="30" readonly style="font-family:monospace" />
    </n-modal>
  </div>
</template>

<style scoped>
.page-container { height: 100%; display: flex; flex-direction: column; overflow: hidden; }
.page-header { display: flex; align-items: center; justify-content: space-between; padding: 20px 24px; border-bottom: 1px solid var(--border-color); }
.page-body { flex: 1; overflow-y: auto; padding: 24px; }
.loading-wrap { flex: 1; display: flex; align-items: center; justify-content: center; }
</style>