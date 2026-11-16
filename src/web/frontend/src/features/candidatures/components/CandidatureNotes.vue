<script setup lang="ts">
import type { Note, NoteRouteNames } from '../types'
import type { CandidatureParams } from '@/api/params'
import { computed, ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { isHttpStatus } from '@/api/errors'
import CspAsyncSection from '@/components/base/CspAsyncSection/CspAsyncSection.vue'
import CspBadge from '@/components/base/CspBadge/CspBadge.vue'
import CspButton from '@/components/base/CspButton/CspButton.vue'
import CspCard from '@/components/base/CspCard/CspCard.vue'
import CspDialog from '@/components/base/CspDialog/CspDialog.vue'
import CspDrawer from '@/components/base/CspDrawer/CspDrawer.vue'
import CspDropdownMenu from '@/components/base/CspDropdownMenu/CspDropdownMenu.vue'
import CspEmptyState from '@/components/base/CspEmptyState/CspEmptyState.vue'
import CspSkeleton from '@/components/base/CspSkeleton/CspSkeleton.vue'
import { useMinimumPending } from '@/composables/async/useMinimumPending'
import { useToast } from '@/composables/ui/useToast'
import TagList from '@/features/tags/components/TagList.vue'
import TagPicker from '@/features/tags/components/TagPicker.vue'
import { can } from '@/utils/authorizedActions'
import { formatDateTime } from '@/utils/date'
import { pluralize } from '@/utils/format'
import { useCandidatureNotes, useCandidatureNoteTags, useDeleteCandidatureNote, useUpdateCandidatureNoteVisibilite } from '../composables/useCandidatureNotes'
import CandidatureEditNoteForm from './CandidatureEditNoteForm.vue'
import CandidatureNewNoteForm from './CandidatureNewNoteForm.vue'
import CandidatureNoteMessage from './CandidatureNoteMessage.vue'

const props = defineProps<{
  candidature: CandidatureParams
  routes: NoteRouteNames
}>()

const SKELETON_ROWS = 2

const { notes, total, pending, error } = useCandidatureNotes(() => props.candidature)

const showSkeleton = useMinimumPending(pending)

const title = computed(() => `${total.value} ${pluralize(total.value, 'note')}`)

const route = useRoute()
const isCreatingNote = computed(() => route.name === props.routes.create)

const editedNoteUuid = ref<string | null>(null)
const editedNote = computed(() => notes.value.find(({ uuid }) => uuid === editedNoteUuid.value))

const router = useRouter()

function startNote(): void {
  const { organismeUuid, recrutementUuid, candidatureUuid } = props.candidature
  void router.push({
    name: props.routes.create,
    params: { organismeUuid, recrutementUuid, candidatureUuid },
  })
}

const { addToast } = useToast()

const { updateVisibilite, updatingVisibilite } = useUpdateCandidatureNoteVisibilite(() => props.candidature)

async function toggleVisibilite(note: Note): Promise<void> {
  const estPrivee = !note.est_privee
  try {
    await updateVisibilite({ noteUuid: note.uuid, est_privee: estPrivee })
    addToast({ variant: 'success', title: estPrivee ? 'Note rendue privée' : 'Note rendue publique' })
  }
  catch {
    addToast({ variant: 'error', title: 'Le changement de visibilité de la note a échoué' })
  }
}

const { remove, removing } = useDeleteCandidatureNote(() => props.candidature)

const noteToDelete = ref<Note | null>(null)
const deletionDialogOpen = computed({
  get: () => noteToDelete.value !== null,
  set: (open) => {
    if (!open) {
      noteToDelete.value = null
    }
  },
})

async function confirmDeletion(): Promise<void> {
  if (!noteToDelete.value) {
    return
  }
  try {
    await remove(noteToDelete.value.uuid)
    addToast({ variant: 'success', title: 'Note supprimée' })
    noteToDelete.value = null
  }
  catch {
    addToast({ variant: 'error', title: 'La suppression de la note a échoué' })
  }
}

const { addTags, addingTags, removeTag } = useCandidatureNoteTags(() => props.candidature)

const taggedNoteUuid = ref<string | null>(null)
const taggedNote = computed(() => notes.value.find(({ uuid }) => uuid === taggedNoteUuid.value))
const tagPickerOpen = ref(false)

function openTagPicker(note: Note): void {
  taggedNoteUuid.value = note.uuid
  tagPickerOpen.value = true
}

async function confirmTags(tagUuids: string[]): Promise<void> {
  if (!taggedNote.value) {
    return
  }
  try {
    await addTags({ noteUuid: taggedNote.value.uuid, tagUuids })
    tagPickerOpen.value = false
  }
  catch (error) {
    if (isHttpStatus(error, 404)) {
      addToast({ variant: 'warning', title: 'L\'étiquette ou la note a été supprimée' })
      tagPickerOpen.value = false
      return
    }
    addToast({ variant: 'error', title: 'L\'ajout de l\'étiquette a échoué' })
  }
}

async function handleRemoveTag(note: Note, tagUuid: string): Promise<void> {
  try {
    await removeTag({ noteUuid: note.uuid, tagUuid })
  }
  catch (error) {
    if (!isHttpStatus(error, 404)) {
      addToast({ variant: 'error', title: 'Le retrait de l\'étiquette a échoué' })
    }
  }
}

function canChangeNote(note: Note): boolean {
  return can(note.authorized_actions, 'update_note')
}

function noteActions(note: Note) {
  return [
    ...(canChangeNote(note) ? updateActions(note) : []),
    ...(can(note.authorized_actions, 'delete_note') ? deleteActions(note) : []),
  ]
}

function updateActions(note: Note) {
  return [
    {
      items: [
        {
          label: 'Modifier la note',
          icon: 'ri:pencil-line',
          disabled: isCreatingNote.value || editedNote.value !== undefined,
          onSelect: () => {
            editedNoteUuid.value = note.uuid
          },
        },
      ],
    },
    {
      items: [
        {
          label: note.est_privee ? 'Rendre la note publique' : 'Rendre la note privée',
          icon: note.est_privee ? 'ri:eye-line' : 'ri:eye-off-line',
          disabled: updatingVisibilite.value,
          onSelect: () => toggleVisibilite(note),
        },
        {
          label: 'Ajouter une étiquette',
          icon: 'ri:price-tag-3-line',
          onSelect: () => openTagPicker(note),
        },
      ],
    },
  ]
}

function deleteActions(note: Note) {
  return [
    {
      items: [
        {
          label: 'Supprimer la note',
          icon: 'ri:delete-bin-line',
          destructive: true,
          onSelect: () => {
            noteToDelete.value = note
          },
        },
      ],
    },
  ]
}
</script>

<template>
  <section class="candidature-notes">
    <CspAsyncSection
      :pending="showSkeleton"
      :error="error"
      loading-label="Chargement des notes"
      error-title="Les notes n'ont pas pu être chargées."
    >
      <template #skeleton>
        <h3
          class="candidature-notes__title"
          aria-hidden="true"
        >
          <CspSkeleton
            width="8rem"
            variant="text"
          />
        </h3>
        <ul
          class="candidature-notes__list"
          aria-hidden="true"
        >
          <CspCard
            v-for="row in SKELETON_ROWS"
            :key="row"
            as="li"
            variant="alt"
            class="candidature-notes__item"
          >
            <template #start>
              <CspSkeleton
                width="14rem"
                variant="text"
              />
            </template>
            <CspSkeleton
              width="80%"
              variant="text"
            />
          </CspCard>
        </ul>
      </template>

      <CspEmptyState
        v-if="notes.length === 0 && !isCreatingNote"
        icon="ri:sticky-note-line"
        title="Aucune note sur cette candidature"
      >
        <template #action>
          <CspButton
            variant="secondary"
            icon="ri:add-line"
            is-icon-left
            label="Ajouter une note"
            @click="startNote"
          />
        </template>
      </CspEmptyState>
      <template v-else>
        <header class="candidature-notes__header">
          <h3 class="candidature-notes__title">
            {{ title }}
          </h3>
          <CspButton
            variant="secondary"
            size="sm"
            icon="ri:add-line"
            is-icon-left
            label="Ajouter une note"
            :disabled="editedNote !== undefined"
            @click="startNote"
          />
        </header>
        <ul class="candidature-notes__list">
          <CandidatureNewNoteForm
            v-if="isCreatingNote"
            :candidature="candidature"
            :routes="routes"
            class="candidature-notes__item candidature-notes__item--edition"
          />
          <CspCard
            v-for="note in notes"
            :key="note.uuid"
            as="li"
            variant="alt"
            class="candidature-notes__item"
            :class="{ 'candidature-notes__item--edition': note === editedNote }"
          >
            <template #start>
              <div class="candidature-notes__entete">
                <span class="candidature-notes__auteur">{{ note.publie_par_prenom }} {{ note.publie_par_nom }}</span>
                <span
                  class="candidature-notes__separator"
                  aria-hidden="true"
                >•</span>
                <time
                  :datetime="note.publie_le"
                  class="candidature-notes__horodatage"
                >
                  {{ formatDateTime(note.publie_le) }}
                </time>
                <CspBadge
                  v-if="note.est_privee"
                  label="Privée"
                  color="var(--text-label-purple-glycine)"
                  class="candidature-notes__badge"
                />
                <CspDropdownMenu
                  v-if="note !== editedNote && noteActions(note).length > 0"
                  :sections="noteActions(note)"
                  side="bottom"
                  align="end"
                >
                  <template #trigger>
                    <CspButton
                      icon="ri:more-fill"
                      variant="tertiary-no-outline"
                      size="sm"
                      class="candidature-notes__actions"
                      :aria-label="`Actions sur la note de ${note.publie_par_prenom} ${note.publie_par_nom}`"
                    />
                  </template>
                </CspDropdownMenu>
              </div>
            </template>
            <TagList
              v-if="note.tags.length > 0"
              :tags="note.tags"
              :dismiss-label="canChangeNote(note) ? tag => `Retirer l'étiquette ${tag.name}` : undefined"
              class="candidature-notes__tags"
              :aria-label="`Étiquettes de la note de ${note.publie_par_prenom} ${note.publie_par_nom}`"
              @dismiss="tag => handleRemoveTag(note, tag.uuid)"
            />
            <CandidatureEditNoteForm
              v-if="note === editedNote"
              :candidature="candidature"
              :note="note"
              @close="editedNoteUuid = null"
            />
            <CandidatureNoteMessage
              v-else
              :message="note.message"
            />
          </CspCard>
        </ul>
      </template>
    </CspAsyncSection>

    <CspDrawer
      v-model:open="tagPickerOpen"
      title="Ajouter une étiquette"
      size="md"
    >
      <TagPicker
        v-if="taggedNote"
        :organisme-uuid="candidature.organismeUuid"
        category="note"
        :excluded-tag-uuids="taggedNote.tags.map(({ uuid }) => uuid)"
        :saving="addingTags"
        @confirm="confirmTags"
        @cancel="tagPickerOpen = false"
      />
    </CspDrawer>

    <CspDialog
      v-model:open="deletionDialogOpen"
      title="Supprimer la note"
      size="sm"
    >
      Cette note sera supprimée définitivement.

      <template #footer>
        <CspButton
          label="Annuler"
          variant="secondary"
          @click="deletionDialogOpen = false"
        />
        <CspButton
          label="Supprimer la note"
          :disabled="removing"
          @click="confirmDeletion"
        />
      </template>
    </CspDialog>
  </section>
</template>

<style scoped lang="scss">
.candidature-notes__header {
  display: flex;
  gap: var(--csp-space-4);
  align-items: center;
  justify-content: space-between;
  margin-bottom: var(--csp-space-4);

  .candidature-notes__title {
    margin: 0;
  }
}

.candidature-notes__title {
  margin: 0 0 var(--csp-space-4);
  font-size: var(--csp-font-size-base);
  font-weight: var(--csp-font-weight-regular);
  color: var(--text-default-grey);
}

.candidature-notes__list {
  display: flex;
  flex-direction: column;
  gap: var(--csp-space-4);
  margin: 0;
  padding: 0;
  list-style: none;
}

.candidature-notes__item {
  --csp-card-border: transparent;

  :deep(.csp-skeleton) {
    background: var(--csp-neutral-background);
  }
}

.candidature-notes__item--edition {
  --csp-card-bg: var(--background-alt-blue-france);
}

.candidature-notes__entete {
  display: flex;
  flex: 1;
  gap: var(--csp-space-2);
  align-items: center;
}

.candidature-notes__entete .candidature-notes__badge {
  --badge-default-bg: var(--background-contrast-purple-glycine);

  align-self: center;
}

.candidature-notes__tags {
  margin-bottom: var(--csp-space-3);
}

.candidature-notes__actions {
  margin-left: auto;
}

.candidature-notes__auteur {
  font-size: var(--csp-font-size-base);
  font-weight: var(--csp-font-weight-bold);
  color: var(--text-title-grey);
}

.candidature-notes__horodatage {
  display: inline-flex;
  gap: var(--csp-space-2);
}

.candidature-notes__horodatage,
.candidature-notes__separator {
  font-size: var(--csp-font-size-sm);
  color: var(--text-default-grey);
}
</style>
