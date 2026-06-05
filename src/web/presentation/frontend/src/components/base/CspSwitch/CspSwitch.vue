<script setup lang="ts">
import { SwitchRoot, SwitchThumb } from 'reka-ui'
import { useId } from 'vue'

export interface CspSwitchProps {
  label: string
  disabled?: boolean
  name?: string
  id?: string
  size?: 'sm' | 'md' | 'lg'
  error?: boolean
}

withDefaults(defineProps<CspSwitchProps>(), {
  disabled: false,
  id: () => useId(),
  size: 'md',
  error: false,
})

const model = defineModel<boolean>({ required: true })
</script>

<template>
  <label
    class="csp-switch"
    :class="[
      `csp-switch--${size}`,
      { 'csp-switch--disabled': disabled },
      { 'csp-switch--error': error },
    ]"
  >
    <SwitchRoot
      :id="id"
      v-model="model"
      class="csp-switch__root"
      :disabled="disabled"
      :name="name"
    >
      <SwitchThumb class="csp-switch__thumb" />
    </SwitchRoot>
    <span class="csp-switch__label">{{ label }}</span>
  </label>
</template>

<style scoped lang="scss">
.csp-switch {
  display: inline-flex;
  align-items: center;
  gap: var(--csp-switch-gap);
  cursor: pointer;
  font-size: var(--csp-switch-font-size);
  color: var(--csp-switch-color);

  --csp-switch-gap: 0.75rem;
  --csp-switch-font-size: 0.875rem;
  --csp-switch-color: var(--text-default-grey);
  --csp-switch-track-width: 2.75rem;
  --csp-switch-track-height: 1.5rem;
  --csp-switch-thumb-size: 1.125rem;
}

.csp-switch--disabled {
  cursor: not-allowed;
  color: var(--text-disabled-grey);
}

.csp-switch--error {
  --csp-switch-color: var(--text-default-error);

  .csp-switch__root {
    box-shadow:
      0 0 0 2px white,
      0 0 0 4px var(--border-plain-error);
  }
}

.csp-switch--sm {
  --csp-switch-gap: 0.5rem;
  --csp-switch-font-size: 0.75rem;
  --csp-switch-track-width: 2.25rem;
  --csp-switch-track-height: 1.125rem;
  --csp-switch-thumb-size: 0.75rem;
}

.csp-switch--lg {
  --csp-switch-gap: 0.875rem;
  --csp-switch-font-size: 1rem;
  --csp-switch-track-width: 3.5rem;
  --csp-switch-track-height: 2rem;
  --csp-switch-thumb-size: 1.5rem;
}

.csp-switch__root {
  position: relative;
  display: inline-flex;
  align-items: center;
  flex-shrink: 0;
  width: var(--csp-switch-track-width);
  height: var(--csp-switch-track-height);
  border-radius: calc(var(--csp-switch-track-height) / 2);
  background: var(--border-default-grey);
  border: none;
  padding: 0;
  cursor: inherit;
  transition: background-color 0.2s ease;

  &[data-state='checked'] {
    background: var(--background-action-high-blue-france);
  }

  &[data-disabled] {
    background: var(--background-disabled-grey);
  }

  &:focus-visible {
    outline: 2px solid var(--csp-focus-ring-color);
    outline-offset: 2px;
  }
}

.csp-switch__thumb {
  display: block;
  width: var(--csp-switch-thumb-size);
  height: var(--csp-switch-thumb-size);
  border-radius: 50%;
  background: white;
  box-shadow: 0 1px 2px rgb(0 0 0 / 20%);
  transition: transform 0.2s ease;
  transform: translateX(calc((var(--csp-switch-track-height) - var(--csp-switch-thumb-size)) / 2));
  will-change: transform;

  &[data-state='checked'] {
    transform: translateX(
      calc(
        var(--csp-switch-track-width) - var(--csp-switch-thumb-size) -
          (var(--csp-switch-track-height) - var(--csp-switch-thumb-size)) / 2
      )
    );
  }
}

.csp-switch__label {
  line-height: 1.25;
  user-select: none;
}
</style>
