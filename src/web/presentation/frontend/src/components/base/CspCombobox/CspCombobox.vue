<script setup lang="ts">
import {
  ComboboxAnchor,
  ComboboxContent,
  ComboboxEmpty,
  ComboboxInput,
  ComboboxItem,
  ComboboxPortal,
  ComboboxRoot,
  ComboboxSeparator,
  ComboboxViewport,
} from 'reka-ui'
import { computed, useId } from 'vue'
import CspIcon from '@/components/base/CspIcon/CspIcon.vue'
import { useDebounce } from '@/composables/async/useDebounce'
import { pluralize } from '@/utils/format'

export interface CspComboboxOption {
  value: string
  label: string
  description?: string
}

const props = withDefaults(defineProps<{
  options: CspComboboxOption[]
  label: string
  hint?: string
  placeholder?: string
  name?: string
  pending?: boolean
  emptyLabel?: string
  actionLabel?: string | null
  actionIcon?: string
  id?: string
}>(), {
  hint: undefined,
  placeholder: undefined,
  name: undefined,
  pending: false,
  emptyLabel: 'Aucun résultat',
  actionLabel: null,
  actionIcon: 'ri:add-line',
  id: () => useId(),
})

const emit = defineEmits<{
  action: []
}>()

const model = defineModel<string | null>({ default: null })
const searchTerm = defineModel<string>('searchTerm', { default: '' })
const open = defineModel<boolean>('open', { default: false })

const hintId = computed(() => `${props.id}-hint`)

const statusMessage = computed(() => {
  if (!open.value || props.pending)
    return ''
  const count = props.options.length
  if (count === 0)
    return props.actionLabel ?? props.emptyLabel
  return `${count} ${pluralize(count, 'résultat')}`
})

const announcedStatus = useDebounce(statusMessage, 1000)
</script>

<template>
  <ComboboxRoot
    v-model="model"
    v-model:open="open"
    ignore-filter
    class="csp-combobox"
  >
    <label
      class="csp-combobox__label"
      :for="id"
    >
      {{ label }}
    </label>
    <p
      v-if="hint"
      :id="hintId"
      class="csp-combobox__hint"
    >
      {{ hint }}
    </p>

    <ComboboxAnchor class="csp-combobox__anchor">
      <CspIcon
        class="csp-combobox__search-icon"
        name="ri:search-line"
      />
      <ComboboxInput
        :id="id"
        v-model="searchTerm"
        class="csp-combobox__input"
        :name="name"
        :placeholder="placeholder"
        :aria-describedby="hint ? hintId : undefined"
        autocomplete="off"
      />
    </ComboboxAnchor>

    <ComboboxPortal>
      <ComboboxContent
        class="csp-combobox-content"
        position="popper"
        :side-offset="4"
      >
        <ComboboxViewport class="csp-combobox-content__viewport">
          <ComboboxEmpty
            v-if="!actionLabel"
            class="csp-combobox-content__empty"
          >
            {{ pending ? 'Chargement…' : emptyLabel }}
          </ComboboxEmpty>

          <ComboboxItem
            v-for="option in options"
            :key="option.value"
            class="csp-combobox-content__item"
            :value="option.value"
          >
            <span class="csp-combobox-content__item-label">{{ option.label }}</span>
            <span
              v-if="option.description"
              class="csp-combobox-content__item-description"
            >
              {{ option.description }}
            </span>
          </ComboboxItem>

          <template v-if="actionLabel">
            <ComboboxSeparator
              v-if="options.length > 0"
              class="csp-combobox-content__separator"
            />
            <ComboboxItem
              class="csp-combobox-content__item csp-combobox-content__item--action"
              value="__action__"
              @select.prevent="emit('action')"
            >
              <CspIcon
                :name="actionIcon"
                :size="16"
              />
              <span>{{ actionLabel }}</span>
            </ComboboxItem>
          </template>
        </ComboboxViewport>
      </ComboboxContent>
    </ComboboxPortal>

    <span
      class="csp-combobox__status"
      role="status"
    >
      {{ announcedStatus }}
    </span>
  </ComboboxRoot>
</template>

<style scoped lang="scss">
.csp-combobox {
  display: flex;
  flex-direction: column;
  gap: 0.375rem;
}

.csp-combobox__label {
  font-size: 0.875rem;
  font-weight: 600;
  color: var(--text-default-grey);
}

.csp-combobox__hint {
  margin: 0;
  font-size: 0.75rem;
  color: var(--text-mention-grey);
}

.csp-combobox__anchor {
  position: relative;
  display: flex;
  align-items: center;
}

.csp-combobox__search-icon {
  position: absolute;
  left: 0.75rem;
  width: 1rem;
  height: 1rem;
  color: var(--text-mention-grey);
  pointer-events: none;
}

.csp-combobox__input {
  width: 100%;
  appearance: none;
  background-color: var(--background-default-grey);
  color: var(--text-default-grey);
  box-shadow: inset 0 0 0 1px var(--border-default-grey);
  border: none;
  border-radius: 0.25rem;
  font-size: 0.875rem;
  line-height: 1.25;
  padding: 0.625em 0.875em 0.625em 2.5em;

  &::placeholder {
    color: var(--text-mention-grey);
  }

  &:focus-visible {
    outline: 2px solid var(--csp-focus-ring-color);
    outline-offset: 2px;
  }
}

.csp-combobox__status {
  position: absolute;
  width: 1px;
  height: 1px;
  overflow: hidden;
  clip-path: inset(50%);
  white-space: nowrap;
}
</style>

<style lang="scss">
.csp-combobox-content {
  width: var(--reka-combobox-trigger-width);
  max-height: var(--reka-combobox-content-available-height, 20rem);
  background-color: var(--background-overlap-grey);
  border-radius: 0.25rem;
  box-shadow:
    inset 0 0 0 1px var(--border-default-grey),
    var(--csp-shadow-md);
  overflow: hidden;
  z-index: var(--csp-z-dropdown);
}

.csp-combobox-content__viewport {
  padding: 0.25rem;
}

.csp-combobox-content__empty {
  padding: 0.75rem;
  font-size: 0.875rem;
  color: var(--text-mention-grey);
}

.csp-combobox-content__item {
  display: flex;
  flex-direction: column;
  gap: 0.125rem;
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
}

.csp-combobox-content__item-label {
  font-weight: 500;
}

.csp-combobox-content__item-description {
  font-size: 0.8125rem;
  color: var(--text-mention-grey);
}

.csp-combobox-content__item--action {
  flex-direction: row;
  align-items: center;
  gap: 0.5rem;
  color: var(--text-action-high-blue-france);
  font-weight: 500;
}

.csp-combobox-content__separator {
  height: 1px;
  margin: 0.25rem 0;
  background-color: var(--border-default-grey);
}
</style>
