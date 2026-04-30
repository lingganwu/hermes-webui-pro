<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { NCard, NInput, NButton, NSwitch, NSelect, NDivider, useMessage, NFormItem, NForm } from 'naive-ui'
import { useAppStore } from '@/stores/app'
import { useTheme } from '@/composables/useTheme'

const appStore = useAppStore()
const { isDark, toggleTheme } = useTheme()
const message = useMessage()
const config = ref<any>({})
const loading = ref(true)

async function loadConfig() {
  loading.value = true
  try {
    const { data } = await (await import('@/api/system')).fetchConfig()
    config.value = data
  } catch { } finally { loading.value = false }
}

async function saveConfig() {
  try {
    await (await import('@/api/system')).updateConfig(config.value)
    message.success('配置已保存')
  } catch { message.error('保存失败') }
}

onMounted(loadConfig)
</script>

<template>
  <div class="page-container">
    <div class="page-header">
      <h2>⚙️ 设置</h2>
      <n-button type="primary" size="small" @click="saveConfig">保存</n-button>
    </div>
    <div class="page-body">
      <n-card title="外观" size="small" style="margin-bottom:16px">
        <div class="setting-row">
          <span>深色模式</span>
          <n-switch :value="isDark" @update:value="toggleTheme" />
        </div>
      </n-card>

      <n-card title="默认模型" size="small" style="margin-bottom:16px">
        <div class="setting-row">
          <span>默认模型</span>
          <n-select v-model:value="config.defaultModel" :options="(appStore.models || []).map((m:string) => ({label:m, value:m}))" placeholder="选择默认模型" style="width:260px" />
        </div>
        <div class="setting-row">
          <span>默认 Provider</span>
          <n-input v-model:value="config.defaultProvider" placeholder="openrouter" size="small" style="width:260px" />
        </div>
      </n-card>

      <n-card title="安全" size="small" style="margin-bottom:16px">
        <div class="setting-row">
          <span>修改访问密码</span>
          <n-input v-model:value="config.newPassword" type="password" show-password-on="click" placeholder="留空不修改" size="small" style="width:260px" />
        </div>
      </n-card>

      <n-card title="高级" size="small">
        <div class="setting-row">
          <span>Max Tokens</span>
          <n-input v-model:value="config.maxTokens" size="small" style="width:140px" />
        </div>
        <div class="setting-row">
          <span>Stream 模式</span>
          <n-switch v-model:value="config.streamEnabled" />
        </div>
      </n-card>
    </div>
  </div>
</template>

<style scoped lang="scss">
.page-container { height: 100%; display: flex; flex-direction: column; overflow: hidden; }
.page-header { display: flex; align-items: center; justify-content: space-between; padding: 20px 24px; border-bottom: 1px solid var(--border-color); flex-shrink: 0; h2 { margin: 0; font-size: 18px; } }
.page-body { flex: 1; overflow-y: auto; padding: 24px; }
.setting-row { display: flex; align-items: center; justify-content: space-between; padding: 10px 0; border-bottom: 1px solid var(--border-color); &:last-child { border-bottom: none; } span { font-size: 14px; } }
</style>
