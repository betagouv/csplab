<script setup lang="ts">
import { useAttrs, useId } from 'vue'
import CspIcon from '@/components/base/CspIcon/CspIcon.vue'

export interface CspTextareaProps {
  placeholder?: string
  rows?: number
  disabled?: boolean
  error?: boolean
  errorMessage?: string
  resize?: 'none' | 'vertical' | 'horizontal' | 'both'
  id?: string
  label?: string
}

defineOptions({
  inheritAttrs: false,
})

const props = withDefaults(defineProps<CspTextareaProps>(), {
  rows: 4,
  disabled: false,
  error: false,
  resize: 'vertical',
  id: () => useId(),
  label: undefined,
})

const model = defineModel<string>({ default: '' })

const attrs = useAttrs()
</script>

<template>
  <div
    class="csp-textarea-group"
    :class="{ 'csp-textarea-group--error': error }"
  >
    <label
      v-if="label"
      class="csp-textarea-group__label"
      :for="id"
    >
      {{ label }}
    </label>
    <textarea
      v-bind="attrs"
      :id="id"
      v-model="model"
      class="csp-textarea"
      :class="[
        `csp-textarea--resize-${props.resize}`,
        {
          'csp-textarea--error': props.error,
        },
      ]"
      :placeholder="props.placeholder"
      :rows="props.rows"
      :disabled="props.disabled"
      :aria-invalid="error || undefined"
    />
    <p
      v-if="error && errorMessage"
      class="csp-textarea-group__error"
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
.csp-textarea {
  width: 100%;
  appearance: none;

  padding: var(--csp-textarea-padding-y) var(--csp-textarea-padding-x);
  border-radius: 0.25rem;
  background-color: var(--csp-textarea-bg);
  color: var(--csp-textarea-text);
  font-family: inherit;
  line-height: 1.25;

  box-shadow: inset 0 0 0 1px var(--csp-textarea-border);
  border: none;

  resize: var(--csp-textarea-resize);
  min-height: calc(2lh + (2 * var(--csp-textarea-padding-y)));

  font-size: 0.875rem;

  --csp-textarea-padding-y: 0.625em;
  --csp-textarea-padding-x: 0.875em;
  --csp-textarea-bg: var(--background-default-grey);
  --csp-textarea-text: var(--text-default-grey);
  --csp-textarea-border: var(--border-default-grey);
  --csp-textarea-resize: vertical;

  &::placeholder {
    color: var(--text-mention-grey);
  }

  &:focus-visible {
    outline: 2px solid var(--csp-focus-ring-color);
    outline-offset: 2px;
  }

  &:disabled {
    pointer-events: none;
    background-color: var(--background-disabled-grey);
    box-shadow: inset 0 0 0 1px var(--border-disabled-grey);
    color: var(--text-disabled-grey);
  }
}

.csp-textarea--error {
  --csp-textarea-border: var(--border-plain-error);
}

.csp-textarea--resize-none {
  --csp-textarea-resize: none;
}

.csp-textarea--resize-vertical {
  --csp-textarea-resize: vertical;
}

.csp-textarea--resize-horizontal {
  --csp-textarea-resize: horizontal;
}

.csp-textarea--resize-both {
  --csp-textarea-resize: both;
}

.csp-textarea-group {
  display: flex;
  flex-direction: column;
  gap: 0.375rem;
}

.csp-textarea-group__label {
  font-size: 0.875rem;
  font-weight: 600;
  color: var(--text-default-grey);
}

.csp-textarea-group--error {
  border-left: 2px solid var(--border-plain-error);
  padding-left: 0.75rem;

  .csp-textarea-group__label {
    color: var(--text-default-error);
  }
}

.csp-textarea-group__error {
  display: flex;
  align-items: center;
  gap: 0.375rem;
  color: var(--text-default-error);
  font-size: 0.75rem;
  margin: 0;
}
</style>
