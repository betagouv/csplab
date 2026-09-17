<script setup lang="ts">
import type { CandidatureParams, DocumentListe } from '../types'
import { computed, useId } from 'vue'
import CspAsyncSection from '@/components/base/CspAsyncSection/CspAsyncSection.vue'
import CspButton from '@/components/base/CspButton/CspButton.vue'
import CspEmptyState from '@/components/base/CspEmptyState/CspEmptyState.vue'
import CspSkeleton from '@/components/base/CspSkeleton/CspSkeleton.vue'
import { useMinimumPending } from '@/composables/async/useMinimumPending'
import { useCandidatureDocuments } from '../composables/useCandidatureDocuments'

const props = defineProps<{
  candidature: CandidatureParams
  candidatNom: string
}>()

const { documents, pending, error, pdfUrl } = useCandidatureDocuments(() => props.candidature)

const cv = computed<DocumentListe | null>(() => documents.value.find(document => document.type === 'cv') ?? null)
const cvUrl = computed(() => cv.value ? pdfUrl(cv.value) : null)

const showSkeleton = useMinimumPending(pending)
const title = computed(() => `CV de ${props.candidatNom}`)
const titleId = useId()
</script>

<template>
  <section
    class="candidature-cv"
    :aria-labelledby="titleId"
  >
    <header class="candidature-cv__header">
      <h3
        :id="titleId"
        class="candidature-cv__title"
      >
        Curriculum vitae
      </h3>
      <div
        v-if="cv && cvUrl && !showSkeleton"
        class="candidature-cv__actions"
      >
        <CspButton
          as="a"
          :href="cvUrl"
          target="_blank"
          variant="tertiary-no-outline"
          size="sm"
          label="Afficher pleine page"
          icon="ri:fullscreen-line"
          is-icon-left
        />
        <CspButton
          as="a"
          :href="cvUrl"
          :download="cv.nom_original"
          variant="tertiary-no-outline"
          size="sm"
          label="Télécharger"
          icon="ri:download-line"
          is-icon-left
        />
      </div>
    </header>

    <CspAsyncSection
      :pending="showSkeleton"
      :error="error"
      loading-label="Chargement du CV"
      error-title="Le CV n'a pas pu être chargé."
      fill
    >
      <template #skeleton>
        <CspSkeleton height="100%" />
      </template>

      <CspEmptyState
        v-if="!cv"
        icon="ri:file-list-line"
        title="La candidature ne contient pas de CV"
        description="Les autres pièces du dossier sont consultables dans l'onglet Documents."
      />
      <CspEmptyState
        v-else-if="!cvUrl"
        icon="ri:file-list-line"
        title="Le CV ne peut pas être affiché ici."
      />
      <iframe
        v-else
        class="candidature-cv__document"
        :src="cvUrl"
        :title="title"
      />
    </CspAsyncSection>
  </section>
</template>

<style scoped lang="scss">
.candidature-cv {
  display: flex;
  flex: 1;
  flex-direction: column;
  min-height: 24rem;
  overflow: hidden;
  border: 1px solid var(--border-default-grey);
  background: var(--background-default-grey);
}

.candidature-cv__header {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  justify-content: space-between;
  gap: var(--csp-space-2);
  min-height: 2.75rem;
  padding: var(--csp-space-1) var(--csp-space-2) var(--csp-space-1) var(--csp-space-4);
  background: var(--background-alt-grey);
  border-bottom: 1px solid var(--border-default-grey);
}

.candidature-cv__title {
  margin: 0;
  font-size: 0.875rem;
  font-weight: 700;
  color: var(--text-title-grey);
}

.candidature-cv__actions {
  display: flex;
  flex-wrap: wrap;
  gap: var(--csp-space-1);
}

.candidature-cv__document {
  flex: 1;
  width: 100%;
  min-height: 0;
  border: 0;
}
</style>
