import { createApp } from 'vue'
import { createPinia } from 'pinia'
import router from './router'
import App from './App.vue'
import './styles/global.scss'

// Prevent FOUC: apply dark class before mount
const savedTheme = localStorage.getItem('hermes_theme') || 'dark'
const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches
if (savedTheme === 'dark' || (savedTheme === 'system' && prefersDark)) {
  document.documentElement.classList.add('dark')
}

const app = createApp(App)
app.use(createPinia())
app.use(router)
app.mount('#app')
