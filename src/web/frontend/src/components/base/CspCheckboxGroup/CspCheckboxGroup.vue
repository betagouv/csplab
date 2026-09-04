<script setup lang="ts">
import { CheckboxGroupRoot } from 'reka-ui'
import CspCheckbox from '@/components/base/CspCheckbox/CspCheckbox.vue'
import CspIcon from '@/components/base/CspIcon/CspIcon.vue'

export interface CspCheckboxGroupOption {
  value: string
  label: string
  disabled?: boolean
}

export interface CspCheckboxGroupProps {
  options: CspCheckboxGroupOption[]
  label?: string
  name?: string
  disabled?: boolean
  size?: NonNullable<InstanceType<typeof CspCheckbox>['$props']['size']>
  error?: boolean
  errorMessage?: string
}

withDefaults(defineProps<CspCheckboxGroupProps>(), {
  disabled: false,
  size: 'md',
  error: false,
})

const model = defineModel<string[]>({ required: true })

function updateModel(val: unknown[]): void {
  model.value = val.filter((v): v is string => {
    return typeof v === 'string'
  })
}
</script>

<template>
  <CheckboxGroupRoot
    :model-value="model"
    as="fieldset"
    class="csp-checkbox-group"
    :class="[
      { 'csp-checkbox-group--disabled': disabled },
      { 'csp-checkbox-group--error': error },
    ]"
    :name="name"
    :disabled="disabled"
    @update:model-value="updateModel"
  >
    <legend
      v-if="label"
      class="csp-checkbox-group__legend"
    >
      {{ label }}
    </legend>

    <div class="csp-checkbox-group__items">
      <CspCheckbox
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
      class="csp-checkbox-group__error"
      role="alert"
    >
      <CspIcon
        name="ri:error-warning-fill"
        :size="14"
      />
      {{ errorMessage }}
    </p>
  </CheckboxGroupRoot>
</template>

<style scoped lang="scss">
.csp-checkbox-group {
  border: none;
  padding: 0;
  margin: 0;
  min-width: 0;
}

.csp-checkbox-group__legend {
  font-size: 0.875rem;
  font-weight: 600;
  color: var(--text-default-grey);
  margin-bottom: var(--csp-space-3, 0.75rem);
  padding: 0;
}

.csp-checkbox-group__items {
  display: flex;
  flex-direction: column;
  gap: var(--csp-space-2, 0.5rem);
}

.csp-checkbox-group--disabled {
  .csp-checkbox-group__legend {
    color: var(--text-disabled-grey);
  }
}

.csp-checkbox-group--error {
  border-left: 2px solid var(--border-plain-error);
  padding-left: 0.75rem;

  .csp-checkbox-group__legend {
    color: var(--text-default-error);
  }
}

.csp-checkbox-group__error {
  display: flex;
  align-items: center;
  gap: 0.375rem;
  color: var(--text-default-error);
  font-size: 0.75rem;
  margin: 0;
  margin-top: 0.5rem;
}
</style>
