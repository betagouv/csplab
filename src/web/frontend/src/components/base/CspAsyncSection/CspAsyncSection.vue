<script setup lang="ts">
import CspErrorState from '@/components/base/CspErrorState/CspErrorState.vue'

withDefaults(defineProps<{
  pending: boolean
  error?: unknown
  loadingLabel?: string
  errorTitle?: string
  errorDescription?: string
  fill?: boolean
  minHeight?: string
}>(), {
  error: undefined,
  loadingLabel: 'Chargement',
  errorTitle: undefined,
  errorDescription: undefined,
  fill: false,
  minHeight: undefined,
})
</script>

<template>
  <div
    class="csp-async-section"
    :class="{ 'csp-async-section--fill': fill }"
    :style="minHeight ? { minHeight } : undefined"
  >
    <div
      v-if="pending"
      class="csp-async-section__loading"
      role="status"
      :aria-label="loadingLabel"
    >
      <slot name="skeleton" />
    </div>
    <CspErrorState
      v-else-if="error"
      :title="errorTitle"
      :description="errorDescription"
    >
      <template
        v-if="$slots['error-action']"
        #action
      >
        <slot name="error-action" />
      </template>
    </CspErrorState>
    <slot v-else />
  </div>
</template>

<style scoped lang="scss">
.csp-async-section--fill,
.csp-async-section--fill .csp-async-section__loading {
  display: flex;
  flex-direction: column;
  flex: 1;
  min-height: 0;
}
</style>
