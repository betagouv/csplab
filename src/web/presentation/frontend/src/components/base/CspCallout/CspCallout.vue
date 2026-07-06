<script setup lang="ts">
import { computed, useSlots } from 'vue'
import CspIcon from '@/components/base/CspIcon/CspIcon.vue'

export interface CspCalloutProps {
  variant?: 'default' | 'info' | 'success' | 'warning' | 'error'
  title?: string | null
  description?: string | null
  icon?: string | null
  showIcon?: boolean
}

const props = withDefaults(defineProps<CspCalloutProps>(), {
  variant: 'default',
  title: null,
  description: null,
  icon: null,
  showIcon: true,
})

const slots = useSlots()

const hasTitle = computed(() => Boolean(slots.title) || Boolean(props.title))
const hasDescription = computed(() => Boolean(slots.description) || Boolean(props.description))
const hasBody = computed(() => Boolean(slots.default))

const iconByVariant: Record<NonNullable<CspCalloutProps['variant']>, string> = {
  default: 'ri:information-line',
  info: 'ri:information-line',
  success: 'ri:checkbox-circle-line',
  warning: 'ri:alert-line',
  error: 'ri:error-warning-line',
}

const resolvedIcon = computed(() => props.icon ?? iconByVariant[props.variant])
</script>

<template>
  <div
    class="csp-callout"
    :class="`csp-callout--${variant}`"
    role="alert"
  >
    <div
      v-if="showIcon"
      class="csp-callout__icon"
    >
      <slot name="icon">
        <CspIcon :name="resolvedIcon" />
      </slot>
    </div>

    <div class="csp-callout__content">
      <h4
        v-if="hasTitle"
        class="csp-callout__title"
      >
        <slot name="title">
          {{ title }}
        </slot>
      </h4>

      <p
        v-if="hasDescription"
        class="csp-callout__description"
      >
        <slot name="description">
          {{ description }}
        </slot>
      </p>

      <div
        v-if="hasBody"
        class="csp-callout__body"
      >
        <slot />
      </div>
    </div>
  </div>
</template>

<style scoped lang="scss">
.csp-callout {
  --csp-callout-bg: var(--background-alt-grey);
  --csp-callout-border: var(--border-default-grey);
  --csp-callout-accent: var(--border-action-high-blue-france);
  --csp-callout-title: var(--text-title-grey);
  --csp-callout-text: var(--text-default-grey);
  --csp-callout-icon: var(--text-action-high-grey);

  display: flex;
  align-items: flex-start;
  gap: var(--csp-space-3);
  padding: var(--csp-space-4);
  background-color: var(--csp-callout-bg);
  border: 1px solid var(--csp-callout-border);
  border-left: 4px solid var(--csp-callout-accent);
  border-radius: 0.25rem;
  color: var(--csp-callout-text);
}

.csp-callout__icon {
  flex-shrink: 0;
  color: var(--csp-callout-icon);
  font-size: 1.125rem;
  line-height: 1;
  margin-top: 0.0625rem;
}

.csp-callout__content {
  flex: 1 1 auto;
  display: flex;
  flex-direction: column;
  gap: var(--csp-space-1);
  min-width: 0;
}

.csp-callout__title {
  margin: 0;
  font-size: 0.9375rem;
  line-height: 1.35;
  font-weight: 700;
  color: var(--csp-callout-title);
}

.csp-callout__description {
  margin: 0;
  font-size: 0.875rem;
  line-height: 1.5;
  color: var(--csp-callout-text);
}

.csp-callout__body {
  margin-top: var(--csp-space-2);
  font-size: 0.875rem;
  line-height: 1.5;
  color: var(--csp-callout-text);

  :deep(ul) {
    margin: 0;
    padding-left: 1.25rem;
    list-style-type: disc;

    li {
      margin-top: var(--csp-space-1);
    }
  }

  :deep(p) {
    margin: 0;

    + p {
      margin-top: var(--csp-space-2);
    }
  }
}

.csp-callout--info {
  --csp-callout-bg: color-mix(in sRGB, var(--background-contrast-info) 15%, var(--background-default-grey));
  --csp-callout-border: color-mix(in sRGB, var(--border-plain-info) 30%, transparent);
  --csp-callout-accent: var(--border-plain-info);
  --csp-callout-icon: var(--text-default-info);
}

.csp-callout--success {
  --csp-callout-bg: color-mix(in sRGB, var(--background-contrast-success) 15%, var(--background-default-grey));
  --csp-callout-border: color-mix(in sRGB, var(--border-plain-success) 30%, transparent);
  --csp-callout-accent: var(--border-plain-success);
  --csp-callout-icon: var(--text-default-success);
}

.csp-callout--warning {
  --csp-callout-bg: color-mix(in sRGB, var(--background-contrast-warning) 15%, var(--background-default-grey));
  --csp-callout-border: color-mix(in sRGB, var(--border-plain-warning) 30%, transparent);
  --csp-callout-accent: var(--border-plain-warning);
  --csp-callout-icon: var(--text-default-warning);
}

.csp-callout--error {
  --csp-callout-bg: color-mix(in sRGB, var(--background-contrast-error) 15%, var(--background-default-grey));
  --csp-callout-border: color-mix(in sRGB, var(--border-plain-error) 30%, transparent);
  --csp-callout-accent: var(--border-plain-error);
  --csp-callout-icon: var(--text-default-error);
}
</style>
