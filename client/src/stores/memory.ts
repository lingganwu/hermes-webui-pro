import { defineStore } from 'pinia'
import { ref } from 'vue'

export const useMemoryStore = defineStore('memory', () => {
  const entries = ref<any[]>([])
  const loading = ref(false)

  return { entries, loading }
})
