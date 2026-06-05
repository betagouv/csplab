<script setup lang="ts">
import { Icon } from '@iconify/vue'
import { computed } from 'vue'

type CspBadgeProps = {
  size?: 'sm' | 'md' | 'lg'
  variant?: 'default' | 'soft' | 'outline'
  label: string
} & ({
  type?: 'info' | 'new' | 'warning' | 'error' | 'success'
  icon?: never
  color?: never
} | {
  icon?: string
  color?: string
  type?: never
})

const props = withDefaults(defineProps<CspBadgeProps>(), {
  variant: 'default',
  size: 'md',
})

const resolvedIcon = computed(() => {
  if (props.type) {
    switch (props.type) {
      case 'info':
        return 'ri:information-fill'
      case 'new':
        return 'ri:flashlight-fill'
      case 'warning':
        return 'ri:alert-fill'
      case 'error':
        return 'ri:spam-fill'
      case 'success':
        return 'ri:checkbox-circle-fill'
    }
  }

  if (props.icon) {
    return props.icon
  }

  return null
})
</script>

<template>
  <p
    class="badge"
    :class="[
      `badge--${variant}`,
      `badge--${size}`,
      { [`badge--type-${type}`]: Boolean(type) },
      { 'badge--custom-color': Boolean(color) },
    ]"
    :style="{
      color: color ?? undefined,
    }"
  >
    <span
      v-if="resolvedIcon"
    >
      <Icon
        :icon="resolvedIcon"
        :width="12"
        :height="12"
        aria-hidden="true"
        class="badge__icon"
      />
    </span>
    <span class="badge__label">
      {{ props.label }}
    </span>
  </p>
</template>

<style scoped lang="scss">
.badge {
  display: inline-flex;
  align-items: center;
  align-self: flex-start;
  border-radius: 0.25rem;
  font-weight: bold;
  text-transform: uppercase;
  letter-spacing: 0.05em;

  font-size: var(--badge-font-size);
  padding: var(--badge-padding-y) var(--badge-padding-x);
  gap: var(--badge-gap);

  --badge-default-bg: var(--background-contrast-grey);
  --badge-default-text: var(--text-default-grey);
  --badge-soft-bg: var(--background-alt-grey);
  --badge-soft-text: var(--text-mention-grey);
  --badge-outline-border: var(--border-default-grey);
  --badge-outline-text: var(--text-default-grey);
}

.badge__label {
  line-height: 1.25;
}

.badge__icon {
  width: 1em;
  height: 1em;
}

.badge--default {
  background-color: var(--badge-default-bg);
  color: var(--badge-default-text);
}

.badge--soft {
  background-color: var(--badge-soft-bg);
  color: var(--badge-soft-text);
}

.badge--outline {
  background-color: transparent;
  border: 1px solid var(--badge-outline-border);
  color: var(--badge-outline-text);
}

.badge--custom-color {
  --badge-default-bg: color-mix(in sRGB, currentColor 10%, transparent);
  --badge-default-text: currentColor;
  --badge-soft-bg: color-mix(in sRGB, currentColor 5%, transparent);
  --badge-soft-text: color-mix(in sRGB, currentColor 80%, transparent);
  --badge-outline-border: color-mix(in sRGB, currentColor 25%, transparent);
  --badge-outline-text: currentColor;
}

.badge--type-info {
  --badge-default-bg: var(--background-contrast-info);
  --badge-default-text: var(--text-default-info);
  --badge-soft-bg: color-mix(in sRGB, var(--background-contrast-info) 30%, transparent);
  --badge-soft-text: color-mix(in sRGB, var(--text-default-info) 80%, transparent);
  --badge-outline-border: color-mix(in sRGB, var(--border-plain-info) 25%, transparent);
  --badge-outline-text: var(--text-default-info);
}

.badge--type-success {
  --badge-default-bg: var(--background-contrast-success);
  --badge-default-text: var(--text-default-success);
  --badge-soft-bg: color-mix(in sRGB, var(--background-contrast-success) 20%, transparent);
  --badge-soft-text: color-mix(in sRGB, var(--text-default-success) 80%, transparent);
  --badge-outline-border: color-mix(in sRGB, var(--border-plain-success) 25%, transparent);
  --badge-outline-text: var(--text-default-success);
}

.badge--type-new {
  --badge-default-bg: var(--background-contrast-yellow-moutarde);
  --badge-default-text: var(--text-action-high-yellow-moutarde);
  --badge-soft-bg: color-mix(in sRGB, var(--background-contrast-yellow-moutarde) 30%, transparent);
  --badge-soft-text: color-mix(in sRGB, var(--text-action-high-yellow-moutarde) 80%, transparent);
  --badge-outline-border: var(--background-contrast-yellow-moutarde);
  --badge-outline-text: var(--text-action-high-yellow-moutarde);
}

.badge--type-warning {
  --badge-default-bg: var(--background-contrast-warning);
  --badge-default-text: var(--text-default-warning);
  --badge-soft-bg: color-mix(in sRGB, var(--background-contrast-warning) 30%, transparent);
  --badge-soft-text: color-mix(in sRGB, var(--text-default-warning) 80%, transparent);
  --badge-outline-border: color-mix(in sRGB, var(--border-plain-warning) 25%, transparent);
  --badge-outline-text: var(--text-default-warning);
}

.badge--type-error {
  --badge-default-bg: var(--background-contrast-error);
  --badge-default-text: var(--text-default-error);
  --badge-soft-bg: color-mix(in sRGB, var(--background-contrast-error) 30%, transparent);
  --badge-soft-text: color-mix(in sRGB, var(--text-default-error) 70%, transparent);
  --badge-outline-border: color-mix(in sRGB, var(--border-plain-error) 25%, transparent);
  --badge-outline-text: var(--text-default-error);
}

.badge__icon {
  flex-shrink: 0;
}

.badge--sm {
  --badge-padding-y: 0.0625rem;
  --badge-padding-x: 0.25rem;
  --badge-gap: 0.125rem;
  --badge-font-size: 0.625rem;
}

.badge--md {
  --badge-padding-y: 0.125rem;
  --badge-padding-x: 0.375rem;
  --badge-gap: 0.25rem;
  --badge-font-size: 0.75rem;
}

.badge--lg {
  --badge-padding-y: 0.15rem;
  --badge-padding-x: 0.5rem;
  --badge-gap: 0.375rem;
  --badge-font-size: 0.875rem;
}
</style>
