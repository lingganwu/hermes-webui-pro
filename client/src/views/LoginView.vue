<script setup lang="ts">
import { ref } from 'vue'
import { NCard, NInput, NButton, NSpace, NIcon, useMessage } from 'naive-ui'
import { useRouter } from 'vue-router'
import client from '@/api/client'

const router = useRouter()
const message = useMessage()
const password = ref('')
const loading = ref(false)

async function handleLogin() {
  if (!password.value) {
    message.warning('请输入密码')
    return
  }
  loading.value = true
  try {
    const res = await client.post('/api/auth/login', { password: password.value })
    localStorage.setItem('hermes_token', res.data.token)
    message.success('登录成功')
    router.push('/')
  } catch (e: any) {
    message.error(e.response?.data?.detail || '密码错误')
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <div class="login-page">
    <!-- 背景装饰 -->
    <div class="bg-decoration">
      <div class="circle circle-1"></div>
      <div class="circle circle-2"></div>
      <div class="circle circle-3"></div>
    </div>
    
    <!-- 登录卡片 -->
    <div class="login-container">
      <div class="login-header">
        <div class="logo">
          <svg viewBox="0 0 32 32" fill="none">
            <path d="M16 2L2 9l14 7 14-7-14-7z" fill="currentColor" opacity="0.3"/>
            <path d="M16 2L2 9l14 7 14-7-14-7z" stroke="currentColor" stroke-width="1.5" fill="none"/>
            <path d="M2 23l14 7 14-7" stroke="currentColor" stroke-width="1.5" fill="none"/>
            <path d="M2 16l14 7 14-7" stroke="currentColor" stroke-width="1.5" fill="none"/>
          </svg>
        </div>
        <h1>HERMES AGENT</h1>
        <p>智能助手管理平台</p>
      </div>
      
      <n-card class="login-card" :bordered="false">
        <n-space vertical :size="20">
          <div class="input-group">
            <label>登录密码</label>
            <n-input 
              v-model:value="password" 
              type="password" 
              show-password-on="click" 
              placeholder="请输入登录密码" 
              @keyup.enter="handleLogin"
              size="large"
            />
          </div>
          <n-button 
            type="primary" 
            block 
            :loading="loading" 
            @click="handleLogin"
            size="large"
            strong
          >
            登录
          </n-button>
        </n-space>
      </n-card>
      
      <div class="login-footer">
        <span>Hermes WebUI Pro v2.2.0</span>
      </div>
    </div>
  </div>
</template>

<style scoped lang="scss">
.login-page {
  height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: var(--body-color);
  position: relative;
  overflow: hidden;
}

.bg-decoration {
  position: absolute;
  inset: 0;
  pointer-events: none;
}

.circle {
  position: absolute;
  border-radius: 50%;
  background: var(--primary-color);
  opacity: 0.1;
  filter: blur(60px);
  
  &-1 {
    width: 300px;
    height: 300px;
    top: -100px;
    right: -50px;
    animation: float 8s ease-in-out infinite;
  }
  
  &-2 {
    width: 200px;
    height: 200px;
    bottom: -50px;
    left: -30px;
    animation: float 6s ease-in-out infinite reverse;
  }
  
  &-3 {
    width: 150px;
    height: 150px;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    animation: pulse 4s ease-in-out infinite;
  }
}

@keyframes float {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-20px); }
}

@keyframes pulse {
  0%, 100% { opacity: 0.1; transform: translate(-50%, -50%) scale(1); }
  50% { opacity: 0.2; transform: translate(-50%, -50%) scale(1.1); }
}

.login-container {
  position: relative;
  z-index: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 32px;
}

.login-header {
  text-align: center;
  
  .logo {
    width: 64px;
    height: 64px;
    margin: 0 auto 16px;
    color: var(--primary-color);
    
    svg {
      width: 100%;
      height: 100%;
    }
  }
  
  h1 {
    font-size: 28px;
    font-weight: 700;
    letter-spacing: 4px;
    margin-bottom: 8px;
  }
  
  p {
    font-size: 14px;
    color: var(--text-secondary);
  }
}

.login-card {
  width: 400px;
  padding: 8px;
  background: var(--card-bg) !important;
  border-radius: 16px !important;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.1);
  
  .input-group {
    display: flex;
    flex-direction: column;
    gap: 8px;
    
    label {
      font-size: 14px;
      font-weight: 500;
      color: var(--text-secondary);
    }
  }
}

.login-footer {
  font-size: 12px;
  color: var(--text-tertiary);
}
</style>