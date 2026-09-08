<script setup lang="ts">
import type { ProtoCandidature, ProtoNote } from '../data/mock'
import { ref } from 'vue'
import CspBadge from '@/components/base/CspBadge/CspBadge.vue'
import CspButton from '@/components/base/CspButton/CspButton.vue'
import CspDropdownMenu from '@/components/base/CspDropdownMenu/CspDropdownMenu.vue'
import { formatRelative } from '../shared/format'
import NoteForm from './NoteForm.vue'

defineProps<{
  candidature: ProtoCandidature
}>()

const emit = defineEmits<{
  submitDraft: []
  update: [uuid: string, patch: Partial<Pick<ProtoNote, 'message' | 'privee'>>]
  delete: [uuid: string]
}>()

const noteDraft = defineModel<string>('noteDraft', { default: '' })
const notePrivee = defineModel<boolean>('notePrivee', { default: false })
const showForm = ref(false)

function submit(): void {
  emit('submitDraft')
  showForm.value = false
}

const editingUuid = ref<string | null>(null)
const editMessage = ref('')
const editPrivee = ref(false)

function startEdit(note: ProtoNote): void {
  editingUuid.value = note.uuid
  editMessage.value = note.message
  editPrivee.value = note.privee
}

function saveEdit(): void {
  if (editingUuid.value)
    emit('update', editingUuid.value, { message: editMessage.value.trim(), privee: editPrivee.value })
  editingUuid.value = null
}

function sectionsFor(note: ProtoNote) {
  return [{
    items: [
      { label: 'Modifier la note', icon: 'ri:edit-line', onSelect: () => startEdit(note) },
      {
        label: note.privee ? 'Rendre la note publique' : 'Rendre la note privée',
        icon: note.privee ? 'ri:lock-unlock-line' : 'ri:lock-line',
        onSelect: () => emit('update', note.uuid, { privee: !note.privee }),
      },
      { label: 'Supprimer la note', icon: 'ri:delete-bin-line', destructive: true, onSelect: () => emit('delete', note.uuid) },
    ],
  }]
}
</script>

<template>
  <section class="notes">
    <header class="notes__header">
      <h3 class="notes__title">
        {{ candidature.notes.length }} note{{ candidature.notes.length > 1 ? 's' : '' }}
      </h3>
      <CspButton
        v-if="!showForm"
        label="Ajouter une note"
        size="sm"
        icon="ri:add-line"
        is-icon-left
        @click="showForm = true"
      />
    </header>

    <div
      v-if="showForm"
      class="notes__new"
    >
      <p class="notes__new-title">
        Nouvelle note
      </p>
      <NoteForm
        v-model:message="noteDraft"
        v-model:privee="notePrivee"
        submit-label="Enregistrer"
        cancelable
        @submit="submit"
        @cancel="showForm = false"
      />
    </div>

    <ul class="notes__list">
      <li
        v-for="note in candidature.notes"
        :key="note.uuid"
        class="notes__item"
        :class="{ 'notes__item--editing': editingUuid === note.uuid }"
      >
        <div class="notes__meta">
          <span class="notes__auteur">{{ note.auteur }}</span>
          <span class="notes__role">{{ note.role }}</span>
          <time class="notes__date">{{ formatRelative(note.date) }}</time>
          <CspBadge
            v-if="note.privee"
            size="sm"
            variant="soft"
            label="Privée"
            icon="ri:lock-line"
          />
          <CspDropdownMenu
            v-if="note.mienne && editingUuid !== note.uuid"
            :sections="sectionsFor(note)"
            side="bottom"
            align="end"
            class="notes__menu"
          >
            <template #trigger>
              <CspButton
                variant="tertiary-no-outline"
                size="sm"
                icon="ri:more-fill"
                aria-label="Actions sur la note"
              />
            </template>
          </CspDropdownMenu>
        </div>
        <NoteForm
          v-if="editingUuid === note.uuid"
          v-model:message="editMessage"
          v-model:privee="editPrivee"
          submit-label="Enregistrer les modifications"
          cancelable
          @submit="saveEdit"
          @cancel="editingUuid = null"
        />
        <p
          v-else
          class="notes__message"
        >
          {{ note.message }}
        </p>
      </li>
    </ul>
  </section>
</template>

<style scoped lang="scss">
.notes {
  display: flex;
  flex-direction: column;
  gap: var(--csp-space-4);
}

.notes__header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: var(--csp-space-3);
}

.notes__title {
  margin: 0;
  font-size: 0.875rem;
  font-weight: 500;
  color: var(--text-mention-grey);
}

.notes__new {
  display: flex;
  flex-direction: column;
  gap: var(--csp-space-3);
  padding: var(--csp-space-4);
  background: var(--background-alt-blue-france);
  border: 1px solid var(--border-action-high-blue-france);
}

.notes__new-title {
  margin: 0;
  font-size: 0.9375rem;
  font-weight: 700;
  color: var(--text-title-grey);
}

.notes__list {
  display: flex;
  flex-direction: column;
  gap: var(--csp-space-3);
  margin: 0;
  padding: 0;
  list-style: none;
}

.notes__item {
  display: flex;
  flex-direction: column;
  gap: var(--csp-space-2);
  padding: var(--csp-space-4);
  background: var(--background-alt-grey);
}

.notes__item--editing {
  background: var(--background-alt-blue-france);
}

.notes__meta {
  display: flex;
  align-items: center;
  flex-wrap: wrap;
  gap: var(--csp-space-2);
  font-size: 0.8125rem;
  color: var(--text-mention-grey);
}

.notes__auteur {
  font-weight: 700;
  color: var(--text-title-grey);
}

.notes__menu {
  margin-left: auto;
}

.notes__message {
  margin: 0;
  font-size: 0.9375rem;
  line-height: 1.5;
  white-space: pre-line;
  color: var(--text-default-grey);
}
</style>
