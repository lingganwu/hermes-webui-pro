import { ref, watch, onMounted } from 'vue'
import { useOsTheme } from 'naive-ui'

type ThemeMode = 'light' | 'dark' | 'system'

const themeMode = ref<ThemeMode>((localStorage.getItem('hermes_theme') as ThemeMode) || 'dark')
const isDark = ref(true)

export function useTheme() {
  const osTheme = useOsTheme()

  function applyTheme() {
    const dark = themeMode.value === 'dark' || (themeMode.value === 'system' && osTheme.value === 'dark')
    isDark.value = dark
    if (dark) {
      document.documentElement.classList.add('dark')
    } else {
      document.documentElement.classList.remove('dark')
    }
    // Update CSS variables for bg/text colors
    document.documentElement.style.setProperty('--bg-body', dark ? '#0a0a0a' : '#ffffff')
    document.documentElement.style.setProperty('--bg-sidebar', dark ? '#111111' : '#f8f8f8')
    document.documentElement.style.setProperty('--bg-card', dark ? '#1a1a1a' : '#ffffff')
    document.documentElement.style.setProperty('--text-primary', dark ? '#e5e5e5' : '#1a1a1a')
    document.documentElement.style.setProperty('--text-secondary', dark ? '#a3a3a3' : '#666666')
    document.documentElement.style.setProperty('--border-color', dark ? '#2a2a2a' : '#e5e5e5')
    document.documentElement.style.setProperty('--hover-color', dark ? 'rgba(255,255,255,0.06)' : 'rgba(0,0,0,0.04)')
    document.documentElement.style.setProperty('--card-color', dark ? '#1a1a1a' : '#ffffff')
  }

  function setTheme(mode: ThemeMode) {
    themeMode.value = mode
    localStorage.setItem('hermes_theme', mode)
    applyTheme()
  }

  function toggleTheme() {
    setTheme(isDark.value ? 'light' : 'dark')
  }

  watch(osTheme, applyTheme)
  onMounted(applyTheme)

  return {
    themeMode,
    isDark,
    setTheme,
    toggleTheme,
  }
}
