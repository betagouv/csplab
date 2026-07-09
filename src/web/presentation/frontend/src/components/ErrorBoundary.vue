<script setup lang="ts">
import * as Sentry from '@sentry/vue'
import { onErrorCaptured, ref } from 'vue'

const captured = ref<Error | null>(null)

onErrorCaptured((err) => {
  captured.value = err instanceof Error ? err : new Error(String(err))
  Sentry.captureException(err)
  return false
})
</script>

<template>
  <slot v-if="!captured" />
  <div
    v-else
    role="alert"
  >
    <p>Une erreur est survenue.</p>
  </div>
</template>
