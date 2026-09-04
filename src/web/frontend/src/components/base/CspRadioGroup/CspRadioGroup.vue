<script setup lang="ts">
import type { CspRadioSize } from '@/components/base/CspRadio/CspRadio.vue'
import { RadioGroupRoot } from 'reka-ui'
import CspIcon from '@/components/base/CspIcon/CspIcon.vue'
import CspRadio from '@/components/base/CspRadio/CspRadio.vue'

export interface CspRadioGroupOption {
  value: string
  label: string
  disabled?: boolean
}

export interface CspRadioGroupProps {
  options: CspRadioGroupOption[]
  label?: string
  name?: string
  disabled?: boolean
  size?: CspRadioSize
  error?: boolean
  errorMessage?: string
}

withDefaults(defineProps<CspRadioGroupProps>(), {
  label: undefined,
  name: undefined,
  disabled: false,
  size: 'md',
  error: false,
  errorMessage: undefined,
})

const model = defineModel<string>({ required: true })

function updateModel(val: unknown): void {
  if (typeof val === 'string')
    model.value = val
}
</script>

<template>
  <RadioGroupRoot
    :model-value="model"
    as="fieldset"
    class="csp-radio-group"
    :class="{ 'csp-radio-group--disabled': disabled, 'csp-radio-group--error': error }"
    :name="name"
    :disabled="disabled"
    orientation="vertical"
    @update:model-value="updateModel"
  >
    <legend
      v-if="label"
      class="csp-radio-group__legend"
    >
      {{ label }}
    </legend>

    <div class="csp-radio-group__items">
      <CspRadio
        v-for="option in options"
        :key="option.value"
        :value="option.value"
        :label="option.label"
        :disabled="disabled || option.disabled"
        :size="size"
        :error="error"
      />
    </div>

    <p
      v-if="error && errorMessage"
      class="csp-radio-group__error"
      role="alert"
    >
      <CspIcon
        name="ri:error-warning-fill"
        :size="14"
      />
      {{ errorMessage }}
    </p>
  </RadioGroupRoot>
</template>

<style scoped lang="scss">
.csp-radio-group {
  border: none;
  padding: 0;
  margin: 0;
  min-width: 0;
}

.csp-radio-group__legend {
  font-size: 0.875rem;
  font-weight: 600;
  color: var(--text-default-grey);
  margin-bottom: var(--csp-space-3, 0.75rem);
  padding: 0;
}

.csp-radio-group__items {
  display: flex;
  flex-direction: column;
  gap: var(--csp-space-2, 0.5rem);
}

.csp-radio-group--disabled {
  .csp-radio-group__legend {
    color: var(--text-disabled-grey);
  }
}

.csp-radio-group--error {
  border-left: 4px solid var(--border-plain-error);
  padding-left: 1rem;

  .csp-radio-group__legend {
    color: var(--text-default-error);
  }
}

.csp-radio-group__error {
  display: flex;
  align-items: center;
  gap: 0.375rem;
  color: var(--text-default-error);
  font-size: 0.75rem;
  margin: 0;
  margin-top: 0.5rem;
}
</style>
