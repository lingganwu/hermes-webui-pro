<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { NCard, NTag, NSpin, NDescriptions, NDescriptionsItem } from 'naive-ui'
import { fetchGateways } from '@/api/system'

const loading = ref(true)
const gw = ref<any>({})
const pName: Record<string,string> = { telegram:'Telegram', discord:'Discord', weixin:'微信', api_server:'API', sms:'短信' }
const pIcon: Record<string,string> = { telegram:'📱', discord:'💬', weixin:'💚', api_server:'🔌', sms:'✉️' }
async function load() { try { gw.value = (await fetchGateways()).data } catch {} finally { loading.value = false } }
onMounted(load)
</script>

<template>
  <div class="page"><div class="head"><h2>🌐 网关</h2><n-tag :type="gw.state==='running'?'success':'error'">{{ gw.state==='running'?'运行中':'离线' }}</n-tag></div>
    <div class="body" v-if="!loading">
      <n-card title="概览"><n-descriptions bordered :column="2">
        <n-descriptions-item label="状态"><n-tag :type="gw.state==='running'?'success':'error'">{{ gw.state }}</n-tag></n-descriptions-item>
        <n-descriptions-item label="PID">{{ gw.pid || 'N/A' }}</n-descriptions-item>
        <n-descriptions-item label="Agents">{{ gw.active_agents || 0 }}</n-descriptions-item>
      </n-descriptions></n-card>
      <n-card title="平台" style="margin-top:16px">
        <div class="list"><div v-for="(info,name) in gw.platforms" :key="name" class="item">
          <span class="icon">{{ pIcon[String(name)] || '🌐' }}</span>
          <span class="name">{{ pName[String(name)] || String(name) }}</span>
          <n-tag size="small" :type="info.state==='connected'?'success':'warning'">{{ info.state==='connected'?'已连接':info.state }}</n-tag>
        </div></div>
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
.item { display:flex; align-items:center; gap:10px; padding:10px; background:var(--hover-color); border-radius:8px; }
.icon { font-size:20px; }
.name { flex:1; font-weight:500; }
</style>