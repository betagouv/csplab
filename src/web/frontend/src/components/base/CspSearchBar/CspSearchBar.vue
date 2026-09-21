<script setup lang="ts">
import { useId } from 'vue'
import CspButton from '@/components/base/CspButton/CspButton.vue'
import CspIcon from '@/components/base/CspIcon/CspIcon.vue'

export interface CspSearchBarProps {
  label: string
  mode?: 'submit' | 'live'
  hideLabel?: boolean
  hint?: string
  placeholder?: string
  size?: 'md' | 'lg'
  disabled?: boolean
  error?: boolean
  errorMessage?: string
  buttonLabel?: string
  id?: string
  name?: string
}

const props = withDefaults(defineProps<CspSearchBarProps>(), {
  mode: 'submit',
  hideLabel: false,
  size: 'md',
  disabled: false,
  error: false,
  buttonLabel: 'Rechercher',
  id: () => useId(),
})

const emit = defineEmits<{
  search: [value: string]
}>()

const model = defineModel<string>({ default: '' })

function submit() {
  if (props.disabled) {
    return
  }
  emit('search', model.value.trim())
}
</script>

<template>
  <div
    class="csp-search-bar"
    :class="[
      `csp-search-bar--${size}`,
      `csp-search-bar--${mode}`,
      { 'csp-search-bar--error': error },
    ]"
    role="search"
  >
    <label
      class="csp-search-bar__label"
      :class="{ 'csp-search-bar__label--hidden': hideLabel }"
      :for="id"
    >
      {{ label }}
      <span
        v-if="hint"
        class="csp-search-bar__hint"
      >
        {{ hint }}
      </span>
    </label>
    <div class="csp-search-bar__field">
      <CspIcon
        v-if="mode === 'live'"
        name="ri:search-line"
        class="csp-search-bar__icon"
        aria-hidden="true"
      />
      <input
        :id="id"
        v-model="model"
        class="csp-search-bar__input"
        type="search"
        :name="name"
        :placeholder="placeholder"
        :disabled="disabled"
        :aria-invalid="error || undefined"
        :aria-describedby="`${id}-messages`"
        autocomplete="off"
        @keydown.enter.prevent="submit"
      >
      <CspButton
        v-if="mode === 'submit' && size === 'lg'"
        class="csp-search-bar__button"
        :label="buttonLabel"
        icon="ri:search-line"
        is-icon-left
        :disabled="disabled"
        @click="submit"
      />
      <CspButton
        v-else-if="mode === 'submit'"
        class="csp-search-bar__button"
        icon="ri:search-line"
        :aria-label="buttonLabel"
        :title="buttonLabel"
        :disabled="disabled"
        @click="submit"
      />
    </div>
    <div
      :id="`${id}-messages`"
      class="csp-search-bar__messages"
      aria-live="polite"
    >
      <p
        v-if="error && errorMessage"
        class="csp-search-bar__error"
      >
        {{ errorMessage }}
      </p>
    </div>
  </div>
</template>

<style scoped lang="scss">
.csp-search-bar {
  display: flex;
  flex-direction: column;
  gap: 0.375rem;
  min-width: 0;
}

.csp-search-bar__label {
  display: flex;
  flex-direction: column;
  gap: 0.125rem;
  font-size: 0.875rem;
  font-weight: 600;
  color: var(--text-default-grey);
}

.csp-search-bar__label--hidden {
  position: absolute;
  width: 1px;
  height: 1px;
  overflow: hidden;
  clip: rect(0 0 0 0);
  white-space: nowrap;
}

.csp-search-bar__hint {
  font-size: 0.75rem;
  font-weight: 400;
  color: var(--text-mention-grey);
}

.csp-search-bar__field {
  position: relative;
  display: flex;
  align-items: stretch;
}

.csp-search-bar__icon {
  position: absolute;
  z-index: 1;
  top: 50%;
  left: 0.875em;
  color: var(--text-mention-grey);
  pointer-events: none;
  transform: translateY(-50%);
}

.csp-search-bar__input {
  flex: 1;
  min-width: 0;
  appearance: none;
  border: none;
  border-radius: 0.25rem 0 0 0.25rem;
  background-color: var(--background-default-grey);
  color: var(--text-default-grey);
  box-shadow: inset 0 0 0 1px var(--border-default-grey);
  font-size: 0.875rem;
  line-height: 1.25;
  padding: 0.625em 0.875em;

  .csp-search-bar--lg & {
    font-size: 1rem;
  }

  .csp-search-bar--live & {
    border-radius: 0.25rem;
    padding-left: 2.5em;
  }

  .csp-search-bar--error & {
    box-shadow: inset 0 0 0 1px var(--border-plain-error);
  }

  &:focus-visible {
    outline: 2px solid var(--csp-focus-ring-color);
    outline-offset: 2px;
    position: relative;
  }

  &:disabled {
    background-color: var(--background-disabled-grey);
    color: var(--text-disabled-grey);
    box-shadow: inset 0 0 0 1px var(--border-disabled-grey);
  }

  &::placeholder {
    color: var(--text-mention-grey);
  }

  &::-webkit-search-decoration,
  &::-webkit-search-cancel-button {
    appearance: none;
  }
}

.csp-search-bar__button {
  flex-shrink: 0;
  border-radius: 0 0.25rem 0.25rem 0;
}

.csp-search-bar__messages:empty {
  display: none;
}

.csp-search-bar__error {
  margin: 0;
  font-size: 0.75rem;
  color: var(--text-default-error);
}
</style>
