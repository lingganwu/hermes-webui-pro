<script setup lang="ts">
import { ref } from 'vue'
import { NCard, NInput, NButton, NSpace, useMessage } from 'naive-ui'
import { useRouter } from 'vue-router'
import client from '@/api/client'

const router = useRouter()
const message = useMessage()
const password = ref('')
const loading = ref(false)

async function handleLogin() {
  if (!password.value) { message.warning('请输入密码'); return }
  loading.value = true
  try {
    const res = await client.post('/api/auth/login', { password: password.value })
    localStorage.setItem('hermes_token', res.data.token)
    message.success('登录成功')
    router.push('/')
  } catch (e: any) {
    message.error(e.response?.data?.detail || '密码错误')
  } finally { loading.value = false }
}
</script>

<template>
  <div class="login-page">
    <n-card class="login-card" title="⚡ Hermes WebUI Pro">
      <n-space vertical :size="16">
        <n-input v-model:value="password" type="password" show-password-on="click" placeholder="请输入登录密码" @keyup.enter="handleLogin" size="large" />
        <n-button type="primary" block :loading="loading" @click="handleLogin" size="large">登录</n-button>
      </n-space>
    </n-card>
  </div>
</template>

<style scoped>
.login-page { height: 100vh; display: flex; align-items: center; justify-content: center; background: var(--body-color); }
.login-card { width: 380px; }
</style>