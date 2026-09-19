<script setup lang="ts">
import CspToast from '@/components/base/CspToast/CspToast.vue'
import CspToastProvider from '@/components/base/CspToast/CspToastProvider.vue'
import { useToast } from '@/composables/ui/useToast'

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
      :action-label="toast.action?.label ?? null"
      :action-icon="toast.action?.icon ?? null"
      :action-alt-text="toast.action?.label"
      @action="toast.action?.onSelect()"
      @update:open="(value) => !value && dismissToast(toast.id)"
    />
  </CspToastProvider>
</template>
