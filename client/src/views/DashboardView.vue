<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue'
import { NGrid, NGi, NCard, NTag, NSpin, NProgress } from 'naive-ui'
import { fetchDashboard } from '@/api/system'

const loading = ref(true)
const d = ref<any>({})
let timer: ReturnType<typeof setInterval>

async function load() {
  try { d.value = (await fetchDashboard()).data } catch {} finally { loading.value = false }
}
onMounted(() => { load(); timer = setInterval(load, 15000) })
onUnmounted(() => clearInterval(timer))

const platformNames: Record<string, string> = { telegram: 'Telegram', discord: 'Discord', weixin: '微信', api_server: 'API', sms: '短信', whatsapp: 'WhatsApp' }
const platformIcons: Record<string, string> = { telegram: '📱', discord: '💬', weixin: '💚', api_server: '🔌', sms: '✉️', whatsapp: '📞' }
function pName(k: string) { return platformNames[k] || k }
function pIcon(k: string) { return platformIcons[k] || '🌐' }
function pColor(v: string) { return v === 'connected' ? 'success' : 'warning' }
function pLabel(v: string) { return v === 'connected' ? '已连接' : v }
function rColor(v: number) { return v > 90 ? '#ef4444' : v > 70 ? '#f59e0b' : '#6366f1' }
</script>

<template>
  <div class="page">
    <div class="page-head">
      <h2>📊 仪表盘</h2>
      <n-tag :type="d.gateway?.state === 'running' ? 'success' : 'error'" round>
        {{ d.gateway?.state === 'running' ? '🟢 运行中' : '🔴 离线' }}
      </n-tag>
    </div>
    <div class="page-body" v-if="!loading">
      <!-- 资源 -->
      <n-grid :cols="4" :x-gap="16" :y-gap="16" responsive="screen" item-responsive>
        <n-gi span="4 m:2 l:1">
          <n-card class="card"><div class="res"><div><div class="res-label">CPU</div><div class="res-val">{{ d.health?.cpu_percent || 0 }}%</div></div><n-progress type="circle" :percentage="d.health?.cpu_percent || 0" :color="rColor(d.health?.cpu_percent || 0)" :stroke-width="8" :size="56" /></div></n-card>
        </n-gi>
        <n-gi span="4 m:2 l:1">
          <n-card class="card"><div class="res"><div><div class="res-label">内存</div><div class="res-val">{{ d.health?.memory?.percent || 0 }}%</div></div><n-progress type="circle" :percentage="d.health?.memory?.percent || 0" :color="rColor(d.health?.memory?.percent || 0)" :stroke-width="8" :size="56" /></div></n-card>
        </n-gi>
        <n-gi span="4 m:2 l:1">
          <n-card class="card"><div class="res"><div><div class="res-label">磁盘</div><div class="res-val">{{ d.health?.disk?.percent || 0 }}%</div></div><n-progress type="circle" :percentage="d.health?.disk?.percent || 0" :color="rColor(d.health?.disk?.percent || 0)" :stroke-width="8" :size="56" /></div></n-card>
        </n-gi>
        <n-gi span="4 m:2 l:1">
          <n-card class="card summary"><div class="sum-grid"><div class="sum-item"><div class="sum-num">{{ d.skills_count || 0 }}</div><div class="sum-label">技能</div></div><div class="sum-item"><div class="sum-num">{{ d.sessions_count || 0 }}</div><div class="sum-label">会话</div></div><div class="sum-item"><div class="sum-num">{{ d.jobs?.length || 0 }}</div><div class="sum-label">任务</div></div><div class="sum-item"><div class="sum-num">{{ d.memories_count || 0 }}</div><div class="sum-label">记忆</div></div></div></n-card>
        </n-gi>
      </n-grid>

      <!-- 网关 + 模型 -->
      <n-grid :cols="2" :x-gap="16" :y-gap="16" style="margin-top:20px" responsive="screen" item-responsive>
        <n-gi span="2 l:1">
          <n-card title="🌐 网关状态" class="card">
            <div class="plat-grid">
              <div v-for="(info, name) in d.gateway?.platforms" :key="name" class="plat" :class="info.state">
                <span class="plat-icon">{{ pIcon(String(name)) }}</span>
                <span class="plat-name">{{ pName(String(name)) }}</span>
                <n-tag size="small" :type="pColor(info.state)">{{ pLabel(info.state) }}</n-tag>
              </div>
            </div>
          </n-card>
        </n-gi>
        <n-gi span="2 l:1">
          <n-card title="🤖 模型" class="card">
            <div class="model-row"><span>默认模型</span><n-tag type="info">{{ d.models?.default_model || '未知' }}</n-tag></div>
            <div class="model-row"><span>Provider</span><n-tag type="success">{{ d.models?.default_provider || '未知' }}</n-tag></div>
            <div class="model-row"><span>免费模型</span><n-tag type="warning">{{ d.models?.free_models_count || 0 }}</n-tag></div>
          </n-card>
        </n-gi>
      </n-grid>

      <!-- 任务 -->
      <n-card title="⏰ 定时任务" style="margin-top:20px" class="card">
        <div v-if="d.jobs?.length" class="job-list">
          <div v-for="j in d.jobs" :key="j.id" class="job">
            <div><div class="job-name">{{ j.name }}</div><div class="job-schedule">{{ j.schedule_display }}</div></div>
            <n-tag size="small" :type="j.enabled ? 'success' : 'default'">{{ j.enabled ? '启用' : '禁用' }}</n-tag>
          </div>
        </div>
        <div v-else class="empty">暂无定时任务</div>
      </n-card>
    </div>
    <div v-else class="loading"><n-spin size="large" /></div>
  </div>
</template>

<style scoped>
.page { height: 100%; display: flex; flex-direction: column; overflow: hidden; }
.page-head { display: flex; align-items: center; justify-content: space-between; padding: 20px 24px; border-bottom: 1px solid var(--border-color); flex-shrink: 0; }
.page-head h2 { margin: 0; font-size: 20px; }
.page-body { flex: 1; overflow-y: auto; padding: 24px; }
.loading { flex: 1; display: flex; align-items: center; justify-content: center; }
.card { border-radius: 12px; }
.res { display: flex; align-items: center; justify-content: space-between; }
.res-label { font-size: 13px; color: var(--text-secondary); }
.res-val { font-size: 28px; font-weight: 700; margin-top: 4px; }
.summary { background: linear-gradient(135deg, var(--primary-color), #818cf8); }
.sum-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 12px; text-align: center; }
.sum-num { font-size: 24px; font-weight: 700; color: #fff; }
.sum-label { font-size: 12px; color: rgba(255,255,255,0.8); }
.plat-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(160px, 1fr)); gap: 10px; }
.plat { display: flex; align-items: center; gap: 8px; padding: 10px; background: var(--hover-color); border-radius: 8px; }
.plat.connected { border: 1px solid rgba(34,197,94,0.3); }
.plat-icon { font-size: 20px; }
.plat-name { flex: 1; font-size: 13px; font-weight: 500; }
.model-row { display: flex; align-items: center; justify-content: space-between; padding: 8px 0; border-bottom: 1px solid var(--border-color); }
.model-row:last-child { border-bottom: none; }
.model-row span:first-child { color: var(--text-secondary); font-size: 13px; }
.job-list { display: flex; flex-direction: column; gap: 10px; }
.job { display: flex; align-items: center; justify-content: space-between; padding: 12px; background: var(--hover-color); border-radius: 8px; }
.job-name { font-weight: 600; font-size: 14px; }
.job-schedule { font-size: 12px; color: var(--text-secondary); margin-top: 2px; }
.empty { text-align: center; padding: 24px; color: var(--text-secondary); }
</style>