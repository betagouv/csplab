<script setup lang="ts">
import {
  ToastAction,
  ToastClose,
  ToastDescription,
  ToastRoot,
  ToastTitle,
} from 'reka-ui'
import { computed, useAttrs, useSlots } from 'vue'
import CspButton from '@/components/base/CspButton/CspButton.vue'
import CspIcon from '@/components/base/CspIcon/CspIcon.vue'

export interface CspToastProps {
  open?: boolean
  defaultOpen?: boolean
  title?: string | null
  description?: string | null
  duration?: number
  variant?: 'default' | 'info' | 'success' | 'warning' | 'error'
  showIcon?: boolean
  actionLabel?: string | null
  actionAltText?: string
  showClose?: boolean
  closeLabel?: string
}

defineOptions({
  inheritAttrs: false,
})

const props = withDefaults(defineProps<CspToastProps>(), {
  open: undefined,
  defaultOpen: false,
  title: null,
  description: null,
  duration: undefined,
  variant: 'default',
  showIcon: true,
  actionLabel: null,
  actionAltText: 'Exécuter l\'action',
  showClose: true,
  closeLabel: 'Fermer la notification',
})

const emit = defineEmits<{
  'update:open': [value: boolean]
  'action': []
}>()

const attrs = useAttrs()
const slots = useSlots()

const hasTitle = computed(() => Boolean(slots.title) || Boolean(props.title))
const hasDescription = computed(() => Boolean(slots.description) || Boolean(props.description))
const hasAction = computed(() => Boolean(slots.action) || Boolean(props.actionLabel))

const iconByVariant: Record<NonNullable<CspToastProps['variant']>, string> = {
  default: 'ri:notification-3-line',
  info: 'ri:information-line',
  success: 'ri:checkbox-circle-line',
  warning: 'ri:alert-line',
  error: 'ri:error-warning-line',
}

const resolvedIcon = computed(() => iconByVariant[props.variant])
</script>

<template>
  <ToastRoot
    v-bind="attrs"
    :open="open"
    :default-open="defaultOpen"
    :duration="duration"
    class="csp-toast"
    :class="`csp-toast--${variant}`"
    @update:open="value => emit('update:open', value)"
  >
    <div class="csp-toast__layout">
      <div
        v-if="showIcon"
        class="csp-toast__icon"
      >
        <slot name="icon">
          <CspIcon :name="resolvedIcon" />
        </slot>
      </div>

      <div class="csp-toast__content">
        <ToastTitle
          v-if="hasTitle"
          as="h3"
          class="csp-toast__title"
        >
          <slot name="title">
            {{ title }}
          </slot>
        </ToastTitle>

        <ToastDescription
          v-if="hasDescription"
          as="p"
          class="csp-toast__description"
        >
          <slot name="description">
            {{ description }}
          </slot>
        </ToastDescription>

        <div
          v-if="$slots.default"
          class="csp-toast__body"
        >
          <slot />
        </div>
      </div>

      <div
        v-if="hasAction || showClose"
        class="csp-toast__actions"
      >
        <ToastAction
          v-if="hasAction"
          as-child
          :alt-text="actionAltText"
          @click="emit('action')"
        >
          <slot name="action">
            <CspButton
              variant="tertiary-no-outline"
              size="sm"
              :label="actionLabel!"
            />
          </slot>
        </ToastAction>

        <ToastClose
          v-if="showClose"
          as-child
        >
          <CspButton
            variant="tertiary-no-outline"
            size="sm"
            icon="ri:close-line"
            :aria-label="closeLabel"
          />
        </ToastClose>
      </div>
    </div>
  </ToastRoot>
</template>

<style lang="scss">
.csp-toast {
  --csp-toast-bg: var(--background-overlap-grey);
  --csp-toast-border: var(--border-default-grey);
  --csp-toast-accent: var(--border-action-high-blue-france);
  --csp-toast-title: var(--text-title-grey);
  --csp-toast-text: var(--text-default-grey);
  --csp-toast-icon: var(--text-action-high-grey);

  background-color: var(--csp-toast-bg);
  border: 1px solid var(--csp-toast-border);
  border-left: 4px solid var(--csp-toast-accent);
  color: var(--csp-toast-text);
  box-shadow: var(--csp-shadow-md);
  overflow: hidden;
  will-change: transform, opacity;
}

.csp-toast[data-state='open'] {
  animation: csp-toast-enter 160ms ease-out;
}

.csp-toast[data-state='closed'] {
  animation: csp-toast-exit 120ms ease-in forwards;
}

.csp-toast[data-swipe='move'] {
  transform: translate(var(--reka-toast-swipe-move-x), var(--reka-toast-swipe-move-y));
}

.csp-toast[data-swipe='cancel'] {
  transform: translate(0, 0);
  transition: transform 120ms ease-out;
}

.csp-toast[data-swipe='end'] {
  animation: csp-toast-swipe-out 120ms ease-out forwards;
}

.csp-toast__layout {
  display: flex;
  align-items: flex-start;
  gap: var(--csp-space-3);
  padding: var(--csp-space-4);
}

.csp-toast__icon {
  color: var(--csp-toast-icon);
  font-size: 1.125rem;
  line-height: 1;
  margin-top: 0.125rem;
}

.csp-toast__content {
  flex: 1 1 auto;
  display: flex;
  flex-direction: column;
  gap: var(--csp-space-1);
  min-width: 0;
}

.csp-toast__title {
  margin: 0;
  font-size: 0.9375rem;
  line-height: 1.35;
  font-weight: 700;
  color: var(--csp-toast-title);
}

.csp-toast__description,
.csp-toast__body {
  margin: 0;
  font-size: 0.875rem;
  line-height: 1.45;
  color: var(--csp-toast-text);
}

.csp-toast__actions {
  display: flex;
  align-items: center;
  gap: var(--csp-space-2);
}

.csp-toast--info {
  --csp-toast-accent: var(--border-plain-info);
  --csp-toast-icon: var(--text-default-info);
}

.csp-toast--success {
  --csp-toast-accent: var(--border-plain-success);
  --csp-toast-icon: var(--text-default-success);
}

.csp-toast--warning {
  --csp-toast-accent: var(--border-plain-warning);
  --csp-toast-icon: var(--text-default-warning);
}

.csp-toast--error {
  --csp-toast-accent: var(--border-plain-error);
  --csp-toast-icon: var(--text-default-error);
}

@keyframes csp-toast-enter {
  from {
    opacity: 0;
    transform: translateY(-0.5rem) scale(0.98);
  }

  to {
    opacity: 1;
    transform: translateY(0) scale(1);
  }
}

@keyframes csp-toast-exit {
  from {
    opacity: 1;
    transform: translateY(0);
  }

  to {
    opacity: 0;
    transform: translateY(-0.25rem);
  }
}

@keyframes csp-toast-swipe-out {
  from {
    opacity: 1;
    transform: translate(var(--reka-toast-swipe-move-x), var(--reka-toast-swipe-move-y));
  }

  to {
    opacity: 0;
    transform: translate(var(--reka-toast-swipe-end-x), var(--reka-toast-swipe-end-y));
  }
}
</style>
