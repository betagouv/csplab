<script setup lang="ts">
import { RadioGroupIndicator, RadioGroupItem } from 'reka-ui'

export type CspRadioSize = 'sm' | 'md' | 'lg'

export interface CspRadioProps {
  value: string
  label: string
  disabled?: boolean
  size?: CspRadioSize
  error?: boolean
}

withDefaults(defineProps<CspRadioProps>(), {
  disabled: false,
  size: 'md',
  error: false,
})
</script>

<template>
  <label
    class="csp-radio"
    :class="[
      `csp-radio--${size}`,
      { 'csp-radio--disabled': disabled },
      { 'csp-radio--error': error },
    ]"
  >
    <RadioGroupItem
      class="csp-radio__control"
      :value="value"
      :disabled="disabled"
    >
      <RadioGroupIndicator class="csp-radio__indicator" />
    </RadioGroupItem>
    <span class="csp-radio__label">{{ label }}</span>
  </label>
</template>

<style scoped lang="scss">
.csp-radio {
  display: inline-flex;
  align-items: center;
  gap: var(--csp-radio-gap);
  cursor: pointer;
  font-size: var(--csp-radio-font-size);
  color: var(--csp-radio-color);

  --csp-radio-gap: 0.5rem;
  --csp-radio-font-size: 0.875rem;
  --csp-radio-color: var(--text-default-grey);
  --csp-radio-size: 1.125rem;
  --csp-radio-indicator-size: 0.5rem;
}

.csp-radio--sm {
  --csp-radio-size: 1rem;
  --csp-radio-font-size: 0.75rem;
  --csp-radio-gap: 0.375rem;
  --csp-radio-indicator-size: 0.375rem;
}

.csp-radio--lg {
  --csp-radio-size: 1.375rem;
  --csp-radio-font-size: 1rem;
  --csp-radio-gap: 0.625rem;
  --csp-radio-indicator-size: 0.625rem;
}

.csp-radio--disabled {
  cursor: not-allowed;
  color: var(--text-disabled-grey);
}

.csp-radio--error {
  .csp-radio__control {
    border-color: var(--border-plain-error);
  }
}

.csp-radio__control {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: var(--csp-radio-size);
  height: var(--csp-radio-size);
  flex: 0 0 auto;
  border-radius: 50%;
  border: 1px solid var(--border-default-grey);
  background: transparent;
  padding: 0;
  cursor: inherit;

  &[data-state='checked'] {
    border-color: var(--background-action-high-blue-france);
  }

  &[data-disabled] {
    border-color: var(--border-disabled-grey);
    background: var(--background-disabled-grey);
  }

  &:focus-visible {
    outline: 2px solid var(--csp-focus-ring-color);
    outline-offset: 2px;
  }
}

.csp-radio__indicator {
  display: block;
  width: var(--csp-radio-indicator-size);
  height: var(--csp-radio-indicator-size);
  border-radius: 50%;
  background: var(--background-action-high-blue-france);
}

.csp-radio__label {
  line-height: 1.25;
  user-select: none;
}
</style>
