<script setup lang="ts">
import type { ProtoCandidature } from '../data/mock'
import { computed, ref } from 'vue'
import CspButton from '@/components/base/CspButton/CspButton.vue'
import CspIcon from '@/components/base/CspIcon/CspIcon.vue'
import CspInput from '@/components/base/CspInput/CspInput.vue'
import CspPopover from '@/components/base/CspPopover/CspPopover.vue'
import CspSeparator from '@/components/base/CspSeparator/CspSeparator.vue'
import CspTag from '@/components/base/CspTag/CspTag.vue'
import { TAGS_ORGANISME } from '../data/mock'
import { ACTIVITE_ICONS, formatRelative } from '../shared/format'
import NoteForm from './NoteForm.vue'

const props = defineProps<{
  candidature: ProtoCandidature
}>()

const emit = defineEmits<{
  voirTout: []
  addTag: [label: string]
  removeTag: [label: string]
  saveNote: []
}>()

const noteDraft = defineModel<string>('noteDraft', { default: '' })
const notePrivee = defineModel<boolean>('notePrivee', { default: false })
const tagPickerOpen = defineModel<boolean>('tagPickerOpen', { default: false })

const dernieresActivites = computed(() => props.candidature.activites.slice(0, 3))

const tagSearch = ref('')
const tagOptions = computed(() => TAGS_ORGANISME.filter(tag =>
  tag.toLowerCase().includes(tagSearch.value.trim().toLowerCase()),
))
</script>

<template>
  <aside class="colonne-droite">
    <section class="colonne-droite__section">
      <header class="colonne-droite__header">
        <h3 class="colonne-droite__title">
          Dernières activités
        </h3>
        <CspButton
          label="Voir tout"
          variant="tertiary-no-outline"
          size="sm"
          @click="emit('voirTout')"
        />
      </header>
      <ol class="activites">
        <li
          v-for="activite in dernieresActivites"
          :key="activite.uuid"
          class="activites__item"
        >
          <span class="activites__icon">
            <CspIcon
              :name="ACTIVITE_ICONS[activite.type]"
              :size="14"
              aria-hidden="true"
            />
          </span>
          <div class="activites__content">
            <p class="activites__libelle">
              {{ activite.libelle }}<template v-if="activite.tags?.length">
                : {{ activite.tags.join(', ') }}
              </template>
            </p>
            <p class="activites__meta">
              <span v-if="activite.auteur">par {{ activite.auteur }}</span>
              <time>{{ formatRelative(activite.date) }}</time>
            </p>
          </div>
        </li>
      </ol>
    </section>

    <CspSeparator />

    <section class="colonne-droite__section">
      <h3 class="colonne-droite__title">
        Tags
      </h3>
      <div class="tags">
        <CspTag
          v-for="tag in candidature.tags"
          :key="tag"
          size="sm"
          variant="dismissible"
          :label="tag"
          :dismiss-label="`Retirer le tag ${tag}`"
          @dismiss="emit('removeTag', tag)"
        />
        <CspPopover
          v-model:open="tagPickerOpen"
          side="bottom"
          align="start"
        >
          <template #trigger>
            <CspTag
              size="sm"
              variant="clickable"
              icon="ri:add-line"
              label="Ajouter"
            />
          </template>
          <div class="tag-picker">
            <CspInput
              v-model="tagSearch"
              type="search"
              size="sm"
              placeholder="Rechercher un tag"
              aria-label="Rechercher un tag de l'organisme"
            />
            <ul class="tag-picker__list">
              <li
                v-for="tag in tagOptions"
                :key="tag"
              >
                <button
                  type="button"
                  class="tag-picker__option"
                  :disabled="candidature.tags.includes(tag)"
                  @click="emit('addTag', tag)"
                >
                  <span>{{ tag }}</span>
                  <span class="tag-picker__state">
                    {{ candidature.tags.includes(tag) ? 'Déjà ajouté' : 'Ajouter' }}
                  </span>
                </button>
              </li>
            </ul>
            <p class="tag-picker__hint">
              La liste des tags se gère dans les paramètres de l'organisme.
            </p>
          </div>
        </CspPopover>
      </div>
    </section>

    <CspSeparator />

    <section class="colonne-droite__section">
      <h3 class="colonne-droite__title">
        Ajouter une note
      </h3>
      <NoteForm
        v-model:message="noteDraft"
        v-model:privee="notePrivee"
        block
        @submit="emit('saveNote')"
      />
    </section>
  </aside>
</template>

<style scoped lang="scss">
.colonne-droite {
  display: flex;
  flex-direction: column;
  gap: var(--csp-space-5);
}

.colonne-droite__section {
  display: flex;
  flex-direction: column;
  gap: var(--csp-space-3);
}

.colonne-droite__header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: var(--csp-space-2);
  min-height: 1.75rem;
}

.colonne-droite__title {
  margin: 0;
  font-size: 0.875rem;
  font-weight: 700;
  line-height: 1.4;
  color: var(--text-title-grey);
}

.activites {
  display: flex;
  flex-direction: column;
  margin: 0;
  padding: 0;
  list-style: none;
}

.activites {
  gap: var(--csp-space-3);
}

.activites__item {
  display: flex;
  align-items: flex-start;
  gap: var(--csp-space-3);
}

.activites__icon {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
  width: 1.75rem;
  height: 1.75rem;
  color: var(--text-action-high-grey);
  background: var(--background-alt-grey);
  border-radius: 0.25rem;
}

.activites__content {
  display: flex;
  flex-direction: column;
  gap: 0.125rem;
  min-width: 0;
  padding-top: 0.25rem;
}

.activites__libelle {
  margin: 0;
  font-size: 0.875rem;
  line-height: 1.4;
  color: var(--text-default-grey);
}

.activites__meta {
  display: flex;
  flex-wrap: wrap;
  gap: var(--csp-space-2);
  margin: 0;
  font-size: 0.75rem;
  line-height: 1.4;
  color: var(--text-mention-grey);
}

.tags {
  display: flex;
  flex-wrap: wrap;
  gap: var(--csp-space-2);
}

.tag-picker {
  display: flex;
  flex-direction: column;
  gap: var(--csp-space-2);
  width: 18rem;
}

.tag-picker__list {
  display: flex;
  flex-direction: column;
  max-height: 14rem;
  margin: 0;
  padding: 0;
  overflow-y: auto;
  list-style: none;
}

.tag-picker__option {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: var(--csp-space-2);
  width: 100%;
  padding: var(--csp-space-2);
  font: inherit;
  font-size: 0.875rem;
  text-align: left;
  color: var(--text-default-grey);
  background: none;
  border: none;
  cursor: pointer;

  &:hover:not(:disabled) {
    background: var(--background-default-grey-hover);
  }

  &:disabled {
    color: var(--text-disabled-grey);
    cursor: default;
  }
}

.tag-picker__state {
  font-size: 0.75rem;
  color: var(--text-action-high-blue-france);

  .tag-picker__option:disabled & {
    color: var(--text-disabled-grey);
  }
}

.tag-picker__hint {
  margin: 0;
  font-size: 0.75rem;
  color: var(--text-mention-grey);
}
</style>
