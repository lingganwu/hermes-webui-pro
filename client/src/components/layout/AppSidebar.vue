<script setup lang="ts">
import { computed } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { NMenu } from 'naive-ui'
import type { MenuOption } from 'naive-ui'
import { h } from 'vue'

const router = useRouter()
const route = useRoute()
const activeKey = computed(() => route.name as string)

const menuOptions: MenuOption[] = [
  { label: '仪表盘', key: 'Dashboard', icon: () => h('span', { style: 'font-size:18px' }, '📊') },
  { label: '聊天', key: 'Chat', icon: () => h('span', { style: 'font-size:18px' }, '💬') },
  { label: '记忆', key: 'Memory', icon: () => h('span', { style: 'font-size:18px' }, '🧠') },
  { label: '定时任务', key: 'Jobs', icon: () => h('span', { style: 'font-size:18px' }, '⏰') },
  { label: '模型', key: 'Models', icon: () => h('span', { style: 'font-size:18px' }, '🤖') },
  { label: '技能', key: 'Skills', icon: () => h('span', { style: 'font-size:18px' }, '🛠️') },
  { label: '会话', key: 'Sessions', icon: () => h('span', { style: 'font-size:18px' }, '💬') },
  { label: '统计', key: 'Usage', icon: () => h('span', { style: 'font-size:18px' }, '📈') },
  { label: '日志', key: 'Logs', icon: () => h('span', { style: 'font-size:18px' }, '📋') },
  { label: '网关', key: 'Gateways', icon: () => h('span', { style: 'font-size:18px' }, '🌐') },
  { label: '终端', key: 'Terminal', icon: () => h('span', { style: 'font-size:18px' }, '💻') },
  { label: '设置', key: 'Settings', icon: () => h('span', { style: 'font-size:18px' }, '⚙️') },
]

function handleMenuUpdate(key: string) { router.push({ name: key }) }
function handleLogout() { localStorage.removeItem('hermes_token'); router.push('/login') }
</script>

<template>
  <div class="sidebar">
    <div class="sidebar-header">
      <div class="logo">⚡ HERMES <small>AGENT</small></div>
    </div>
    <div class="sidebar-menu">
      <n-menu :value="activeKey" :options="menuOptions" @update:value="handleMenuUpdate" />
    </div>
    <div class="sidebar-footer">
      <button class="logout-btn" @click="handleLogout">🚪 退出登录</button>
    </div>
  </div>
</template>

<style scoped>
.sidebar {
  width: 220px;
  height: 100vh;
  display: flex;
  flex-direction: column;
  background: var(--sidebar-bg);
  border-right: 1px solid var(--border-color);
}
.sidebar-header {
  padding: 20px 16px;
  border-bottom: 1px solid var(--border-color);
}
.logo {
  font-size: 18px;
  font-weight: 700;
  color: var(--primary-color);
}
.logo small {
  font-size: 10px;
  letter-spacing: 3px;
  color: var(--text-secondary);
  margin-left: 4px;
}
.sidebar-menu {
  flex: 1;
  overflow-y: auto;
  padding: 8px;
}
.sidebar-footer {
  padding: 16px;
  border-top: 1px solid var(--border-color);
}
.logout-btn {
  width: 100%;
  padding: 10px;
  border: none;
  background: transparent;
  color: var(--text-secondary);
  cursor: pointer;
  border-radius: 8px;
  font-size: 14px;
}
.logout-btn:hover {
  background: rgba(239, 68, 68, 0.1);
  color: #ef4444;
}
</style>