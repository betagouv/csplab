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

function displayValue(value: unknown): string {
  if (value == null) {
    return ''
  }
  return props.options.find(option => option.value === value)?.label ?? searchTerm.value
}

const statusMessage = computed(() => {
  if (!open.value || props.pending) {
    return ''
  }
  const count = props.options.length
  if (count === 0) {
    return props.actionLabel ?? props.emptyLabel
  }
  return `${count} ${pluralize(count, 'résultat')}`
})

const announcedStatus = useDebounce(statusMessage, 1000)
</script>

<template>
  <ComboboxRoot
    v-model="model"
    v-model:open="open"
    ignore-filter
    open-on-focus
    open-on-click
    class="csp-combobox"
  >
    <label
      class="csp-combobox__label"
      :for="id"
    >
      {{ label }}
      <span
        v-if="hint"
        class="csp-combobox__hint"
      >
        {{ hint }}
      </span>
    </label>

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
        autocomplete="off"
        :display-value="displayValue"
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
      class="sr-only"
      role="status"
    >
      {{ announcedStatus }}
    </span>
  </ComboboxRoot>
</template>

<style scoped lang="scss">
@use '@/styles/search';

// ComboboxRoot's DOM element does not receive Vue's scoped attribute, so the
// root layout rule must be global to apply.
:global(.csp-combobox) {
  display: flex;
  flex-direction: column;
  gap: var(--csp-field-label-gap);
}

.csp-combobox__label {
  display: flex;
  flex-direction: column;
  gap: var(--csp-field-hint-gap);
  font-size: 0.875rem;
  font-weight: 600;
  color: var(--text-default-grey);
}

.csp-combobox__hint {
  font-size: 0.75rem;
  font-weight: 400;
  color: var(--text-mention-grey);
}

.csp-combobox__anchor {
  @include search.field;
}

.csp-combobox__search-icon {
  @include search.icon;

  width: 1rem;
  height: 1rem;
}

.csp-combobox__input {
  @include search.input;

  width: 100%;
}
</style>

<style lang="scss">
@use '@/styles/menu';

.csp-combobox-content {
  width: var(--reka-combobox-trigger-width);
  max-height: var(--reka-combobox-content-available-height, 20rem);
  background-color: var(--background-overlap-grey);
  border-radius: 0.25rem;
  box-shadow:
    inset 0 0 0 1px var(--border-default-grey),
    var(--csp-overlap-shadow);
  overflow: hidden;
  z-index: var(--csp-z-dropdown);
  transform-origin: var(--reka-popper-transform-origin);

  &[data-state='open'] {
    animation: var(--csp-motion-overlap-enter);
  }

  &[data-state='closed'] {
    animation: var(--csp-motion-overlap-exit);
  }
}

.csp-combobox-content__viewport {
  padding: var(--csp-menu-padding);
}

.csp-combobox-content__empty {
  padding: var(--csp-space-3);
  font-size: 0.875rem;
  color: var(--text-mention-grey);
}

.csp-combobox-content__item {
  @include menu.item;

  flex-direction: column;
  align-items: stretch;
  gap: 0.125rem;
  font-size: 0.875rem;
  line-height: 1.25;
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
  gap: var(--csp-menu-item-gap);
  color: var(--text-action-high-blue-france);
  font-weight: 500;
}

.csp-combobox-content__separator {
  @include menu.separator;
}
</style>
