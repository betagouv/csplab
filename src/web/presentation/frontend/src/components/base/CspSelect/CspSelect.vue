<script setup lang="ts">
import {
  SelectContent,
  SelectItem,
  SelectItemIndicator,
  SelectItemText,
  SelectPortal,
  SelectRoot,
  SelectScrollDownButton,
  SelectScrollUpButton,
  SelectTrigger,
  SelectValue,
  SelectViewport,
} from 'reka-ui'
import { useId } from 'vue'
import CspIcon from '@/components/base/CspIcon/CspIcon.vue'

export interface CspSelectOption {
  value: string
  label: string
  disabled?: boolean
}

withDefaults(defineProps<{
  options: {
    value: string
    label: string
    disabled?: boolean
  }[]
  placeholder?: string
  size?: 'sm' | 'md' | 'lg'
  disabled?: boolean
  error?: boolean
  errorMessage?: string
  id?: string
  label?: string
}>(), {
  placeholder: 'Sélectionner…',
  size: 'md',
  disabled: false,
  error: false,
  id: () => useId(),
})

const model = defineModel<string>()
</script>

<template>
  <div
    class="csp-select-group"
    :class="{ 'csp-select-group--error': error }"
  >
    <label
      v-if="label"
      class="csp-select-group__label"
      :for="id"
    >
      {{ label }}
    </label>

    <SelectRoot
      v-model="model"
      :disabled="disabled"
    >
      <SelectTrigger
        :id="id"
        class="csp-select"
        :class="[
          `csp-select--${size}`,
          { 'csp-select--error': error },
        ]"
        :aria-invalid="error || undefined"
      >
        <SelectValue :placeholder="placeholder" />
        <CspIcon
          class="csp-select__chevron"
          name="ri:arrow-down-s-line"
        />
      </SelectTrigger>

      <SelectPortal>
        <SelectContent
          class="csp-select-content"
          position="popper"
          :side-offset="4"
        >
          <SelectScrollUpButton class="csp-select-content__scroll-btn">
            <CspIcon name="ri:arrow-up-s-line" />
          </SelectScrollUpButton>

          <SelectViewport class="csp-select-content__viewport">
            <SelectItem
              v-for="option in options"
              :key="option.value"
              class="csp-select-content__item"
              :value="option.value"
              :disabled="option.disabled"
            >
              <SelectItemText>{{ option.label }}</SelectItemText>
              <SelectItemIndicator class="csp-select-content__item-indicator">
                <CspIcon name="ri:check-line" />
              </SelectItemIndicator>
            </SelectItem>
          </SelectViewport>

          <SelectScrollDownButton class="csp-select-content__scroll-btn">
            <CspIcon name="ri:arrow-down-s-line" />
          </SelectScrollDownButton>
        </SelectContent>
      </SelectPortal>
    </SelectRoot>

    <p
      v-if="error && errorMessage"
      class="csp-select-group__error"
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
.csp-select {
  display: flex;
  width: 100%;
  align-items: center;
  justify-content: space-between;
  gap: 0.5rem;
  appearance: none;
  background-color: var(--background-default-grey);
  color: var(--text-default-grey);
  box-shadow: inset 0 0 0 1px var(--border-default-grey);
  border: none;
  border-radius: 0.25rem;
  font-size: var(--csp-select-font-size);
  line-height: 1.25;
  padding: var(--csp-select-padding-y) var(--csp-select-padding-x);
  cursor: pointer;

  &:focus-visible {
    outline: 2px solid var(--csp-focus-ring-color);
    outline-offset: 2px;
  }

  &[data-disabled] {
    cursor: not-allowed;
    background-color: var(--background-disabled-grey);
    color: var(--text-disabled-grey);
    box-shadow: inset 0 0 0 1px var(--border-disabled-grey);
  }

  &[data-placeholder] {
    color: var(--text-mention-grey);
  }
}

.csp-select--error {
  box-shadow: inset 0 0 0 1px var(--border-plain-error);
}

.csp-select--sm {
  font-size: 0.825rem;

  --csp-select-padding-y: 0.5em;
  --csp-select-padding-x: 0.75em;
}

.csp-select--md {
  font-size: 0.875rem;

  --csp-select-padding-y: 0.625em;
  --csp-select-padding-x: 0.875em;
}

.csp-select--lg {
  font-size: 1rem;

  --csp-select-padding-y: 0.625em;
  --csp-select-padding-x: 0.875em;
}

.csp-select__chevron {
  flex: 0 0 auto;
  width: 1.125em;
  height: 1.125em;
  color: var(--text-mention-grey);

  [data-state='open'] & {
    transform: rotate(180deg);
  }
}

.csp-select-group {
  display: flex;
  flex-direction: column;
  gap: 0.375rem;
}

.csp-select-group__label {
  font-size: 0.875rem;
  font-weight: 600;
  color: var(--text-default-grey);
}

.csp-select-group--error {
  border-left: 2px solid var(--border-plain-error);
  padding-left: 0.75rem;

  .csp-select-group__label {
    color: var(--text-default-error);
  }
}

.csp-select-group__error {
  display: flex;
  align-items: center;
  gap: 0.375rem;
  color: var(--text-default-error);
  font-size: 0.75rem;
  margin: 0;
}

:deep {
  .csp-select-content {
    width: var(--reka-select-trigger-width);
    max-height: var(--reka-select-content-available-height);
    background-color: var(--background-overlap-grey);
    border-radius: 0.25rem;
    box-shadow:
      inset 0 0 0 1px var(--border-default-grey),
      var(--csp-shadow-md);
    overflow: hidden;
    z-index: var(--csp-z-dropdown);
  }

  .csp-select-content__viewport {
    padding: 0.25rem;
  }

  .csp-select-content__item {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 0.5rem;
    padding: 0.5rem 0.75rem;
    font-size: 0.875rem;
    line-height: 1.25;
    border-radius: 0.125rem;
    cursor: pointer;
    outline: none;
    color: var(--text-default-grey);
    user-select: none;

    &[data-highlighted] {
      background-color: var(--background-default-grey-hover);
      color: var(--text-action-high-blue-france);
    }

    &[data-disabled] {
      pointer-events: none;
      color: var(--text-disabled-grey);
    }
  }

  .csp-select-content__item-indicator {
    display: flex;
    align-items: center;
    color: var(--text-action-high-blue-france);
    font-size: 1rem;
  }

  .csp-select-content__scroll-btn {
    display: flex;
    align-items: center;
    justify-content: center;
    height: 1.5rem;
    background-color: var(--background-overlap-grey);
    color: var(--text-mention-grey);
    cursor: default;
  }
}
</style>
