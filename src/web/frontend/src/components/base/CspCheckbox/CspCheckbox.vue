<script setup lang="ts">
import { CheckboxIndicator, CheckboxRoot } from 'reka-ui'
import { computed, useAttrs, useId } from 'vue'

defineOptions({
  inheritAttrs: false,
})

const props = withDefaults(defineProps<{
  variant?: 'default' | 'checkbox-only'
  label: string
  value?: string
  disabled?: boolean
  indeterminate?: boolean
  size?: 'sm' | 'md' | 'lg'
  error?: boolean
  hint?: string
}>(), {
  variant: 'default',
  disabled: false,
  indeterminate: false,
  size: 'md',
  error: false,
})

const model = defineModel<boolean>()

const attrs = useAttrs()
const labelId = useId()
const hintId = useId()

const labelAttrs = computed(() => ({
  class: attrs.class,
  style: attrs.style,
}))

const controlAttrs = computed(() => {
  const { class: _c, style: _s, ...rest } = attrs
  return rest
})

const checkboxModelValue = computed<boolean | 'indeterminate' | undefined>(() => {
  if (model.value === undefined) {
    return undefined
  }
  return props.indeterminate
    ? ('indeterminate' as const)
    : model.value
})

function handleUpdate(val: unknown): void {
  if (typeof val === 'boolean') {
    model.value = val
  }
}
</script>

<template>
  <label
    v-bind="labelAttrs"
    class="csp-checkbox"
    :class="[
      `csp-checkbox--${size}`,
      { 'csp-checkbox--disabled': disabled },
      { 'csp-checkbox--error': error },
      { 'csp-checkbox--with-hint': hint },
    ]"
  >
    <CheckboxRoot
      v-bind="controlAttrs"
      class="csp-checkbox__control"
      :model-value="checkboxModelValue"
      :value="value"
      :disabled="disabled"
      :aria-labelledby="hint ? labelId : undefined"
      :aria-describedby="hint ? hintId : undefined"
      @update:model-value="handleUpdate"
    >
      <CheckboxIndicator
        class="csp-checkbox__indicator"
        force-mount
      />
    </CheckboxRoot>
    <span class="csp-checkbox__text">
      <span
        :id="labelId"
        class="csp-checkbox__label"
        :class="{ 'sr-only': variant === 'checkbox-only' }"
      >{{ label }}</span>
      <span
        v-if="hint"
        :id="hintId"
        class="csp-checkbox__hint"
      >{{ hint }}</span>
    </span>
  </label>
</template>

<style scoped lang="scss">
.csp-checkbox {
  display: inline-flex;
  align-items: center;
  gap: var(--csp-checkbox-gap);
  cursor: pointer;
  font-size: var(--csp-checkbox-font-size);
  color: var(--csp-checkbox-color);

  --csp-checkbox-gap: 0.5rem;
  --csp-checkbox-font-size: 0.875rem;
  --csp-checkbox-color: var(--text-default-grey);
  --csp-checkbox-size: 1.125rem;
  --csp-checkbox-indicator-check-w: 0.25rem;
  --csp-checkbox-indicator-check-h: 0.5rem;
  --csp-checkbox-indicator-dash-w: 0.5rem;
}

.csp-checkbox--sm {
  --csp-checkbox-size: 1rem;
  --csp-checkbox-font-size: 0.75rem;
  --csp-checkbox-gap: 0.375rem;
  --csp-checkbox-indicator-check-w: 0.1875rem;
  --csp-checkbox-indicator-check-h: 0.375rem;
  --csp-checkbox-indicator-dash-w: 0.375rem;
}

.csp-checkbox--lg {
  --csp-checkbox-size: 1.375rem;
  --csp-checkbox-font-size: 1rem;
  --csp-checkbox-gap: 0.625rem;
  --csp-checkbox-indicator-check-w: 0.3125rem;
  --csp-checkbox-indicator-check-h: 0.625rem;
  --csp-checkbox-indicator-dash-w: 0.625rem;
}

.csp-checkbox--with-hint {
  align-items: flex-start;
}

.csp-checkbox--disabled {
  cursor: not-allowed;
  color: var(--text-disabled-grey);
}

.csp-checkbox__control {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: var(--csp-checkbox-size);
  height: var(--csp-checkbox-size);
  flex: 0 0 auto;
  border-radius: 2px;
  border: 1px solid var(--border-action-high-blue-france);
  background: transparent;
  padding: 0;
  cursor: inherit;

  &[data-state='checked'],
  &[data-state='indeterminate'] {
    background: var(--background-active-blue-france);
    border-color: var(--border-active-blue-france);
  }

  &:focus-visible {
    outline: 2px solid var(--csp-focus-ring-color);
    outline-offset: 2px;
  }
}

.csp-checkbox:not(.csp-checkbox--disabled) {
  &:hover .csp-checkbox__control {
    background: var(--background-default-grey-hover);

    &[data-state='checked'],
    &[data-state='indeterminate'] {
      background: var(--background-active-blue-france-hover);
    }
  }

  &:active .csp-checkbox__control {
    background: var(--background-default-grey-active);

    &[data-state='checked'],
    &[data-state='indeterminate'] {
      background: var(--background-active-blue-france-active);
    }
  }
}

.csp-checkbox--error .csp-checkbox__control {
  border-color: var(--border-plain-error);
}

.csp-checkbox__control[data-disabled] {
  border-color: var(--border-disabled-grey);

  &[data-state='checked'],
  &[data-state='indeterminate'] {
    background: var(--background-disabled-grey);
  }
}

.csp-checkbox__indicator {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 100%;
  height: 100%;
  color: var(--text-inverted-blue-france);

  &[data-disabled] {
    color: var(--text-disabled-grey);
  }

  &[data-state='unchecked'] {
    visibility: hidden;
  }

  &[data-state='checked']::after {
    content: '';
    display: block;
    width: var(--csp-checkbox-indicator-check-w);
    height: var(--csp-checkbox-indicator-check-h);
    border: 2px solid currentColor;
    border-top: none;
    border-left: none;
    transform: rotate(45deg) translate(-1px, -1px);
  }

  &[data-state='indeterminate']::after {
    content: '';
    display: block;
    width: var(--csp-checkbox-indicator-dash-w);
    height: 0;
    border-bottom: 2px solid currentColor;
  }
}

.csp-checkbox__text {
  display: flex;
  flex-direction: column;
  gap: var(--csp-field-hint-gap);
}

.csp-checkbox__label {
  line-height: 1.25;
  user-select: none;
}

.csp-checkbox__hint {
  font-size: 0.75rem;
  color: var(--text-mention-grey);
  user-select: none;
}

.csp-checkbox--disabled .csp-checkbox__hint {
  color: var(--text-disabled-grey);
}
</style>
