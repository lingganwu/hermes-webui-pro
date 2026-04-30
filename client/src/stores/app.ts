import { defineStore } from 'pinia'
import { ref } from 'vue'

export const useAppStore = defineStore('app', () => {
  const sidebarCollapsed = ref(false)
  const connected = ref(false)
  const version = ref('2.0.0')
  const selectedModel = ref(localStorage.getItem('hermes_selected_model') || '')
  const models = ref<string[]>([])

  function toggleSidebar() {
    sidebarCollapsed.value = !sidebarCollapsed.value
  }

  function setModel(model: string) {
    selectedModel.value = model
    localStorage.setItem('hermes_selected_model', model)
  }

  return { sidebarCollapsed, connected, version, selectedModel, models, toggleSidebar, setModel }
})
