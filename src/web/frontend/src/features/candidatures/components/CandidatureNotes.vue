<script setup lang="ts">
import type { CandidatureParams, NoteRouteNames } from '../types'
import { computed } from 'vue'
import { useRoute } from 'vue-router'
import CspAsyncSection from '@/components/base/CspAsyncSection/CspAsyncSection.vue'
import CspCard from '@/components/base/CspCard/CspCard.vue'
import CspEmptyState from '@/components/base/CspEmptyState/CspEmptyState.vue'
import CspSkeleton from '@/components/base/CspSkeleton/CspSkeleton.vue'
import { useMinimumPending } from '@/composables/async/useMinimumPending'
import { formatDate, formatTime } from '@/utils/date'
import { pluralize } from '@/utils/format'
import { useCandidatureNotes } from '../composables/useCandidatureNotes'
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
        title="La candidature ne contient aucune note"
      />
      <template v-else>
        <h3 class="candidature-notes__title">
          {{ title }}
        </h3>
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
                {{ formatDate(note.publie_le) }}
                <span
                  class="candidature-notes__separator"
                  aria-hidden="true"
                >•</span>
                {{ formatTime(note.publie_le) }}
              </time>
            </template>
            <CandidatureNoteMessage :message="note.message" />
          </CspCard>
        </ul>
      </template>
    </CspAsyncSection>
  </section>
</template>

<style scoped lang="scss">
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

.candidature-notes__horodatage,
.candidature-notes__separator {
  font-size: var(--csp-font-size-sm);
  color: var(--text-default-grey);
}
</style>
