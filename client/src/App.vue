<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { NConfigProvider, NMessageProvider, NDialogProvider, darkTheme, zhCN, dateZhCN } from 'naive-ui'
import AppSidebar from '@/components/layout/AppSidebar.vue'
import { useRouter, useRoute } from 'vue-router'

const router = useRouter()
const route = useRoute()
const isDark = ref(localStorage.getItem('hermes_theme') !== 'light')
const isLoginPage = computed(() => route.name === 'Login')

onMounted(() => { document.documentElement.classList.toggle('dark', isDark.value) })

const theme = computed(() => isDark.value ? darkTheme : null)
</script>

<template>
  <n-config-provider :theme="theme" :locale="zhCN" :date-locale="dateZhCN">
    <n-message-provider>
      <n-dialog-provider>
        <div class="app-layout" v-if="!isLoginPage">
          <AppSidebar />
          <main class="main-content">
            <router-view v-slot="{ Component }">
              <transition name="fade" mode="out-in">
                <component :is="Component" />
              </transition>
            </router-view>
          </main>
        </div>
        <router-view v-else />
      </n-dialog-provider>
    </n-message-provider>
  </n-config-provider>
</template>
