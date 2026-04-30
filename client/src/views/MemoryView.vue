<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { NCard, NButton, NInput, NTag, NEmpty, NSpin, NModal, useMessage, NCollapse, NCollapseItem } from 'naive-ui'
import { fetchMemory, updateMemory, deleteMemory } from '@/api/memory'

const message = useMessage()
const loading = ref(true)
const memories = ref<any[]>([])
const editing = ref<any>(null)
const editContent = ref('')
const showAdd = ref(false)
const newContent = ref('')
const searchQuery = ref('')

async function loadMemories() {
  loading.value = true
  try {
    const { data } = await fetchMemory()
    memories.value = data.entries || []
  } catch { message.error('加载记忆失败') }
  finally { loading.value = false }
}

function startEdit(entry: any) {
  editing.value = entry
  editContent.value = entry.content
}

async function saveEdit() {
  if (!editing.value) return
  try {
    await updateMemory(editing.value.id, editContent.value)
    message.success('已保存')
    editing.value = null
    await loadMemories()
  } catch { message.error('保存失败') }
}

async function handleDelete(id: string) {
  try {
    await deleteMemory(id)
    message.success('已删除')
    await loadMemories()
  } catch { message.error('删除失败') }
}

async function addMemory() {
  if (!newContent.value.trim()) return
  try {
    await updateMemory(null, newContent.value)
    message.success('已添加')
    showAdd.value = false
    newContent.value = ''
    await loadMemories()
  } catch { message.error('添加失败') }
}

const filtered = () => {
  if (!searchQuery.value.trim()) return memories.value
  const q = searchQuery.value.toLowerCase()
  return memories.value.filter(m => m.content.toLowerCase().includes(q))
}

onMounted(loadMemories)
</script>

<template>
  <div class="page-container">
    <div class="page-header">
      <h2>🧠 记忆管理</h2>
      <div style="display:flex;gap:8px;align-items:center">
        <n-input v-model:value="searchQuery" placeholder="搜索记忆..." size="small" clearable style="width:200px" />
        <n-button type="primary" size="small" @click="showAdd = true">+ 添加记忆</n-button>
      </div>
    </div>
    <div class="page-body">
      <n-spin :show="loading">
        <div class="memory-grid" v-if="filtered().length">
          <n-card v-for="mem in filtered()" :key="mem.id" size="small" class="memory-card">
            <div class="memory-content">{{ mem.content }}</div>
            <div class="memory-meta">
              <n-tag size="tiny" type="info">{{ mem.source || 'manual' }}</n-tag>
              <div class="memory-actions">
                <n-button text size="small" @click="startEdit(mem)">编辑</n-button>
                <n-button text size="small" type="error" @click="handleDelete(mem.id)">删除</n-button>
              </div>
            </div>
          </n-card>
        </div>
        <n-empty v-else description="暂无记忆条目" />
      </n-spin>
    </div>

    <!-- Edit modal -->
    <n-modal v-model:show="editing" preset="card" title="编辑记忆" style="max-width:600px">
      <n-input v-model:value="editContent" type="textarea" :rows="6" />
      <template #footer>
        <div style="display:flex;gap:8px;justify-content:flex-end">
          <n-button @click="editing = null">取消</n-button>
          <n-button type="primary" @click="saveEdit">保存</n-button>
        </div>
      </template>
    </n-modal>

    <!-- Add modal -->
    <n-modal v-model:show="showAdd" preset="card" title="添加记忆" style="max-width:600px">
      <n-input v-model:value="newContent" type="textarea" :rows="4" placeholder="输入新的记忆内容..." />
      <template #footer>
        <div style="display:flex;gap:8px;justify-content:flex-end">
          <n-button @click="showAdd = false">取消</n-button>
          <n-button type="primary" @click="addMemory">添加</n-button>
        </div>
      </template>
    </n-modal>
  </div>
</template>

<style scoped lang="scss">
.page-container { height: 100%; display: flex; flex-direction: column; overflow: hidden; }
.page-header { display: flex; align-items: center; justify-content: space-between; padding: 20px 24px; border-bottom: 1px solid var(--border-color); flex-shrink: 0; h2 { margin: 0; font-size: 18px; } }
.page-body { flex: 1; overflow-y: auto; padding: 24px; }
.memory-grid { display: flex; flex-direction: column; gap: 12px; }
.memory-card { transition: transform 0.15s; &:hover { transform: translateY(-1px); } }
.memory-content { font-size: 14px; line-height: 1.6; white-space: pre-wrap; }
.memory-meta { display: flex; align-items: center; justify-content: space-between; margin-top: 10px; }
.memory-actions { display: flex; gap: 4px; }
</style>
