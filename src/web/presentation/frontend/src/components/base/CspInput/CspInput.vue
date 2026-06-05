<script setup lang="ts">
import { useAttrs, useId } from 'vue'
import CspIcon from '@/components/base/CspIcon/CspIcon.vue'

export interface CspInputProps {
  type?: 'text' | 'email' | 'password' | 'search' | 'tel' | 'url' | 'number'
  placeholder?: string
  size?: 'sm' | 'md' | 'lg'
  disabled?: boolean
  error?: boolean
  errorMessage?: string
  id?: string
  name?: string
  label?: string
}

defineOptions({
  inheritAttrs: false,
})

withDefaults(defineProps<CspInputProps>(), {
  type: 'text',
  size: 'md',
  disabled: false,
  error: false,
  id: () => useId(),
})

const model = defineModel<string>({ default: '' })

const attrs = useAttrs()
</script>

<template>
  <div
    class="csp-input-group"
    :class="{ 'csp-input-group--error': error }"
  >
    <label
      v-if="label"
      class="csp-input-group__label"
      :for="id"
    >
      {{ label }}
    </label>
    <input
      v-bind="attrs"
      :id="id"
      v-model="model"
      :name="name"
      :type="type"
      :placeholder="placeholder"
      :disabled="disabled"
      :aria-invalid="error || undefined"
      class="csp-input"
      :class="[
        `csp-input--${size}`,
        {
          'csp-input--error': error,
        },
      ]"
    >
    <p
      v-if="error && errorMessage"
      class="csp-input-group__error"
      role="alert"
    >
      <CspIcon
        name="ri:error-warning-fill"
        :size="14"
      />
      {{ errorMessage }}
    </p>
  </div>
</template>

<style scoped lang="scss">
.csp-input {
  width: 100%;
  appearance: none;
  background-color: var(--csp-input-bg);
  color: var(--csp-input-text);
  box-shadow: inset 0 0 0 1px var(--csp-input-border);
  border: none;
  border-radius: 0.25rem;

  font-size: var(--csp-input-font-size);
  line-height: 1.25;
  padding: var(--csp-input-padding-y) var(--csp-input-padding-x);

  --csp-input-bg: var(--background-default-grey);
  --csp-input-text: var(--text-default-grey);
  --csp-input-border: var(--border-default-grey);

  &:focus-visible {
    outline: 2px solid var(--csp-focus-ring-color);
    outline-offset: 2px;
  }

  &:disabled {
    pointer-events: none;
    background-color: var(--background-disabled-grey);
    color: var(--text-disabled-grey);
    box-shadow: inset 0 0 0 1px var(--border-disabled-grey);
  }

  &::placeholder {
    color: var(--text-mention-grey);
  }
}

.csp-input--error {
  --csp-input-border: var(--border-plain-error);
}

.csp-input--sm {
  font-size: 0.825rem;

  --csp-input-padding-y: 0.5em;
  --csp-input-padding-x: 0.75em;
}

.csp-input--md {
  font-size: 0.875rem;

  --csp-input-padding-y: 0.625em;
  --csp-input-padding-x: 0.875em;
}

.csp-input--lg {
  font-size: 1rem;

  --csp-input-padding-y: 0.625em;
  --csp-input-padding-x: 0.875em;
}

.csp-input-group {
  display: flex;
  flex-direction: column;
  gap: 0.375rem;
}

.csp-input-group__label {
  font-size: 0.875rem;
  font-weight: 600;
  color: var(--text-default-grey);
}

.csp-input-group--error {
  border-left: 2px solid var(--border-plain-error);
  padding-left: 0.75rem;

  .csp-input-group__label {
    color: var(--text-default-error);
  }
}

.csp-input-group__error {
  display: flex;
  align-items: center;
  gap: 0.375rem;
  color: var(--text-default-error);
  font-size: 0.75rem;
  margin: 0;
}
</style>
