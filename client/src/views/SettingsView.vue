<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { NCard, NForm, NFormItem, NInput, NSelect, NSwitch, NButton, NSlider, useMessage } from 'naive-ui'
import { fetchConfig, updateConfig, fetchProviders } from '@/api/system'

const message = useMessage()
const loading = ref(true)
const saving = ref(false)
const config = ref<any>({})
const providers = ref<any[]>([])

const form = ref({
  default_model: '',
  default_provider: '',
  base_url: '',
  agent_max_turns: 20,
  gateway_timeout: 1800,
  terminal_timeout: 180,
  compression_enabled: true,
  checkpoints_enabled: true,
})

const providerOptions = ref<any[]>([])

async function loadConfig() {
  try {
    const [cfgRes, provRes] = await Promise.all([fetchConfig(), fetchProviders()])
    config.value = cfgRes.data
    providers.value = provRes.data
    providerOptions.value = provRes.data.map((p: any) => ({ label: p.name, value: p.name }))
    
    form.value.default_model = cfgRes.data.model?.default || ''
    form.value.default_provider = cfgRes.data.model?.provider || ''
    form.value.base_url = cfgRes.data.model?.base_url || ''
    form.value.agent_max_turns = cfgRes.data.agent?.max_turns || 20
    form.value.gateway_timeout = cfgRes.data.agent?.gateway_timeout || 1800
    form.value.terminal_timeout = cfgRes.data.terminal?.timeout || 180
    form.value.compression_enabled = cfgRes.data.compression?.enabled ?? true
    form.value.checkpoints_enabled = cfgRes.data.checkpoints?.enabled ?? true
  } catch { } finally { loading.value = false }
}

async function handleSave() {
  saving.value = true
  try {
    await updateConfig({
      model: { default: form.value.default_model, provider: form.value.default_provider, base_url: form.value.base_url },
      agent: { max_turns: form.value.agent_max_turns, gateway_timeout: form.value.gateway_timeout },
      terminal: { timeout: form.value.terminal_timeout },
      compression: { enabled: form.value.compression_enabled },
      checkpoints: { enabled: form.value.checkpoints_enabled },
    })
    message.success('配置已保存')
  } catch { message.error('保存失败') } finally { saving.value = false }
}

onMounted(loadConfig)
</script>

<template>
  <div class="page-container">
    <div class="page-header">
      <h2>设置</h2>
      <n-button type="primary" :loading="saving" @click="handleSave">保存配置</n-button>
    </div>
    <div class="page-body" v-if="!loading">
      <n-card title="模型配置" class="settings-card">
        <n-form label-placement="left" label-width="120">
          <n-form-item label="Provider">
            <n-select v-model:value="form.default_provider" :options="providerOptions" />
          </n-form-item>
          <n-form-item label="默认模型">
            <n-input v-model:value="form.default_model" />
          </n-form-item>
          <n-form-item label="Base URL">
            <n-input v-model:value="form.base_url" />
          </n-form-item>
        </n-form>
      </n-card>
      <n-card title="Agent 配置" class="settings-card">
        <n-form label-placement="left" label-width="120">
          <n-form-item label="最大轮次">
            <n-slider v-model:value="form.agent_max_turns" :min="1" :max="50" />
          </n-form-item>
          <n-form-item label="网关超时">
            <n-slider v-model:value="form.gateway_timeout" :min="60" :max="3600" :step="60" />
          </n-form-item>
        </n-form>
      </n-card>
      <n-card title="系统配置" class="settings-card">
        <n-form label-placement="left" label-width="120">
          <n-form-item label="启用压缩">
            <n-switch v-model:value="form.compression_enabled" />
          </n-form-item>
          <n-form-item label="启用检查点">
            <n-switch v-model:value="form.checkpoints_enabled" />
          </n-form-item>
        </n-form>
      </n-card>
    </div>
  </div>
</template>

<style scoped>
.page-container { height: 100%; display: flex; flex-direction: column; overflow: hidden; }
.page-header { display: flex; align-items: center; justify-content: space-between; padding: 20px 24px; border-bottom: 1px solid var(--border-color); }
.page-body { flex: 1; overflow-y: auto; padding: 24px; display: flex; flex-direction: column; gap: 16px; }
.settings-card { margin-bottom: 0; }
</style>