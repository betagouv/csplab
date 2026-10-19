<script setup lang="ts">
import CspIcon from '@/components/base/CspIcon/CspIcon.vue'

withDefaults(defineProps<{
  title: string
  description?: string
  icon?: string
}>(), {
  description: undefined,
  icon: 'ri:inbox-2-line',
})
</script>

<template>
  <div class="csp-empty-state">
    <CspIcon
      :name="icon"
      :size="24"
      class="csp-empty-state__icon"
    />
    <p class="csp-empty-state__title">
      {{ title }}
    </p>
    <p
      v-if="description"
      class="csp-empty-state__description"
    >
      {{ description }}
    </p>
    <div
      v-if="$slots.action"
      class="csp-empty-state__action"
    >
      <slot name="action" />
    </div>
  </div>
</template>

<style scoped lang="scss">
.csp-empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: var(--csp-empty-state-gap);
  padding: var(--csp-empty-state-padding-block) var(--csp-space-4);
  background: var(--csp-empty-state-backdrop), var(--csp-empty-state-background);
  box-shadow: inset 0 0 0 var(--csp-empty-state-frame-width) var(--border-default-grey);
  text-align: center;
}

.csp-empty-state__icon {
  box-sizing: content-box;
  padding: var(--csp-empty-state-icon-padding);
  background-color: var(--csp-empty-state-icon-background);
  border-radius: var(--csp-empty-state-icon-radius);
  color: var(--csp-empty-state-icon-color);
}

.csp-empty-state__title {
  margin: 0;
  font-size: var(--csp-empty-state-title-size);
  font-weight: var(--csp-empty-state-title-weight);
  color: var(--text-title-grey);
}

.csp-empty-state__description {
  margin: 0;
  font-size: var(--csp-empty-state-description-size);
  color: var(--text-mention-grey);
}

.csp-empty-state__action {
  margin-top: var(--csp-space-2);
}
</style>
