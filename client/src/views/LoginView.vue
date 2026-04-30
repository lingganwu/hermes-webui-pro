<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { NCard, NInput, NButton, NIcon, useMessage } from 'naive-ui'
import { useAuthStore } from '@/stores/auth'

const router = useRouter()
const authStore = useAuthStore()
const message = useMessage()
const password = ref('')
const loading = ref(false)

async function handleLogin() {
  if (!password.value.trim()) return
  loading.value = true
  try {
    await authStore.login(password.value)
    router.replace('/dashboard')
  } catch (e: any) {
    message.error(e.response?.data?.detail || '密码错误')
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <div class="login-page">
    <div class="login-bg">
      <div class="login-orb orb-1"></div>
      <div class="login-orb orb-2"></div>
      <div class="login-orb orb-3"></div>
    </div>
    <n-card class="login-card" :bordered="false">
      <div class="login-header">
        <div class="login-logo">⚡</div>
        <h1>Hermes WebUI</h1>
        <p class="login-subtitle">AI Agent Control Center</p>
      </div>
      <form @submit.prevent="handleLogin" class="login-form">
        <n-input
          v-model:value="password"
          type="password"
          show-password-on="click"
          placeholder="输入访问密码"
          size="large"
          :disabled="loading"
          @keyup.enter="handleLogin"
        />
        <n-button
          type="primary"
          block
          size="large"
          :loading="loading"
          :disabled="!password.trim()"
          @click="handleLogin"
        >
          登录
        </n-button>
      </form>
    </n-card>
  </div>
</template>

<style scoped lang="scss">
.login-page {
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: 100vh;
  background: var(--bg-body);
  position: relative;
  overflow: hidden;
}

.login-bg {
  position: absolute;
  inset: 0;
  overflow: hidden;
}

.login-orb {
  position: absolute;
  border-radius: 50%;
  filter: blur(80px);
  opacity: 0.15;
  animation: float 20s infinite ease-in-out;
}
.orb-1 { width: 400px; height: 400px; background: #6366f1; top: -100px; left: -100px; }
.orb-2 { width: 300px; height: 300px; background: #8b5cf6; bottom: -80px; right: -80px; animation-delay: -7s; }
.orb-3 { width: 250px; height: 250px; background: #06b6d4; top: 50%; left: 60%; animation-delay: -14s; }

@keyframes float {
  0%, 100% { transform: translate(0, 0) scale(1); }
  33% { transform: translate(30px, -30px) scale(1.05); }
  66% { transform: translate(-20px, 20px) scale(0.95); }
}

.login-card {
  width: 400px;
  max-width: 90vw;
  position: relative;
  z-index: 1;
  backdrop-filter: blur(20px);
  background: rgba(255, 255, 255, 0.05) !important;
  border: 1px solid rgba(255, 255, 255, 0.1) !important;
  border-radius: 16px !important;
  padding: 20px 0;
}

.login-header {
  text-align: center;
  margin-bottom: 32px;

  .login-logo {
    font-size: 48px;
    margin-bottom: 12px;
  }

  h1 {
    font-size: 24px;
    font-weight: 700;
    color: var(--text-primary);
    margin: 0;
  }

  .login-subtitle {
    color: var(--text-secondary);
    margin-top: 4px;
    font-size: 14px;
  }
}

.login-form {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

:deep(.n-card__content) {
  padding: 40px 32px 32px;
}
</style>
