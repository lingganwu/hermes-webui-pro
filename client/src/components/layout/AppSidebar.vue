<script setup lang="ts">
import { computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { NIcon, NButton, NTooltip } from 'naive-ui'
import { useTheme } from '@/composables/useTheme'
import { useAuthStore } from '@/stores/auth'

const route = useRoute()
const router = useRouter()
const { isDark, toggleTheme } = useTheme()
const authStore = useAuthStore()
const activeRoute = computed(() => route.name as string)

const navItems = [
  { name: 'dashboard', label: 'Dashboard', icon: '📊' },
  { name: 'chat', label: 'Chat', icon: '💬' },
  { name: 'memory', label: 'Memory', icon: '🧠' },
  { name: 'divider1', label: '', icon: '' },
  { name: 'jobs', label: 'Jobs', icon: '⏰' },
  { name: 'models', label: 'Models', icon: '🤖' },
  { name: 'skills', label: 'Skills', icon: '🛠' },
  { name: 'divider2', label: '', icon: '' },
  { name: 'usage', label: 'Usage', icon: '📈' },
  { name: 'logs', label: 'Logs', icon: '📋' },
  { name: 'gateways', label: 'Gateways', icon: '🌐' },
  { name: 'terminal', label: 'Terminal', icon: '💻' },
  { name: 'divider3', label: '', icon: '' },
  { name: 'settings', label: 'Settings', icon: '⚙️' },
]

function go(name: string) { router.push({ name }) }

function handleLogout() {
  authStore.logout()
  router.replace({ name: 'login' })
}
</script>

<template>
  <aside class="sidebar">
    <div class="sidebar-logo" @click="go('chat')">
      <div class="logo-icon">⚡</div>
      <span class="logo-text">Hermes</span>
    </div>

    <nav class="sidebar-nav">
      <template v-for="item in navItems" :key="item.name">
        <div v-if="item.name.startsWith('divider')" class="nav-divider"></div>
        <button v-else class="nav-item" :class="{ active: activeRoute === item.name }" @click="go(item.name)">
          <span class="nav-icon">{{ item.icon }}</span>
          <span class="nav-label">{{ item.label }}</span>
        </button>
      </template>
    </nav>

    <div class="sidebar-footer">
      <button class="nav-item" @click="toggleTheme">
        <span class="nav-icon">{{ isDark ? '☀️' : '🌙' }}</span>
        <span class="nav-label">{{ isDark ? 'Light' : 'Dark' }}</span>
      </button>
      <button class="nav-item logout" @click="handleLogout">
        <span class="nav-icon">🚪</span>
        <span class="nav-label">退出</span>
      </button>
    </div>
  </aside>
</template>

<style scoped lang="scss">
.sidebar {
  width: $sidebar-width;
  height: 100%;
  display: flex;
  flex-direction: column;
  background: var(--bg-sidebar);
  border-right: 1px solid var(--border-color);
  flex-shrink: 0;
  overflow: hidden;
}

.sidebar-logo {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 20px 16px;
  cursor: pointer;
  border-bottom: 1px solid var(--border-color);

  .logo-icon {
    font-size: 28px;
    line-height: 1;
  }

  .logo-text {
    font-size: 18px;
    font-weight: 700;
    background: $gradient-primary;
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
  }
}

.sidebar-nav {
  flex: 1;
  overflow-y: auto;
  padding: 8px;
}

.nav-divider {
  height: 1px;
  background: var(--border-color);
  margin: 6px 8px;
}

.nav-item {
  display: flex;
  align-items: center;
  gap: 10px;
  width: 100%;
  padding: 9px 12px;
  border: none;
  background: transparent;
  color: var(--text-secondary);
  font-size: 13px;
  cursor: pointer;
  border-radius: $border-radius;
  transition: all $transition-fast;

  &:hover {
    background: var(--hover-color);
    color: var(--text-primary);
  }

  &.active {
    background: rgba(99, 102, 241, 0.15);
    color: #6366f1;
    font-weight: 600;
  }

  .nav-icon {
    font-size: 16px;
    width: 22px;
    text-align: center;
  }

  .nav-label {
    flex: 1;
    text-align: left;
  }
}

.sidebar-footer {
  padding: 8px;
  border-top: 1px solid var(--border-color);

  .logout {
    color: var(--color-error);

    &:hover {
      background: rgba(239, 68, 68, 0.1);
    }
  }
}
</style>
