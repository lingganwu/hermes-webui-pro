<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { NGrid, NGi, NCard, NStatistic, NSpin, NProgress } from 'naive-ui'
import { fetchDashboard } from '@/api/system'

const loading = ref(true)
const d = ref<any>({})
async function load() { try { d.value = (await fetchDashboard()).data } catch {} finally { loading.value = false } }
function rColor(v: number) { return v > 90 ? '#ef4444' : v > 70 ? '#f59e0b' : '#6366f1' }
function fmtBytes(b: number) { if(!b) return '0 B'; const k=1024; const s=['B','KB','MB','GB']; const i=Math.floor(Math.log(b)/Math.log(k)); return (b/Math.pow(k,i)).toFixed(1)+' '+s[i] }
onMounted(load)
</script>

<template>
  <div class="page"><div class="head"><h2>📈 统计</h2></div>
    <div class="body" v-if="!loading">
      <div class="section">系统资源</div>
      <n-grid :cols="3" :x-gap="16" :y-gap="16" responsive="screen" item-responsive>
        <n-gi span="3 m:1"><n-card class="res"><div class="res-head"><span>CPU</span><span class="val">{{ d.health?.cpu_percent || 0 }}%</span></div><n-progress :percentage="d.health?.cpu_percent || 0" :color="rColor(d.health?.cpu_percent || 0)" :show-indicator="false" :height="8" /></n-card></n-gi>
        <n-gi span="3 m:1"><n-card class="res"><div class="res-head"><span>内存</span><span class="val">{{ d.health?.memory?.percent || 0 }}%</span></div><n-progress :percentage="d.health?.memory?.percent || 0" :color="rColor(d.health?.memory?.percent || 0)" :show-indicator="false" :height="8" /><div class="detail">{{ fmtBytes(d.health?.memory?.used) }} / {{ fmtBytes(d.health?.memory?.total) }}</div></n-card></n-gi>
        <n-gi span="3 m:1"><n-card class="res"><div class="res-head"><span>磁盘</span><span class="val">{{ d.health?.disk?.percent || 0 }}%</span></div><n-progress :percentage="d.health?.disk?.percent || 0" :color="rColor(d.health?.disk?.percent || 0)" :show-indicator="false" :height="8" /><div class="detail">{{ fmtBytes(d.health?.disk?.used) }} / {{ fmtBytes(d.health?.disk?.total) }}</div></n-card></n-gi>
      </n-grid>

      <div class="section" style="margin-top:24px">Agent 数据</div>
      <n-grid :cols="4" :x-gap="16" :y-gap="16" responsive="screen" item-responsive>
        <n-gi span="4 m:2 l:1"><n-card class="stat purple"><div class="stat-icon">🛠️</div><div><div class="stat-num">{{ d.skills_count || 0 }}</div><div class="stat-label">技能</div></div></n-card></n-gi>
        <n-gi span="4 m:2 l:1"><n-card class="stat blue"><div class="stat-icon">💬</div><div><div class="stat-num">{{ d.sessions_count || 0 }}</div><div class="stat-label">会话</div></div></n-card></n-gi>
        <n-gi span="4 m:2 l:1"><n-card class="stat green"><div class="stat-icon">⏰</div><div><div class="stat-num">{{ d.jobs?.length || 0 }}</div><div class="stat-label">任务</div></div></n-card></n-gi>
        <n-gi span="4 m:2 l:1"><n-card class="stat orange"><div class="stat-icon">🧠</div><div><div class="stat-num">{{ d.memories_count || 0 }}</div><div class="stat-label">记忆</div></div></n-card></n-gi>
      </n-grid>

      <div class="section" style="margin-top:24px">模型配置</div>
      <n-card class="cfg">
        <div class="cfg-row"><span>默认模型</span><span class="val">{{ d.models?.default_model || '?' }}</span></div>
        <div class="cfg-row"><span>Provider</span><span class="val">{{ d.models?.default_provider || '?' }}</span></div>
        <div class="cfg-row"><span>免费模型</span><span class="val">{{ d.models?.free_models_count || 0 }}</span></div>
      </n-card>

      <div class="section" style="margin-top:24px">网关</div>
      <n-card class="cfg">
        <div class="cfg-row"><span>状态</span><span class="val" :style="{color: d.gateway?.state==='running'?'#22c55e':'#ef4444'}">{{ d.gateway?.state==='running'?'运行中':'离线' }}</span></div>
        <div class="cfg-row"><span>Agents</span><span class="val">{{ d.gateway?.active_agents || 0 }}</span></div>
        <div class="plat-grid"><div v-for="(info,name) in d.gateway?.platforms" :key="name" class="plat"><span>{{ name }}</span><n-tag size="small" :type="info.state==='connected'?'success':'warning'">{{ info.state==='connected'?'已连接':info.state }}</n-tag></div></div>
      </n-card>
    </div>
    <div v-else class="loading"><n-spin size="large" /></div>
  </div>
</template>

<style scoped>
.page { height:100%; display:flex; flex-direction:column; overflow:hidden; }
.head { display:flex; align-items:center; justify-content:space-between; padding:20px 24px; border-bottom:1px solid var(--border-color); }
.head h2 { margin:0; font-size:20px; }
.body { flex:1; overflow-y:auto; padding:24px; }
.loading { flex:1; display:flex; align-items:center; justify-content:center; }
.section { font-size:16px; font-weight:600; margin-bottom:14px; }
.res { border-radius:12px; }
.res-head { display:flex; justify-content:space-between; align-items:center; margin-bottom:8px; }
.val { font-size:20px; font-weight:700; }
.detail { font-size:12px; color:var(--text-secondary); margin-top:6px; }
.stat { border-radius:12px; display:flex; align-items:center; gap:16px; }
.stat.purple { background:linear-gradient(135deg,#6366f1,#8b5cf6); }
.stat.blue { background:linear-gradient(135deg,#3b82f6,#06b6d4); }
.stat.green { background:linear-gradient(135deg,#22c55e,#10b981); }
.stat.orange { background:linear-gradient(135deg,#f59e0b,#f97316); }
.stat-icon { font-size:36px; }
.stat-num { font-size:32px; font-weight:800; color:#fff; }
.stat-label { font-size:13px; color:rgba(255,255,255,0.85); }
.cfg { border-radius:12px; }
.cfg-row { display:flex; justify-content:space-between; padding:10px 0; border-bottom:1px solid var(--border-color); }
.cfg-row:last-child { border-bottom:none; }
.cfg-row span:first-child { color:var(--text-secondary); }
.plat-grid { display:grid; grid-template-columns:repeat(auto-fill,minmax(140px,1fr)); gap:10px; margin-top:12px; }
.plat { display:flex; align-items:center; justify-content:space-between; padding:8px 12px; background:var(--hover-color); border-radius:8px; }
</style>