import { createApp } from 'vue'
import { createPinia } from 'pinia'
import naive from 'naive-ui'
import router from './router'
import App from './App.vue'
import './styles/global.scss'

if (localStorage.getItem('hermes_theme') !== 'light') {
  document.documentElement.classList.add('dark')
}

createApp(App).use(createPinia()).use(router).use(naive).mount('#app')
