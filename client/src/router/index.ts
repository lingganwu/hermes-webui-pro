import { createRouter, createWebHashHistory } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const router = createRouter({
  history: createWebHashHistory(),
  routes: [
    {
      path: '/',
      name: 'login',
      component: () => import('@/views/LoginView.vue'),
      meta: { public: true },
    },
    {
      path: '/dashboard',
      name: 'dashboard',
      component: () => import('@/views/DashboardView.vue'),
    },
    {
      path: '/chat',
      name: 'chat',
      component: () => import('@/views/ChatView.vue'),
    },
    {
      path: '/memory',
      name: 'memory',
      component: () => import('@/views/MemoryView.vue'),
    },
    {
      path: '/jobs',
      name: 'jobs',
      component: () => import('@/views/JobsView.vue'),
    },
    {
      path: '/models',
      name: 'models',
      component: () => import('@/views/ModelsView.vue'),
    },
    {
      path: '/skills',
      name: 'skills',
      component: () => import('@/views/SkillsView.vue'),
    },
    {
      path: '/settings',
      name: 'settings',
      component: () => import('@/views/SettingsView.vue'),
    },
    {
      path: '/terminal',
      name: 'terminal',
      component: () => import('@/views/TerminalView.vue'),
    },
    {
      path: '/usage',
      name: 'usage',
      component: () => import('@/views/UsageView.vue'),
    },
    {
      path: '/logs',
      name: 'logs',
      component: () => import('@/views/LogsView.vue'),
    },
    {
      path: '/gateways',
      name: 'gateways',
      component: () => import('@/views/GatewaysView.vue'),
    },
  ],
})

router.beforeEach((to) => {
  if (to.meta.public) return true
  const authStore = useAuthStore()
  if (!authStore.isAuthenticated) {
    return { name: 'login' }
  }
})

export default router
