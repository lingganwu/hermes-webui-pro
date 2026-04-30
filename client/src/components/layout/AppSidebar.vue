<script setup lang="ts">
import { ref, computed } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { NMenu, NButton, NSwitch, NSpace, NTooltip } from 'naive-ui'
import type { MenuOption } from 'naive-ui'

const router = useRouter()
const route = useRoute()

const activeKey = computed(() => route.name as string)
const isDark = ref(localStorage.getItem('hermes_theme') === 'dark')

// SVG 图标组件
const icons = {
  dashboard: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="3" width="7" height="7" rx="1"/><rect x="14" y="3" width="7" height="7" rx="1"/><rect x="3" y="14" width="7" height="7" rx="1"/><rect x="14" y="14" width="7" height="7" rx="1"/></svg>`,
  chat: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/></svg>`,
  memory: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 2a10 10 0 1 0 10 10A10 10 0 0 0 12 2zm0 18a8 8 0 1 1 8-8 8 8 0 0 1-8 8z"/><path d="M12 6v6l4 2"/></svg>`,
  jobs: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg>`,
  models: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 2L2 7l10 5 10-5-10-5z"/><path d="M2 17l10 5 10-5"/><path d="M2 12l10 5 10-5"/></svg>`,
  skills: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M14.7 6.3a1 1 0 0 0 0 1.4l1.6 1.6a1 1 0 0 0 1.4 0l3.77-3.77a6 6 0 0 1-7.94 7.94l-6.91 6.91a2.12 2.12 0 0 1-3-3l6.91-6.91a6 6 0 0 1 7.94-7.94l-3.76 3.76z"/></svg>`,
  sessions: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M23 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/></svg>`,
  usage: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="18" y1="20" x2="18" y2="10"/><line x1="12" y1="20" x2="12" y2="4"/><line x1="6" y1="20" x2="6" y2="14"/></svg>`,
  logs: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/><line x1="16" y1="13" x2="8" y2="13"/><line x1="16" y1="17" x2="8" y2="17"/><polyline points="10 9 9 9 8 9"/></svg>`,
  gateways: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="2" y="2" width="20" height="8" rx="2" ry="2"/><rect x="2" y="14" width="20" height="8" rx="2" ry="2"/><line x1="6" y1="6" x2="6.01" y2="6"/><line x1="6" y1="18" x2="6.01" y2="18"/></svg>`,
  terminal: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="4 17 10 11 4 5"/><line x1="12" y1="19" x2="20" y2="19"/></svg>`,
  settings: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="3"/><path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1 0 2.83 2 2 0 0 1-2.83 0l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-2 2 2 2 0 0 1-2-2v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 0 1-2.83 0 2 2 0 0 1 0-2.83l.06-.06A1.65 1.65 0 0 0 4.68 15a1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1-2-2 2 2 0 0 1 2-2h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 0 1 0-2.83 2 2 0 0 1 2.83 0l.06.06A1.65 1.65 0 0 0 9 4.68a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 2-2 2 2 0 0 1 2 2v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 0 1 2.83 0 2 2 0 0 1 0 2.83l-.06.06a1.65 1.65 0 0 0-.33 1.82V9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 2 2 2 2 0 0 1-2 2h-.09a1.65 1.65 0 0 0-1.51 1z"/></svg>`,
  logout: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4"/><polyline points="16 17 21 12 16 7"/><line x1="21" y1="12" x2="9" y2="12"/></svg>`,
  sun: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="5"/><line x1="12" y1="1" x2="12" y2="3"/><line x1="12" y1="21" x2="12" y2="23"/><line x1="4.22" y1="4.22" x2="5.64" y2="5.64"/><line x1="18.36" y1="18.36" x2="19.78" y2="19.78"/><line x1="1" y1="12" x2="3" y2="12"/><line x1="21" y1="12" x2="23" y2="12"/><line x1="4.22" y1="19.78" x2="5.64" y2="18.36"/><line x1="18.36" y1="5.64" x2="19.78" y2="4.22"/></svg>`,
  moon: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"/></svg>`,
}

function renderIcon(name: string) {
  return `<span class="nav-icon">${icons[name] || ''}</span>`
}

const menuOptions: MenuOption[] = [
  { label: '仪表盘', key: 'Dashboard', icon: () => h('span', { innerHTML: icons.dashboard }) },
  { label: '聊天', key: 'Chat', icon: () => h('span', { innerHTML: icons.chat }) },
  { label: '记忆', key: 'Memory', icon: () => h('span', { innerHTML: icons.memory }) },
  { label: '定时任务', key: 'Jobs', icon: () => h('span', { innerHTML: icons.jobs }) },
  { label: '模型', key: 'Models', icon: () => h('span', { innerHTML: icons.models }) },
  { label: '技能', key: 'Skills', icon: () => h('span', { innerHTML: icons.skills }) },
  { label: '会话', key: 'Sessions', icon: () => h('span', { innerHTML: icons.sessions }) },
  { label: '统计', key: 'Usage', icon: () => h('span', { innerHTML: icons.usage }) },
  { label: '日志', key: 'Logs', icon: () => h('span', { innerHTML: icons.logs }) },
  { label: '网关', key: 'Gateways', icon: () => h('span', { innerHTML: icons.gateways }) },
  { label: '终端', key: 'Terminal', icon: () => h('span', { innerHTML: icons.terminal }) },
  { label: '设置', key: 'Settings', icon: () => h('span', { innerHTML: icons.settings }) },
]

function handleMenuUpdate(key: string) {
  router.push({ name: key })
}

function toggleTheme() {
  isDark.value = !isDark.value
  localStorage.setItem('hermes_theme', isDark.value ? 'dark' : 'light')
  document.documentElement.classList.toggle('dark', isDark.value)
}

function handleLogout() {
  localStorage.removeItem('hermes_token')
  router.push('/login')
}

import { h } from 'vue'
</script>

<template>
  <div class="sidebar">
    <!-- Logo -->
    <div class="sidebar-header">
      <div class="logo-container">
        <div class="logo-icon">
          <svg viewBox="0 0 32 32" fill="none">
            <path d="M16 2L2 9l14 7 14-7-14-7z" fill="currentColor" opacity="0.3"/>
            <path d="M16 2L2 9l14 7 14-7-14-7z" stroke="currentColor" stroke-width="1.5" fill="none"/>
            <path d="M2 23l14 7 14-7" stroke="currentColor" stroke-width="1.5" fill="none"/>
            <path d="M2 16l14 7 14-7" stroke="currentColor" stroke-width="1.5" fill="none"/>
          </svg>
        </div>
        <div class="logo-text">
          <span class="logo-title">HERMES</span>
          <span class="logo-subtitle">AGENT</span>
        </div>
      </div>
    </div>

    <!-- 导航菜单 -->
    <div class="sidebar-menu">
      <n-menu 
        :value="activeKey" 
        :options="menuOptions" 
        @update:value="handleMenuUpdate"
        :collapsed="false"
        :collapsed-width="64"
        :indent="24"
      />
    </div>

    <!-- 底部操作 -->
    <div class="sidebar-footer">
      <div class="footer-actions">
        <n-tooltip trigger="hover">
          <template #trigger>
            <button class="icon-btn" @click="toggleTheme">
              <span v-html="isDark ? icons.sun : icons.moon"></span>
            </button>
          </template>
          {{ isDark ? '切换亮色' : '切换暗色' }}
        </n-tooltip>
        <n-tooltip trigger="hover">
          <template #trigger>
            <button class="icon-btn logout" @click="handleLogout">
              <span v-html="icons.logout"></span>
            </button>
          </template>
          退出登录
        </n-tooltip>
      </div>
    </div>
  </div>
</template>

<style scoped lang="scss">
.sidebar {
  width: 240px;
  height: 100vh;
  display: flex;
  flex-direction: column;
  background: var(--sidebar-bg);
  border-right: 1px solid var(--border-color);
  transition: all 0.3s ease;
}

.sidebar-header {
  padding: 20px 16px;
  border-bottom: 1px solid var(--border-color);
}

.logo-container {
  display: flex;
  align-items: center;
  gap: 12px;
}

.logo-icon {
  width: 36px;
  height: 36px;
  color: var(--primary-color);
  
  svg {
    width: 100%;
    height: 100%;
  }
}

.logo-text {
  display: flex;
  flex-direction: column;
}

.logo-title {
  font-size: 18px;
  font-weight: 700;
  letter-spacing: 2px;
  color: var(--text-primary);
}

.logo-subtitle {
  font-size: 10px;
  letter-spacing: 4px;
  color: var(--text-secondary);
  margin-top: -2px;
}

.sidebar-menu {
  flex: 1;
  overflow-y: auto;
  padding: 8px 0;
  
  :deep(.n-menu) {
    --n-item-height: 44px;
    --n-item-icon-size: 20px;
  }
  
  :deep(.n-menu-item) {
    margin: 2px 8px;
    border-radius: 8px;
  }
  
  :deep(.n-menu-item-content) {
    padding-left: 16px !important;
  }
}

.sidebar-footer {
  padding: 16px;
  border-top: 1px solid var(--border-color);
}

.footer-actions {
  display: flex;
  align-items: center;
  justify-content: space-around;
}

.icon-btn {
  width: 36px;
  height: 36px;
  display: flex;
  align-items: center;
  justify-content: center;
  border: none;
  background: transparent;
  color: var(--text-secondary);
  cursor: pointer;
  border-radius: 8px;
  transition: all 0.2s;
  
  &:hover {
    background: var(--hover-color);
    color: var(--text-primary);
  }
  
  &.logout:hover {
    color: #ef4444;
  }
  
  span {
    width: 20px;
    height: 20px;
    display: flex;
    
    :deep(svg) {
      width: 100%;
      height: 100%;
    }
  }
}

.nav-icon {
  width: 20px;
  height: 20px;
  display: inline-flex;
  
  :deep(svg) {
    width: 100%;
    height: 100%;
  }
}
</style>