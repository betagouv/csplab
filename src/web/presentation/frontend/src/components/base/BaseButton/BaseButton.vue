<script setup lang="ts">
import type { PrimitiveProps } from 'reka-ui'
import { Primitive } from 'reka-ui'
import { computed } from 'vue'
import BaseIcon from '@/components/base/BaseIcon/BaseIcon.vue'

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
    class="btn"
    :class="[
      `btn--${variant}`,
      `btn--${size}`,
      { 'btn--icon-only': isIconOnly },
      { 'btn--icon-left': !isIconOnly && isIconLeft && Boolean(icon) },
      { 'btn--icon-right': !isIconOnly && !isIconLeft && Boolean(icon) },
    ]"
  >
    <span
      v-if="label"
      class="btn__label"
    >
      {{ label }}
    </span>
    <span
      v-if="icon"
      class="btn__icon"
    >
      <BaseIcon
        :name="icon"
      />
    </span>
  </Primitive>
</template>

<style scoped lang="scss">
.btn {
  display: inline-flex;
  width: fit-content;
  align-items: center;
  justify-content: center;
  gap: var(--btn-gap);
  white-space: nowrap;
  font-weight: 500;
  line-height: 1.25;
  cursor: pointer;
  border: none;
  text-decoration: none;
  padding: var(--btn-padding-y) var(--btn-padding-x);

  &:focus-visible {
    outline: 2px solid var(--csplab-focus-ring-color);
    outline-offset: 2px;
  }

  &:disabled {
    pointer-events: none;
    background-color: var(--background-disabled-grey);
    color: var(--text-disabled-grey);
    box-shadow: none;
  }
}

.btn--primary {
  background-color: var(--background-action-high-blue-france);
  color: var(--text-inverted-grey);

  &:hover {
    background-color: var(--background-action-high-blue-france-hover);
  }

  &:active {
    background-color: var(--background-action-high-blue-france-active);
  }
}

.btn--secondary {
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

.btn--tertiary {
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

.btn--tertiary-no-outline {
  background-color: transparent;
  color: var(--text-action-high-blue-france);

  &:hover {
    background-color: var(--background-default-grey-hover);
  }

  &:active {
    background-color: var(--background-default-grey-active);
  }
}

.btn:deep(.icon) {
  width: 1.25em;
  height: 1.25em;
}

.btn--icon-only {
  padding: var(--btn-padding-y) var(--btn-padding-y);
}

.btn--icon-right {
  flex-direction: row;
  padding-right: var(--btn-padding-x-sm);
}

.btn--icon-left {
  flex-direction: row-reverse;
  padding-left: var(--btn-padding-x-sm);
}

.btn--sm {
  font-size: 0.825rem;

  --btn-gap: 0.375rem;
  --btn-padding-y: 0.5em;
  --btn-padding-x: 1.25em;
  --btn-padding-x-sm: 0.75em;
}

.btn--md {
  font-size: 0.875rem;

  --btn-gap: 0.5rem;
  --btn-padding-y: 0.75em;
  --btn-padding-x: 1.5em;
  --btn-padding-x-sm: 1em;
}

.btn--lg {
  font-size: 1rem;

  --btn-gap: 0.625rem;
  --btn-padding-y: 0.75em;
  --btn-padding-x: 1.5em;
  --btn-padding-x-sm: 1em;
}
</style>
