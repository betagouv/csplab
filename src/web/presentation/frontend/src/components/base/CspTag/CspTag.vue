<script setup lang="ts">
import type { PrimitiveProps } from 'reka-ui'
import type { CspTagSize } from './tag'
import { Primitive, Toggle, ToggleGroupItem } from 'reka-ui'
import { computed } from 'vue'
import CspIcon from '@/components/base/CspIcon/CspIcon.vue'
import { resolveDismissAriaLabel, resolveTagRoot } from './tag'
import { useCspTagGroup } from './useCspTagGroup'

type CspTagPolymorphicProps = Pick<PrimitiveProps, 'as' | 'asChild'>

interface CspTagIconProps {
  icon?: string
}

type CspTagProps = {
  size?: CspTagSize
  label?: string
  disabled?: boolean
} & (
  (CspTagIconProps & CspTagPolymorphicProps & {
    variant?: 'static'
  })
  | (CspTagIconProps & CspTagPolymorphicProps & {
    variant: 'clickable'
    href?: string
  })
  | (CspTagIconProps & {
    variant: 'selectable'
    value?: string | number
  })
  | {
    variant: 'dismissible'
    dismissLabel?: string
  }
)

const props = defineProps<CspTagProps>()

const emit = defineEmits<{
  dismiss: []
}>()

const variant = computed(() => props.variant ?? 'static')

const pressed = defineModel<boolean>('pressed', { default: false })

const group = useCspTagGroup()

const resolvedSize = computed<CspTagSize>(() => props.size ?? group?.size ?? 'md')
const resolvedDisabled = computed(() => props.disabled ?? group?.disabled ?? false)

const isInteractive = computed(() => variant.value !== 'static' && variant.value !== 'dismissible')
const isGroupItem = computed(() => variant.value === 'selectable' && group !== null)

const iconName = computed(() => ('icon' in props ? props.icon : undefined))
const href = computed(() => ('href' in props ? props.href : undefined))
const polymorphicAs = computed(() => ('as' in props ? props.as : undefined))
const polymorphicAsChild = computed(() => ('asChild' in props ? props.asChild : undefined))

const dismissAriaLabel = computed(() =>
  resolveDismissAriaLabel('dismissLabel' in props ? props.dismissLabel : undefined, props.label),
)

const root = computed(() => {
  const kind = resolveTagRoot({
    variant: variant.value,
    inGroup: isGroupItem.value,
    disabled: resolvedDisabled.value,
    hasHref: Boolean(href.value),
  })

  switch (kind) {
    case 'toggle-group-item':
      return {
        is: ToggleGroupItem,
        attrs: {
          value: 'value' in props ? props.value : undefined,
          disabled: resolvedDisabled.value,
        },
      }

    case 'toggle':
      return {
        is: Toggle,
        attrs: {
          'modelValue': pressed.value,
          'onUpdate:modelValue': (value: boolean) => { pressed.value = value },
          'disabled': resolvedDisabled.value,
        },
      }

    case 'a':
      return {
        is: Primitive,
        attrs: { as: polymorphicAs.value ?? 'a', asChild: polymorphicAsChild.value, href: href.value },
      }

    case 'button':
      return {
        is: Primitive,
        attrs: variant.value === 'dismissible'
          ? {
              'as': 'button',
              'type': 'button',
              'disabled': resolvedDisabled.value,
              'aria-label': dismissAriaLabel.value,
              'onClick': () => emit('dismiss'),
            }
          : {
              as: polymorphicAs.value ?? 'button',
              asChild: polymorphicAsChild.value,
              type: 'button',
              disabled: resolvedDisabled.value,
            },
      }

    case 'p':
    default:
      return {
        is: Primitive,
        attrs: { as: polymorphicAs.value ?? 'p', asChild: polymorphicAsChild.value },
      }
  }
})
</script>

<template>
  <component
    :is="root.is"
    v-bind="root.attrs"
    class="csp-tag"
    :class="[
      `csp-tag--${resolvedSize}`,
      {
        'csp-tag--interactive': isInteractive,
        'csp-tag--dismissible': variant === 'dismissible',
      },
    ]"
  >
    <CspIcon
      v-if="iconName"
      class="csp-tag__icon"
      :name="iconName"
      aria-hidden="true"
    />
    {{ label }}
    <CspIcon
      v-if="variant === 'dismissible'"
      class="csp-tag__dismiss"
      name="ri:close-line"
      aria-hidden="true"
    />
  </component>
</template>

<style scoped lang="scss">
.csp-tag {
  // White disc + blue-france (#000091) check, readable over any background.
  --csp-tag-check-icon: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24'%3E%3Ccircle cx='12' cy='12' r='11' fill='white'/%3E%3Cpath fill='%23000091' d='M12 22C6.477 22 2 17.523 2 12S6.477 2 12 2s10 4.477 10 10-4.477 10-10 10zm0-2a8 8 0 1 0 0-16 8 8 0 0 0 0 16zm-.997-4L6.76 11.757l1.414-1.414 2.829 2.829 5.657-5.657 1.414 1.414L11.003 16z'/%3E%3C/svg%3E");
  display: inline-flex;
  align-items: center;
  gap: var(--csp-tag-gap);
  font-size: var(--csp-tag-font-size);
  font-weight: 500;
  line-height: 1.25;
  padding: var(--csp-tag-padding-y) var(--csp-tag-padding-x);
  border-radius: 2rem;
  border: none;
  background-color: var(--background-contrast-grey);
  color: var(--text-label-grey);
  white-space: nowrap;
  cursor: default;
  margin: 0;
  text-decoration: none;
}

.csp-tag--sm {
  --csp-tag-font-size: 0.75rem;
  --csp-tag-padding-y: 0.25rem;
  --csp-tag-padding-x: 0.625rem;
  --csp-tag-gap: 0.25rem;
  --csp-tag-check-size: 0.75rem;
}

.csp-tag--md {
  --csp-tag-font-size: 0.875rem;
  --csp-tag-padding-y: 0.25rem;
  --csp-tag-padding-x: 0.75rem;
  --csp-tag-gap: 0.375rem;
  --csp-tag-check-size: 1rem;
}

.csp-tag--lg {
  --csp-tag-font-size: 1rem;
  --csp-tag-padding-y: 0.375rem;
  --csp-tag-padding-x: 1rem;
  --csp-tag-gap: 0.5rem;
  --csp-tag-check-size: 1.25rem;
}

.csp-tag__icon {
  width: 1em;
  height: 1em;
  flex-shrink: 0;
}

.csp-tag--interactive {
  cursor: pointer;
  background-color: var(--background-action-low-blue-france);
  color: var(--text-action-high-blue-france);

  &:hover:not(:disabled):not([data-disabled]) {
    background-color: var(--background-action-low-blue-france-hover);
  }

  &:active:not(:disabled):not([data-disabled]) {
    background-color: var(--background-action-low-blue-france-active);
  }

  &:focus-visible {
    outline: 2px solid var(--csp-focus-ring-color);
    outline-offset: 2px;
  }

  &:disabled,
  &[data-disabled] {
    cursor: not-allowed;
    background-color: var(--background-disabled-grey);
    color: var(--text-disabled-grey);
  }
}

.csp-tag--interactive[data-state='on'],
.csp-tag--interactive[aria-pressed='true'] {
  position: relative;
  overflow: visible;
  background-color: var(--background-action-high-blue-france);
  color: var(--text-inverted-blue-france);

  // Check badge overhanging the top-right corner (DSFR spec).
  &::after {
    content: '';
    position: absolute;
    top: 0;
    right: 0;
    transform: translate(40%, -40%);
    width: var(--csp-tag-check-size);
    height: var(--csp-tag-check-size);
    background-image: var(--csp-tag-check-icon);
    background-size: 100% 100%;
    background-repeat: no-repeat;
  }

  &:hover:not(:disabled):not([data-disabled]) {
    background-color: var(--background-action-high-blue-france-hover);
  }

  &:active:not(:disabled):not([data-disabled]) {
    background-color: var(--background-action-high-blue-france-active);
  }

  &:disabled,
  &[data-disabled] {
    background-color: var(--background-disabled-grey);
    color: var(--text-disabled-grey);
  }
}

.csp-tag--dismissible {
  cursor: pointer;
  padding-right: var(--csp-tag-padding-x-sm, 0.5rem);
  background-color: var(--background-action-high-blue-france);
  color: var(--text-inverted-blue-france);

  &:hover:not(:disabled) {
    background-color: var(--background-action-high-blue-france-hover);
  }

  &:active:not(:disabled) {
    background-color: var(--background-action-high-blue-france-active);
  }

  &:focus-visible {
    outline: 2px solid var(--csp-focus-ring-color);
    outline-offset: 2px;
  }

  &:disabled {
    cursor: not-allowed;
    background-color: var(--background-disabled-grey);
    color: var(--text-disabled-grey);
  }
}

.csp-tag--sm.csp-tag--dismissible {
  --csp-tag-padding-x-sm: 0.375rem;
}

.csp-tag--md.csp-tag--dismissible {
  --csp-tag-padding-x-sm: 0.5rem;
}

.csp-tag__dismiss {
  width: 1em;
  height: 1em;
  flex-shrink: 0;
  color: currentColor;
}
</style>
