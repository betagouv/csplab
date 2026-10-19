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
  gap: var(--csp-empty-state-gap, var(--csp-space-2));
  padding: var(--csp-empty-state-padding-block, var(--csp-space-10)) var(--csp-space-4);
  background-color: var(--csp-empty-state-background, transparent);
  background-image: var(--csp-empty-state-backdrop, none);
  background-repeat: var(--csp-empty-state-backdrop-repeat, no-repeat);
  background-position: var(--csp-empty-state-backdrop-position, right bottom);
  background-size: var(--csp-empty-state-backdrop-size, cover);
  box-shadow: inset 0 0 0 var(--csp-empty-state-frame-width, 0) var(--border-default-grey);
  text-align: center;
}

.csp-empty-state__icon {
  box-sizing: content-box;
  padding: var(--csp-empty-state-icon-padding, 0);
  background-color: var(--csp-empty-state-icon-background, transparent);
  border-radius: var(--csp-empty-state-icon-radius, 0);
  color: var(--csp-empty-state-icon-color, var(--text-mention-grey));
}

.csp-empty-state__title {
  margin: 0;
  font-size: var(--csp-empty-state-title-size, var(--csp-font-size-base));
  font-weight: var(--csp-empty-state-title-weight, var(--csp-font-weight-medium));
  color: var(--text-title-grey);
}

.csp-empty-state__description {
  margin: 0;
  font-size: var(--csp-empty-state-description-size, var(--csp-font-size-sm));
  color: var(--text-mention-grey);
}

.csp-empty-state__action {
  margin-top: var(--csp-space-2);
}
</style>
