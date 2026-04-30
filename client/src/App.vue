<script setup lang="ts">
import { computed, ref, watch, onMounted, onUnmounted } from 'vue'
import { useRoute } from 'vue-router'
import { darkTheme, NConfigProvider, NMessageProvider, NDialogProvider, NNotificationProvider } from 'naive-ui'
import { useTheme } from '@/composables/useTheme'
import { lightThemeOverrides, darkThemeOverrides } from '@/styles/theme'
import AppSidebar from '@/components/layout/AppSidebar.vue'
import { useAuthStore } from '@/stores/auth'

const route = useRoute()
const { isDark } = useTheme()
const authStore = useAuthStore()
const ready = ref(false)

const naiveTheme = computed(() => isDark.value ? darkTheme : null)
const themeOverrides = computed(() => isDark.value ? darkThemeOverrides : lightThemeOverrides)
const isLoginPage = computed(() => route.name === 'login')

onMounted(async () => {
  if (authStore.token) {
    await authStore.verify()
  }
  ready.value = true
})
</script>

<template>
  <NConfigProvider :theme="naiveTheme" :theme-overrides="themeOverrides">
    <NMessageProvider>
      <NDialogProvider>
        <NNotificationProvider>
          <div v-if="ready" class="app-root" :class="{ 'is-login': isLoginPage }">
            <AppSidebar v-if="!isLoginPage" />
            <main class="app-main" :class="{ 'full-width': isLoginPage }">
              <router-view v-slot="{ Component }">
                <transition name="fade" mode="out-in">
                  <component :is="Component" />
                </transition>
              </router-view>
            </main>
          </div>
        </NNotificationProvider>
      </NDialogProvider>
    </NMessageProvider>
  </NConfigProvider>
</template>

<style lang="scss">
.app-root {
  display: flex;
  height: 100vh;
  height: 100dvh;
  overflow: hidden;
  background: var(--bg-body);
}

.app-main {
  flex: 1;
  overflow: hidden;
  display: flex;
  flex-direction: column;
  min-width: 0;

  &.full-width {
    width: 100%;
  }
}

.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.2s ease;
}
.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>
