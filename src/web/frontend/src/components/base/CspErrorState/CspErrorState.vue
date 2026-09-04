<script setup lang="ts">
import CspIcon from '@/components/base/CspIcon/CspIcon.vue'

withDefaults(defineProps<{
  title?: string
  description?: string
  icon?: string
}>(), {
  title: 'Une erreur est survenue',
  description: undefined,
  icon: 'ri:error-warning-line',
})
</script>

<template>
  <div
    class="csp-error-state"
    role="alert"
  >
    <CspIcon
      :name="icon"
      :size="24"
      class="csp-error-state__icon"
    />
    <p class="csp-error-state__title">
      {{ title }}
    </p>
    <p
      v-if="description"
      class="csp-error-state__description"
    >
      {{ description }}
    </p>
    <div
      v-if="$slots.action"
      class="csp-error-state__action"
    >
      <slot name="action" />
    </div>
  </div>
</template>

<style scoped lang="scss">
.csp-error-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: var(--csp-space-2);
  padding: var(--csp-space-10) var(--csp-space-4);
  text-align: center;
}

.csp-error-state__icon {
  color: var(--text-default-error);
}

.csp-error-state__title {
  margin: 0;
  font-size: var(--csp-font-size-base);
  font-weight: var(--csp-font-weight-medium);
  color: var(--text-title-grey);
}

.csp-error-state__description {
  margin: 0;
  font-size: var(--csp-font-size-sm);
  color: var(--text-mention-grey);
}

.csp-error-state__action {
  margin-top: var(--csp-space-2);
}
</style>
