<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { NCard, NForm, NFormItem, NInput, NSelect, NSwitch, NButton, NSlider, useMessage } from 'naive-ui'
import { fetchConfig, updateConfig, fetchProviders } from '@/api/system'

const msg = useMessage()
const loading = ref(true)
const saving = ref(false)
const cfg = ref<any>({})
const form = ref({ model: '', provider: '', url: '', turns: 20, timeout: 1800, compression: true, checkpoints: true })
const provOpts = ref<any[]>([])

async function load() {
  try {
    const [c, p] = await Promise.all([fetchConfig(), fetchProviders()])
    cfg.value = c.data; provOpts.value = p.data.map((x: any) => ({ label: x.name, value: x.name }))
    form.value = { model: c.data.model?.default || '', provider: c.data.model?.provider || '', url: c.data.model?.base_url || '', turns: c.data.agent?.max_turns || 20, timeout: c.data.agent?.gateway_timeout || 1800, compression: c.data.compression?.enabled ?? true, checkpoints: c.data.checkpoints?.enabled ?? true }
  } catch {} finally { loading.value = false }
}

async function save() {
  saving.value = true
  try { await updateConfig({ model: { default: form.value.model, provider: form.value.provider, base_url: form.value.url }, agent: { max_turns: form.value.turns, gateway_timeout: form.value.timeout }, compression: { enabled: form.value.compression }, checkpoints: { enabled: form.value.checkpoints } }); msg.success('已保存') }
  catch { msg.error('保存失败') } finally { saving.value = false }
}

onMounted(load)
</script>

<template>
  <div class="page"><div class="head"><h2>⚙️ 设置</h2><n-button type="primary" :loading="saving" @click="save">保存</n-button></div>
    <div class="body" v-if="!loading">
      <n-card title="模型"><n-form label-placement="left" label-width="100">
        <n-form-item label="Provider"><n-select v-model:value="form.provider" :options="provOpts" /></n-form-item>
        <n-form-item label="模型"><n-input v-model:value="form.model" /></n-form-item>
        <n-form-item label="URL"><n-input v-model:value="form.url" /></n-form-item>
      </n-form></n-card>
      <n-card title="Agent" style="margin-top:16px"><n-form label-placement="left" label-width="100">
        <n-form-item label="最大轮次"><n-slider v-model:value="form.turns" :min="1" :max="50" /></n-form-item>
        <n-form-item label="超时(秒)"><n-slider v-model:value="form.timeout" :min="60" :max="3600" :step="60" /></n-form-item>
      </n-form></n-card>
      <n-card title="系统" style="margin-top:16px"><n-form label-placement="left" label-width="100">
        <n-form-item label="压缩"><n-switch v-model:value="form.compression" /></n-form-item>
        <n-form-item label="检查点"><n-switch v-model:value="form.checkpoints" /></n-form-item>
      </n-form></n-card>
    </div>
  </div>
</template>

<style scoped>
.page { height:100%; display:flex; flex-direction:column; overflow:hidden; }
.head { display:flex; align-items:center; justify-content:space-between; padding:20px 24px; border-bottom:1px solid var(--border-color); }
.head h2 { margin:0; font-size:20px; }
.body { flex:1; overflow-y:auto; padding:24px; display:flex; flex-direction:column; gap:0; }
</style>