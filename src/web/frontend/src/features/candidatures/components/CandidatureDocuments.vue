<script setup lang="ts">
import type { CandidatureParams } from '../types'
import { computed } from 'vue'
import CspAsyncSection from '@/components/base/CspAsyncSection/CspAsyncSection.vue'
import CspButton from '@/components/base/CspButton/CspButton.vue'
import CspEmptyState from '@/components/base/CspEmptyState/CspEmptyState.vue'
import CspIcon from '@/components/base/CspIcon/CspIcon.vue'
import CspSkeleton from '@/components/base/CspSkeleton/CspSkeleton.vue'
import { useMinimumPending } from '@/composables/async/useMinimumPending'
import { formatElapsedDays } from '@/utils/date'
import { pluralize } from '@/utils/format'
import { useCandidatureDocuments } from '../composables/useCandidatureDocuments'
import { TYPE_DOCUMENT_LABELS } from '../constants/candidature'
import { formatFileSize } from '../utils/file'

const props = defineProps<{
  candidature: CandidatureParams
}>()

const SKELETON_ROWS = 2

const { documents, total, pending, error, pdfUrl } = useCandidatureDocuments(() => props.candidature)

const showSkeleton = useMinimumPending(pending)

const title = computed(() => `${total.value} ${pluralize(total.value, 'document')}`)
</script>

<template>
  <section class="candidature-documents">
    <CspAsyncSection
      :pending="showSkeleton"
      :error="error"
      loading-label="Chargement des documents"
      error-title="Les documents n'ont pas pu être chargés."
    >
      <template #skeleton>
        <h3
          class="candidature-documents__title"
          aria-hidden="true"
        >
          <CspSkeleton
            width="8rem"
            variant="text"
          />
        </h3>
        <ul
          class="candidature-documents__list"
          aria-hidden="true"
        >
          <li
            v-for="row in SKELETON_ROWS"
            :key="row"
            class="candidature-documents__item"
          >
            <CspSkeleton
              width="1.25rem"
              height="1.25rem"
            />
            <div class="candidature-documents__content">
              <p class="candidature-documents__name">
                <CspSkeleton
                  width="60%"
                  variant="text"
                />
              </p>
              <p class="candidature-documents__meta">
                <CspSkeleton
                  width="80%"
                  variant="text"
                />
              </p>
            </div>
          </li>
        </ul>
      </template>

      <CspEmptyState
        v-if="documents.length === 0"
        icon="ri:file-list-line"
        title="La candidature ne contient aucun document"
      />
      <h3
        v-else
        class="candidature-documents__title"
      >
        {{ title }}
      </h3>
      <ul
        v-if="documents.length > 0"
        class="candidature-documents__list"
      >
        <li
          v-for="document in documents"
          :key="document.uuid"
          class="candidature-documents__item"
        >
          <CspIcon
            name="ri:file-list-line"
            :size="20"
            aria-hidden="true"
          />
          <div class="candidature-documents__content">
            <p class="candidature-documents__name">
              {{ document.nom_original }}
            </p>
            <p class="candidature-documents__meta">
              {{ TYPE_DOCUMENT_LABELS[document.type] }} · {{ formatFileSize(document.taille) }} · déposé {{ formatElapsedDays(document.depose_le) }}
            </p>
          </div>
          <template v-if="pdfUrl(document)">
            <CspButton
              as="a"
              :href="pdfUrl(document)"
              target="_blank"
              label="Voir"
              variant="tertiary"
              size="sm"
              icon="ri:eye-line"
              is-icon-left
            />
            <CspButton
              as="a"
              :href="pdfUrl(document)"
              :download="document.nom_original"
              label="Télécharger"
              variant="tertiary"
              size="sm"
              icon="ri:download-line"
              is-icon-left
            />
          </template>
        </li>
      </ul>
    </CspAsyncSection>
  </section>
</template>

<style scoped lang="scss">
.candidature-documents__title {
  margin: 0 0 var(--csp-space-4);
  font-size: 0.875rem;
  font-weight: 500;
  color: var(--text-mention-grey);
}

.candidature-documents__list {
  display: flex;
  flex-direction: column;
  margin: 0;
  padding: 0;
  list-style: none;
  border: 1px solid var(--border-default-grey);
}

.candidature-documents__item {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  gap: var(--csp-space-3);
  padding: var(--csp-space-3) var(--csp-space-4);

  & + & {
    border-top: 1px solid var(--border-default-grey);
  }
}

.candidature-documents__content {
  flex: 1;
  min-width: 12rem;
}

.candidature-documents__name {
  margin: 0;
  font-size: 0.9375rem;
  font-weight: 500;
  color: var(--text-title-grey);
}

.candidature-documents__meta {
  margin: 0;
  font-size: 0.8125rem;
  color: var(--text-mention-grey);
}
</style>
