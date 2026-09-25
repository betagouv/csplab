<script setup lang="ts">
import type { CandidatureParams } from '../types'
import { computed } from 'vue'
import CspAsyncSection from '@/components/base/CspAsyncSection/CspAsyncSection.vue'
import CspEmptyState from '@/components/base/CspEmptyState/CspEmptyState.vue'
import CspSkeleton from '@/components/base/CspSkeleton/CspSkeleton.vue'
import { useMinimumPending } from '@/composables/async/useMinimumPending'
import { formatElapsedDays } from '@/utils/date'
import { pluralize } from '@/utils/format'
import { useCandidatureNotes } from '../composables/useCandidatureNotes'

const props = defineProps<{
  candidature: CandidatureParams
}>()

const { notes, total, pending, error } = useCandidatureNotes(() => props.candidature)

const showSkeleton = useMinimumPending(pending)

const title = computed(() => `${total.value} ${pluralize(total.value, 'note')}`)
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
        <CspSkeleton
          width="8rem"
          height="1.25rem"
          class="candidature-notes__skeleton"
        />
        <CspSkeleton height="4.5rem" />
        <CspSkeleton height="4.5rem" />
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
          <li
            v-for="note in notes"
            :key="note.entity_id"
            class="candidature-notes__item"
          >
            <p class="candidature-notes__meta">
              <span class="candidature-notes__auteur">{{ note.publie_par_prenom }} {{ note.publie_par_nom }}</span>
              <time :datetime="note.publie_le">{{ formatElapsedDays(note.publie_le) }}</time>
            </p>
            <p class="candidature-notes__message">
              {{ note.message }}
            </p>
          </li>
        </ul>
      </template>
    </CspAsyncSection>
  </section>
</template>

<style scoped lang="scss">
.candidature-notes__skeleton {
  margin-bottom: var(--csp-space-4);
}

.candidature-notes__title {
  margin: 0 0 var(--csp-space-4);
  font-size: 0.875rem;
  font-weight: 500;
  color: var(--text-mention-grey);
}

.candidature-notes__list {
  display: flex;
  flex-direction: column;
  margin: 0;
  padding: 0;
  list-style: none;
  border: 1px solid var(--border-default-grey);
}

.candidature-notes__item {
  padding: var(--csp-space-3) var(--csp-space-4);

  & + & {
    border-top: 1px solid var(--border-default-grey);
  }
}

.candidature-notes__meta {
  display: flex;
  flex-wrap: wrap;
  gap: var(--csp-space-2);
  margin: 0 0 var(--csp-space-1);
  font-size: 0.8125rem;
  color: var(--text-mention-grey);
}

.candidature-notes__auteur {
  font-weight: 500;
  color: var(--text-title-grey);
}

.candidature-notes__message {
  margin: 0;
  white-space: pre-line;
}
</style>
