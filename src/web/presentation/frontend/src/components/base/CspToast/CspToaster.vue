<script setup lang="ts">
import CspToast from '@/components/base/CspToast/CspToast.vue'
import CspToastProvider from '@/components/base/CspToast/CspToastProvider.vue'
import { useToast } from '@/composables/useToast'

const { toasts, dismissToast } = useToast()
</script>

<template>
  <CspToastProvider>
    <slot />
    <CspToast
      v-for="toast in toasts"
      :key="toast.id"
      :open="true"
      :variant="toast.variant"
      :title="toast.title ?? null"
      :description="toast.description ?? null"
      :duration="toast.duration"
      @update:open="(value) => !value && dismissToast(toast.id)"
    />
  </CspToastProvider>
</template>
