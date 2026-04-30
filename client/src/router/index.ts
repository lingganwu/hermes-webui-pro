import { createRouter, createWebHashHistory } from 'vue-router'

const routes = [
  { path: '/login', name: 'Login', component: () => import('@/views/LoginView.vue') },
  { path: '/', name: 'Dashboard', component: () => import('@/views/DashboardView.vue') },
  { path: '/chat', name: 'Chat', component: () => import('@/views/ChatView.vue') },
  { path: '/memory', name: 'Memory', component: () => import('@/views/MemoryView.vue') },
  { path: '/jobs', name: 'Jobs', component: () => import('@/views/JobsView.vue') },
  { path: '/models', name: 'Models', component: () => import('@/views/ModelsView.vue') },
  { path: '/skills', name: 'Skills', component: () => import('@/views/SkillsView.vue') },
  { path: '/sessions', name: 'Sessions', component: () => import('@/views/SessionsView.vue') },
  { path: '/usage', name: 'Usage', component: () => import('@/views/UsageView.vue') },
  { path: '/logs', name: 'Logs', component: () => import('@/views/LogsView.vue') },
  { path: '/gateways', name: 'Gateways', component: () => import('@/views/GatewaysView.vue') },
  { path: '/terminal', name: 'Terminal', component: () => import('@/views/TerminalView.vue') },
  { path: '/settings', name: 'Settings', component: () => import('@/views/SettingsView.vue') },
]

const router = createRouter({
  history: createWebHashHistory(),
  routes,
})

router.beforeEach((to, from, next) => {
  const token = localStorage.getItem('hermes_token')
  if (to.name !== 'Login' && !token) {
    next({ name: 'Login' })
  } else {
    next()
  }
})

export default router