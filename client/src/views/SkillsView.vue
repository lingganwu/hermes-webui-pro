<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { NCard, NInput, NTag, NGrid, NGi, NEmpty, NSpin, NCollapse, NCollapseItem } from 'naive-ui'
import { fetchSkills } from '@/api/skills'

const loading = ref(true)
const skills = ref<any[]>([])
const search = ref('')

async function loadSkills() {
  loading.value = true
  try { const { data } = await fetchSkills(); skills.value = data.skills || [] }
  catch { } finally { loading.value = false }
}

const filtered = computed(() => {
  if (!search.value.trim()) return skills.value
  const q = search.value.toLowerCase()
  return skills.value.filter(s => s.name.toLowerCase().includes(q) || s.description?.toLowerCase().includes(q))
})

onMounted(loadSkills)
</script>

<template>
  <div class="page-container">
    <div class="page-header">
      <h2>🛠 Skills</h2>
      <n-input v-model:value="search" placeholder="搜索技能..." size="small" clearable style="width:240px" />
    </div>
    <div class="page-body">
      <n-spin :show="loading">
        <n-grid :cols="2" :x-gap="12" :y-gap="12" responsive="screen" item-responsive v-if="filtered.length">
          <n-gi span="2 m:1" v-for="skill in filtered" :key="skill.name">
            <n-card size="small" class="skill-card">
              <div class="skill-name">{{ skill.name }}</div>
              <div class="skill-desc">{{ skill.description || '无描述' }}</div>
              <div class="skill-tags" v-if="skill.tags?.length">
                <n-tag v-for="tag in skill.tags" :key="tag" size="tiny" type="info">{{ tag }}</n-tag>
              </div>
            </n-card>
          </n-gi>
        </n-grid>
        <n-empty v-else description="暂无技能" />
      </n-spin>
    </div>
  </div>
</template>

<style scoped lang="scss">
.page-container { height: 100%; display: flex; flex-direction: column; overflow: hidden; }
.page-header { display: flex; align-items: center; justify-content: space-between; padding: 20px 24px; border-bottom: 1px solid var(--border-color); flex-shrink: 0; h2 { margin: 0; font-size: 18px; } }
.page-body { flex: 1; overflow-y: auto; padding: 24px; }
.skill-card { transition: transform 0.15s; &:hover { transform: translateY(-2px); } }
.skill-name { font-weight: 600; font-size: 14px; margin-bottom: 6px; }
.skill-desc { font-size: 12px; color: var(--text-secondary); line-height: 1.5; margin-bottom: 8px; }
.skill-tags { display: flex; flex-wrap: wrap; gap: 4px; }
</style>
