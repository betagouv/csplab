<script setup lang="ts">
import { nextTick, ref, useId } from 'vue'
import CspButton from '@/components/base/CspButton/CspButton.vue'
import CspInput from '@/components/base/CspInput/CspInput.vue'
import FieldLabel from './FieldLabel.vue'

// Liste de libellés éditable : ajout, modification en place, suppression.
const props = withDefaults(defineProps<{
  label: string
  hint?: string
  path?: string
  placeholder?: string
  addLabel?: string
  disabled?: boolean
}>(), {
  hint: undefined,
  path: undefined,
  placeholder: 'Saisir puis Entrée',
  addLabel: 'Ajouter',
  disabled: false,
})

const items = defineModel<string[]>({ required: true })
const draft = ref('')
const inputId = useId()

function ajouter() {
  const v = draft.value.trim()
  if (!v) {
    return
  }
  items.value = [...items.value, v]
  draft.value = ''
}

function modifier(index: number, valeur: string) {
  const copie = [...items.value]
  copie[index] = valeur
  items.value = copie
}

function supprimer(index: number) {
  items.value = items.value.filter((_, i) => i !== index)
  nextTick(() => document.getElementById(inputId)?.focus())
}
</script>

<template>
  <div class="list-editor">
    <FieldLabel
      :label="label"
      :hint="hint"
      :path="path"
      tag="span"
    />
    <ul
      v-if="items.length"
      class="list-editor__list"
    >
      <li
        v-for="(item, index) in items"
        :key="index"
        class="list-editor__item"
      >
        <span
          class="list-editor__bullet"
          aria-hidden="true"
        >{{ index + 1 }}</span>
        <input
          class="list-editor__input"
          :value="item"
          :aria-label="`${label} ${index + 1}`"
          :disabled="props.disabled"
          @change="modifier(index, ($event.target as HTMLInputElement).value)"
        >
        <CspButton
          v-if="!props.disabled"
          icon="ri:delete-bin-line"
          variant="tertiary-no-outline"
          size="sm"
          :aria-label="`Supprimer « ${item} »`"
          @click="supprimer(index)"
        />
      </li>
    </ul>
    <p
      v-else
      class="list-editor__empty"
    >
      Aucun élément pour l'instant.
    </p>
    <form
      v-if="!props.disabled"
      class="list-editor__add"
      @submit.prevent="ajouter"
    >
      <CspInput
        :id="inputId"
        v-model="draft"
        :placeholder="placeholder"
        size="sm"
        :aria-label="`Nouvel élément : ${label}`"
      />
      <CspButton
        type="submit"
        :label="addLabel"
        icon="ri:add-line"
        is-icon-left
        variant="secondary"
        size="sm"
        :disabled="!draft.trim()"
      />
    </form>
  </div>
</template>

<style scoped lang="scss">
.list-editor {
  display: flex;
  flex-direction: column;
  gap: var(--csp-space-2);
}

.list-editor__list {
  margin: 0;
  padding: 0;
  list-style: none;
  border: 1px solid var(--border-default-grey);
}

.list-editor__item {
  display: flex;
  align-items: center;
  gap: var(--csp-space-2);
  padding: var(--csp-space-1) var(--csp-space-2);

  & + & {
    border-top: 1px solid var(--border-default-grey);
  }
}

.list-editor__bullet {
  flex-shrink: 0;
  width: 1.25rem;
  font-size: var(--csp-font-size-xs);
  color: var(--text-mention-grey);
  text-align: right;
}

.list-editor__input {
  flex: 1;
  min-width: 0;
  padding: var(--csp-space-1) var(--csp-space-2);
  border: 1px solid transparent;
  background: transparent;
  font: inherit;
  font-size: var(--csp-font-size-sm);
  color: var(--text-default-grey);

  &:hover:not(:disabled) {
    border-color: var(--border-default-grey);
  }

  &:focus-visible {
    outline: 2px solid var(--csp-focus-ring-color, #0a76f6);
    outline-offset: 0;
    background: var(--background-default-grey);
  }
}

.list-editor__empty {
  margin: 0;
  font-size: var(--csp-font-size-sm);
  color: var(--text-mention-grey);
  font-style: italic;
}

.list-editor__add {
  display: flex;
  gap: var(--csp-space-2);
  align-items: flex-start;

  > :first-child {
    flex: 1;
  }
}
</style>
