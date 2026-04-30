import { defineStore } from 'pinia'
import { ref } from 'vue'

export const useSkillsStore = defineStore('skills', () => {
  const skills = ref<any[]>([])
  const loading = ref(false)
  return { skills, loading }
})
