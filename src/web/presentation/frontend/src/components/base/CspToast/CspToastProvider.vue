<script setup lang="ts">
import {
  ToastPortal,
  ToastProvider,
  ToastViewport,
} from 'reka-ui'

export interface CspToastProviderProps {
  label?: string
  duration?: number
  swipeDirection?: 'up' | 'right' | 'down' | 'left'
  disableSwipe?: boolean
}

withDefaults(defineProps<CspToastProviderProps>(), {
  label: 'Notification',
  duration: 3200,
  swipeDirection: 'right',
  disableSwipe: false,
})
</script>

<template>
  <ToastProvider
    :label="label"
    :duration="duration"
    :disable-swipe="disableSwipe"
    :swipe-direction="swipeDirection"
  >
    <slot />

    <ToastPortal>
      <ToastViewport class="csp-toast-viewport" />
    </ToastPortal>
  </ToastProvider>
</template>

<style lang="scss">
.csp-toast-viewport {
  position: fixed;
  top: var(--csp-space-4);
  right: var(--csp-space-4);
  z-index: var(--csp-z-toast);
  width: min(26rem, calc(100vw - (var(--csp-space-4) * 2)));
  max-width: 100vw;
  display: flex;
  flex-direction: column;
  gap: var(--csp-space-3);
  margin: 0;
  padding: 0;
  list-style: none;
  outline: none;
}
</style>
