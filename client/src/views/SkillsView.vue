<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { NList, NListItem, NThing, NTag, NSpin, NEmpty, NInput } from 'naive-ui'
import client from '@/api/client'

const loading = ref(true)
const skills = ref<any[]>([])
const q = ref('')
const filtered = computed(() => q.value ? skills.value.filter(s => s.name.toLowerCase().includes(q.value.toLowerCase())) : skills.value)
async function load() { try { skills.value = (await client.get('/api/skills')).data.skills || [] } catch {} finally { loading.value = false } }
onMounted(load)
</script>

<template>
  <div class="page"><div class="head"><h2>🛠️ 技能</h2><n-tag>{{ skills.length }} 个</n-tag></div>
    <div class="body" v-if="!loading">
      <n-input v-model:value="q" placeholder="搜索..." clearable style="margin-bottom:16px" />
      <n-list hoverable v-if="filtered.length"><n-list-item v-for="s in filtered" :key="s.name">
        <n-thing :title="s.name" :description="s.description || '暂无描述'"><template #header-extra><n-tag size="small" :type="s.enabled?'success':'default'">{{ s.enabled?'启用':'禁用' }}</n-tag></template></n-thing>
      </n-list-item></n-list>
      <n-empty v-else description="暂无技能" />
    </div>
    <div v-else class="loading"><n-spin size="large" /></div>
  </div>
</template>

<style scoped>
.page { height:100%; display:flex; flex-direction:column; overflow:hidden; }
.head { display:flex; align-items:center; justify-content:space-between; padding:20px 24px; border-bottom:1px solid var(--border-color); }
.head h2 { margin:0; font-size:20px; }
.body { flex:1; overflow-y:auto; padding:24px; }
.loading { flex:1; display:flex; align-items:center; justify-content:center; }
</style>