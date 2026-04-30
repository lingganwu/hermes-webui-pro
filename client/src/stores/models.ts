import { defineStore } from 'pinia'
import { ref } from 'vue'

export const useModelsStore = defineStore('models', () => {
  const models = ref<any[]>([])
  const loading = ref(false)
  return { models, loading }
})
