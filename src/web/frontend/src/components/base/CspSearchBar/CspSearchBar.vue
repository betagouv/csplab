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
      :class="{ 'sr-only': hideLabel }"
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
        <CspIcon
          name="ri:error-warning-fill"
          :size="14"
        />
        {{ errorMessage }}
      </p>
    </div>
  </div>
</template>

<style scoped lang="scss">
@use '@/styles/search';

.csp-search-bar {
  display: flex;
  flex-direction: column;
  min-width: 0;
}

.csp-search-bar--error {
  border-inline-start: var(--csp-field-error-bar-width) solid var(--border-plain-error);
  padding-inline-start: var(--csp-field-error-padding-start);

  .csp-search-bar__label {
    color: var(--text-default-error);
  }
}

.csp-search-bar__label {
  display: flex;
  flex-direction: column;
  gap: var(--csp-field-hint-gap);
  margin-bottom: var(--csp-field-label-gap);
  font-size: 0.875rem;
  font-weight: 600;
  color: var(--text-default-grey);
}

.csp-search-bar__hint {
  font-size: 0.75rem;
  font-weight: 400;
  color: var(--text-mention-grey);
}

.csp-search-bar__field {
  @include search.field;
}

.csp-search-bar__icon {
  @include search.icon;
}

.csp-search-bar__input {
  @include search.input;

  .csp-search-bar--submit & {
    border-radius: 0.25rem 0 0 0.25rem;
    padding-left: 0.875em;
  }

  .csp-search-bar--lg & {
    font-size: 1rem;
  }

  .csp-search-bar--error & {
    box-shadow: inset 0 0 0 1px var(--border-plain-error);
  }

  &:disabled {
    background-color: var(--background-disabled-grey);
    color: var(--text-disabled-grey);
    box-shadow: inset 0 0 0 1px var(--border-disabled-grey);
  }
}

.csp-search-bar__button {
  flex-shrink: 0;
  border-radius: 0 0.25rem 0.25rem 0;
}

.csp-search-bar__messages:not(:empty) {
  margin-top: var(--csp-field-messages-gap);
}

.csp-search-bar__error {
  display: flex;
  align-items: center;
  gap: 0.375rem;
  color: var(--text-default-error);
  font-size: 0.75rem;
  margin: 0;
}
</style>
