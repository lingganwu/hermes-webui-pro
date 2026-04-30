import { ref } from 'vue'

const isDark = ref(localStorage.getItem('hermes_theme') === 'dark')

export function useTheme() {
  function toggle() {
    isDark.value = !isDark.value
    localStorage.setItem('hermes_theme', isDark.value ? 'dark' : 'light')
    document.documentElement.classList.toggle('dark', isDark.value)
  }

  return { isDark, toggle }
}