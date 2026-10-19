<script setup lang="ts">
import type { Note, NoteRouteNames } from '../types'
import type { CandidatureParams } from '@/api/params'
import type { CspLabelItem } from '@/components/base/CspLabel/types'
import { computed, ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import CspAsyncSection from '@/components/base/CspAsyncSection/CspAsyncSection.vue'
import CspButton from '@/components/base/CspButton/CspButton.vue'
import CspCard from '@/components/base/CspCard/CspCard.vue'
import CspEmptyState from '@/components/base/CspEmptyState/CspEmptyState.vue'
import CspLabelList from '@/components/base/CspLabel/CspLabelList.vue'
import CspSkeleton from '@/components/base/CspSkeleton/CspSkeleton.vue'
import { useMinimumPending } from '@/composables/async/useMinimumPending'
import { useCurrentUser } from '@/stores/currentUser'
import { formatDateTime } from '@/utils/date'
import { pluralize } from '@/utils/format'
import { useCandidatureNotes } from '../composables/useCandidatureNotes'
import { etiquettesOf } from '../etiquettes'
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

const { user } = useCurrentUser()
const retirees = ref(new Set<string>())

const etiquettesByNote = computed(() => new Map(notes.value.map(note => [
  note.uuid,
  etiquettesOf(note).filter(({ label }) => !retirees.value.has(`${note.uuid}/${label}`)),
])))

function isAuthor(note: Note): boolean {
  return note.publie_par_prenom === user.value?.prenom && note.publie_par_nom === user.value?.nom
}

function retirer(note: Note, etiquette: CspLabelItem): void {
  retirees.value.add(`${note.uuid}/${etiquette.label}`)
}

const route = useRoute()
const isCreatingNote = computed(() => route.name === props.routes.create)

const router = useRouter()

function startNote(): void {
  const { organismeUuid, recrutementUuid, candidatureUuid } = props.candidature
  void router.push({
    name: props.routes.create,
    params: { organismeUuid, recrutementUuid, candidatureUuid },
  })
}
</script>

<template>
  <CandidatureNewNoteForm
    v-if="isCreatingNote"
    :candidature="candidature"
    :routes="routes"
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
            </template>
            <CspLabelList
              v-if="etiquettesByNote.get(note.uuid)?.length"
              class="candidature-notes__etiquettes"
              :labels="etiquettesByNote.get(note.uuid)!"
              :removable="isAuthor(note)"
              @remove="etiquette => retirer(note, etiquette)"
            />
            <CandidatureNoteMessage :message="note.message" />
          </CspCard>
        </ul>
      </template>
    </CspAsyncSection>
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

.candidature-notes__auteur {
  font-size: var(--csp-font-size-base);
  font-weight: var(--csp-font-weight-bold);
  color: var(--text-title-grey);
}

.candidature-notes__horodatage {
  display: inline-flex;
  gap: var(--csp-space-2);
}

.candidature-notes__etiquettes {
  margin-bottom: var(--csp-space-3);
}

.candidature-notes__horodatage,
.candidature-notes__separator {
  font-size: var(--csp-font-size-sm);
  color: var(--text-default-grey);
}
</style>
