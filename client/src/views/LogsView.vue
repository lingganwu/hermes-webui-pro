<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { NCard, NSpin, NEmpty, NModal, NInput } from 'naive-ui'
import client from '@/api/client'

const loading = ref(true)
const logs = ref<any[]>([])
const show = ref(false)
const content = ref('')
async function load() { try { logs.value = (await client.get('/api/logs')).data.logs || [] } catch {} finally { loading.value = false } }
async function view(name: string) { try { content.value = (await client.get('/api/logs/' + name)).data.content || ''; show.value = true } catch {} }
onMounted(load)
</script>

<template>
  <div class="page"><div class="head"><h2>📋 日志</h2><n-tag>{{ logs.length }} 个</n-tag></div>
    <div class="body" v-if="!loading">
      <div v-if="logs.length" class="list">
        <n-card v-for="l in logs" :key="l.name" class="card" hoverable @click="view(l.name)">
          <span class="name">{{ l.name }}</span>
          <span class="date">{{ new Date(l.modified).toLocaleString('zh-CN') }}</span>
        </n-card>
      </div>
      <n-empty v-else description="暂无日志" />
    </div>
    <div v-else class="loading"><n-spin size="large" /></div>
    <n-modal v-model:show="show" preset="card" title="日志" style="width:90%"><n-input v-model:value="content" type="textarea" :rows="30" readonly style="font-family:monospace" /></n-modal>
  </div>
</template>

<style scoped>
.page { height:100%; display:flex; flex-direction:column; overflow:hidden; }
.head { display:flex; align-items:center; justify-content:space-between; padding:20px 24px; border-bottom:1px solid var(--border-color); }
.head h2 { margin:0; font-size:20px; }
.body { flex:1; overflow-y:auto; padding:24px; }
.loading { flex:1; display:flex; align-items:center; justify-content:center; }
.list { display:flex; flex-direction:column; gap:10px; }
.card { cursor:pointer; display:flex; align-items:center; justify-content:space-between; }
.name { font-weight:500; }
.date { font-size:12px; color:var(--text-secondary); }
</style>