<script setup lang="ts">
import type { Note, NoteRouteNames } from '../types'
import type { CandidatureParams } from '@/api/params'
import { computed, ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import CspAsyncSection from '@/components/base/CspAsyncSection/CspAsyncSection.vue'
import CspBadge from '@/components/base/CspBadge/CspBadge.vue'
import CspButton from '@/components/base/CspButton/CspButton.vue'
import CspCard from '@/components/base/CspCard/CspCard.vue'
import CspDialog from '@/components/base/CspDialog/CspDialog.vue'
import CspDropdownMenu from '@/components/base/CspDropdownMenu/CspDropdownMenu.vue'
import CspEmptyState from '@/components/base/CspEmptyState/CspEmptyState.vue'
import CspSkeleton from '@/components/base/CspSkeleton/CspSkeleton.vue'
import { useMinimumPending } from '@/composables/async/useMinimumPending'
import { useToast } from '@/composables/ui/useToast'
import { formatDateTime } from '@/utils/date'
import { pluralize } from '@/utils/format'
import { useCandidatureNotes, useDeleteCandidatureNote, useUpdateCandidatureNoteVisibilite } from '../composables/useCandidatureNotes'
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
const editedNote = computed(() =>
  route.name === props.routes.edit
    ? notes.value.find(({ uuid }) => uuid === route.params.noteUuid)
    : undefined,
)

const router = useRouter()

function startNote(): void {
  const { organismeUuid, recrutementUuid, candidatureUuid } = props.candidature
  void router.push({
    name: props.routes.create,
    params: { organismeUuid, recrutementUuid, candidatureUuid },
  })
}

function editNote(noteUuid: string): void {
  const { organismeUuid, recrutementUuid, candidatureUuid } = props.candidature
  void router.push({
    name: props.routes.edit,
    params: { organismeUuid, recrutementUuid, candidatureUuid, noteUuid },
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

function noteActions(note: Note) {
  return [
    {
      items: [
        {
          label: 'Modifier la note',
          icon: 'ri:pencil-line',
          onSelect: () => editNote(note.uuid),
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
      ],
    },
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
  <CandidatureNewNoteForm
    v-if="isCreatingNote"
    :candidature="candidature"
    :routes="routes"
  />
  <CandidatureEditNoteForm
    v-else-if="editedNote"
    :key="editedNote.uuid"
    :candidature="candidature"
    :routes="routes"
    :note="editedNote"
  />
  <section
    v-else
    class="candidature-notes"
  >
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
        v-if="notes.length === 0"
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
            @click="startNote"
          />
        </header>
        <ul class="candidature-notes__list">
          <CspCard
            v-for="note in notes"
            :key="note.uuid"
            as="li"
            variant="alt"
            class="candidature-notes__item"
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
            <CandidatureNoteMessage :message="note.message" />
          </CspCard>
        </ul>
      </template>
    </CspAsyncSection>

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
    background: var(--background-contrast-grey);
  }
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
