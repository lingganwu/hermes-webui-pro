<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { NCard, NTag, NSpin, NEmpty, NModal, NInput } from 'naive-ui'
import client from '@/api/client'

const loading = ref(true)
const memories = ref<any[]>([])
const show = ref(false)
const content = ref('')
async function load() { try { memories.value = (await client.get('/api/memory')).data.memories || [] } catch {} finally { loading.value = false } }
async function view(name: string) { try { content.value = (await client.get('/api/memory/' + name)).data.content || ''; show.value = true } catch {} }
function fmtSize(b: number) { return b < 1024 ? b + ' B' : (b/1024).toFixed(1) + ' KB' }
onMounted(load)
</script>

<template>
  <div class="page"><div class="head"><h2>🧠 记忆</h2><n-tag>{{ memories.length }} 条</n-tag></div>
    <div class="body" v-if="!loading">
      <div v-if="memories.length" class="grid">
        <n-card v-for="m in memories" :key="m.name" class="card" hoverable @click="view(m.name)">
          <div class="row"><span class="name">{{ m.name }}</span><n-tag size="small">{{ fmtSize(m.size) }}</n-tag></div>
          <div class="preview">{{ m.preview || '暂无预览' }}</div>
        </n-card>
      </div>
      <n-empty v-else description="暂无记忆" />
    </div>
    <div v-else class="loading"><n-spin size="large" /></div>
    <n-modal v-model:show="show" preset="card" title="记忆内容" style="width:80%"><n-input v-model:value="content" type="textarea" :rows="20" readonly /></n-modal>
  </div>
</template>

<style scoped>
.page { height:100%; display:flex; flex-direction:column; overflow:hidden; }
.head { display:flex; align-items:center; justify-content:space-between; padding:20px 24px; border-bottom:1px solid var(--border-color); }
.head h2 { margin:0; font-size:20px; }
.body { flex:1; overflow-y:auto; padding:24px; }
.loading { flex:1; display:flex; align-items:center; justify-content:center; }
.grid { display:grid; grid-template-columns:repeat(auto-fill,minmax(280px,1fr)); gap:14px; }
.card { cursor:pointer; }
.row { display:flex; justify-content:space-between; margin-bottom:8px; }
.name { font-weight:600; }
.preview { font-size:13px; color:var(--text-secondary); max-height:50px; overflow:hidden; }
</style>