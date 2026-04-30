import { createApp } from 'vue'
import { createPinia } from 'pinia'
import naive from 'naive-ui'
import router from './router'
import App from './App.vue'
import './styles/global.scss'

// 默认暗色主题
const savedTheme = localStorage.getItem('hermes_theme') || 'dark'
localStorage.setItem('hermes_theme', savedTheme)
if (savedTheme === 'dark') {
  document.documentElement.classList.add('dark')
}

const app = createApp(App)
app.use(createPinia())
app.use(router)
app.use(naive)
app.mount('#app')