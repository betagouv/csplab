<script setup lang="ts">
import { SwitchRoot, SwitchThumb } from 'reka-ui'
import { useId } from 'vue'
import CspIcon from '@/components/base/CspIcon/CspIcon.vue'

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
      <SwitchThumb class="csp-switch__thumb">
        <CspIcon
          v-if="model"
          name="ri:check-line"
          class="csp-switch__icon"
        />
      </SwitchThumb>
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
  --csp-switch-border-color: var(--border-action-high-blue-france);
  --csp-switch-track-width: 2.75rem;
  --csp-switch-track-height: 1.5rem;
  --csp-switch-icon-size: 1rem;
}

.csp-switch--disabled {
  cursor: not-allowed;
  color: var(--text-disabled-grey);

  --csp-switch-border-color: var(--border-disabled-grey);
}

.csp-switch--error {
  --csp-switch-color: var(--text-default-error);

  .csp-switch__root {
    outline: 2px solid var(--border-plain-error);
    outline-offset: 2px;
  }
}

.csp-switch--sm {
  --csp-switch-gap: 0.5rem;
  --csp-switch-font-size: 0.75rem;
  --csp-switch-track-width: 2.25rem;
  --csp-switch-track-height: 1.125rem;
  --csp-switch-icon-size: 0.75rem;
}

.csp-switch--lg {
  --csp-switch-gap: 0.875rem;
  --csp-switch-font-size: 1rem;
  --csp-switch-track-width: 3.5rem;
  --csp-switch-track-height: 2rem;
  --csp-switch-icon-size: 1.25rem;
}

.csp-switch__root {
  position: relative;
  display: inline-flex;
  align-items: center;
  flex-shrink: 0;
  width: var(--csp-switch-track-width);
  height: var(--csp-switch-track-height);
  border-radius: calc(var(--csp-switch-track-height) / 2);
  background: transparent;
  box-shadow: inset 0 0 0 1px var(--csp-switch-border-color);
  border: none;
  padding: 0;
  cursor: inherit;
  transition: background-color 0.2s ease;

  &[data-state='checked'] {
    background: var(--background-active-blue-france);
  }

  &[data-disabled][data-state='checked'] {
    background: var(--background-disabled-grey);
  }

  &:focus-visible {
    outline: 2px solid var(--csp-focus-ring-color);
    outline-offset: 2px;
  }
}

.csp-switch__thumb {
  display: flex;
  align-items: center;
  justify-content: center;
  width: var(--csp-switch-track-height);
  height: var(--csp-switch-track-height);
  border-radius: 50%;
  background: var(--background-default-grey);
  box-shadow: inset 0 0 0 1px var(--csp-switch-border-color);
  color: var(--text-active-blue-france);
  transition: transform 0.2s ease;
  will-change: transform;

  &[data-state='checked'] {
    transform: translateX(calc(var(--csp-switch-track-width) - var(--csp-switch-track-height)));
  }

  &[data-disabled] {
    color: var(--text-disabled-grey);
  }
}

.csp-switch__icon {
  width: var(--csp-switch-icon-size);
  height: var(--csp-switch-icon-size);
  flex-shrink: 0;
}

.csp-switch:not(.csp-switch--disabled) {
  &:hover {
    .csp-switch__root[data-state='checked'] {
      background: var(--background-active-blue-france-hover);
    }

    .csp-switch__thumb {
      background: var(--background-default-grey-hover);
    }
  }

  &:active {
    .csp-switch__root[data-state='checked'] {
      background: var(--background-active-blue-france-active);
    }

    .csp-switch__thumb {
      background: var(--background-default-grey-active);
    }
  }
}

.csp-switch__label {
  line-height: 1.25;
  user-select: none;
}

@media (forced-colors: active) {
  .csp-switch__root,
  .csp-switch__thumb {
    box-sizing: border-box;
    border: 1px solid ButtonText;
  }

  .csp-switch__root[data-state='checked'] {
    border-color: Highlight;
  }

  .csp-switch__thumb {
    margin: -1px;
  }

  .csp-switch--disabled {
    .csp-switch__root,
    .csp-switch__thumb {
      border-color: GrayText;
    }
  }
}
</style>
