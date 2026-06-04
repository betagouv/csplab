<script setup lang="ts">
import type { PrimitiveProps } from 'reka-ui'
import { Primitive } from 'reka-ui'
import { computed } from 'vue'
import CspIcon from '@/components/base/CspIcon/CspIcon.vue'

type ButtonProps = PrimitiveProps & {
  variant?: 'primary' | 'secondary' | 'tertiary' | 'tertiary-no-outline'
  size?: 'sm' | 'md' | 'lg'
  isIconLeft?: boolean
} & ({
  label: string
  icon?: never
} | {
  icon: string
  label?: never
})

const props = withDefaults(defineProps<ButtonProps>(), {
  variant: 'primary',
  size: 'md',
  as: 'button',
  isIconLeft: false,
})

const isIconOnly = computed(() => Boolean(props.icon) && !props.label)
</script>

<template>
  <Primitive
    v-bind="props"
    class="csp-btn"
    :class="[
      `csp-btn--${variant}`,
      `csp-btn--${size}`,
      { 'csp-btn--icon-only': isIconOnly },
      { 'csp-btn--icon-left': !isIconOnly && isIconLeft && Boolean(icon) },
      { 'csp-btn--icon-right': !isIconOnly && !isIconLeft && Boolean(icon) },
    ]"
  >
    <span
      v-if="label"
      class="csp-btn__label"
    >
      {{ label }}
    </span>
    <span
      v-if="icon"
      class="btn__icon"
    >
      <CspIcon
        class="csp-btn__icon"
        :name="icon"
      />
    </span>
  </Primitive>
</template>

<style scoped lang="scss">
.csp-btn {
  display: inline-flex;
  width: fit-content;
  align-items: center;
  justify-content: center;
  gap: var(--csp-btn-gap);
  white-space: nowrap;
  font-weight: 500;
  line-height: 1.25;
  cursor: pointer;
  border: none;
  text-decoration: none;
  padding: var(--csp-btn-padding-y) var(--csp-btn-padding-x);

  &:focus-visible {
    outline: 2px solid var(--csp-focus-ring-color);
    outline-offset: 2px;
  }

  &:disabled {
    pointer-events: none;
    background-color: var(--background-disabled-grey);
    color: var(--text-disabled-grey);
    box-shadow: none;
  }
}

.csp-btn--primary {
  background-color: var(--background-action-high-blue-france);
  color: var(--text-inverted-grey);

  &:hover {
    background-color: var(--background-action-high-blue-france-hover);
  }

  &:active {
    background-color: var(--background-action-high-blue-france-active);
  }
}

.csp-btn--secondary {
  background-color: transparent;
  color: var(--text-action-high-blue-france);
  box-shadow: inset 0 0 0 1px var(--border-action-high-blue-france);

  &:hover {
    background-color: var(--background-default-grey-hover);
  }

  &:active {
    background-color: var(--background-default-grey-active);
  }
}

.csp-btn--tertiary {
  background-color: transparent;
  color: var(--text-action-high-blue-france);
  box-shadow: inset 0 0 0 1px var(--border-default-grey);

  &:hover {
    background-color: var(--background-default-grey-hover);
  }

  &:active {
    background-color: var(--background-default-grey-active);
  }
}

.csp-btn--tertiary-no-outline {
  background-color: transparent;
  color: var(--text-action-high-blue-france);

  &:hover {
    background-color: var(--background-default-grey-hover);
  }

  &:active {
    background-color: var(--background-default-grey-active);
  }
}

.csp-btn__icon {
  width: 1.25em;
  height: 1.25em;
}

.csp-btn--icon-only {
  padding: var(--csp-btn-padding-y) var(--csp-btn-padding-y);
}

.csp-btn--icon-right {
  flex-direction: row;
  padding-right: var(--csp-btn-padding-x-sm);
}

.csp-btn--icon-left {
  flex-direction: row-reverse;
  padding-left: var(--csp-btn-padding-x-sm);
}

.csp-btn--sm {
  font-size: 0.825rem;

  --csp-btn-gap: 0.375rem;
  --csp-btn-padding-y: 0.5em;
  --csp-btn-padding-x: 1.25em;
  --csp-btn-padding-x-sm: 0.75em;
}

.csp-btn--md {
  font-size: 0.875rem;

  --csp-btn-gap: 0.5rem;
  --csp-btn-padding-y: 0.75em;
  --csp-btn-padding-x: 1.5em;
  --csp-btn-padding-x-sm: 1em;
}

.csp-btn--lg {
  font-size: 1rem;

  --csp-btn-gap: 0.625rem;
  --csp-btn-padding-y: 0.75em;
  --csp-btn-padding-x: 1.5em;
  --csp-btn-padding-x-sm: 1em;
}
</style>
