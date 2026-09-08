<script setup lang="ts">
import type { ProtoCandidature } from '../data/mock'
import { ref } from 'vue'
import CspButton from '@/components/base/CspButton/CspButton.vue'
import CspDialog from '@/components/base/CspDialog/CspDialog.vue'
import CspEmptyState from '@/components/base/CspEmptyState/CspEmptyState.vue'
import CvFictif from './CvFictif.vue'

defineProps<{
  candidature: ProtoCandidature
}>()

const pleinePage = ref(false)
</script>

<template>
  <section class="onglet-cv">
    <header class="onglet-cv__header">
      <h3 class="onglet-cv__title">
        Curriculum vitae
      </h3>
      <CspButton
        v-if="candidature.cv === 'lisible'"
        label="Afficher pleine page"
        variant="tertiary-no-outline"
        size="sm"
        icon="ri:fullscreen-line"
        is-icon-left
        @click="pleinePage = true"
      />
    </header>
    <div class="onglet-cv__body">
      <CvFictif
        v-if="candidature.cv === 'lisible'"
        :candidat="candidature.candidat"
      />
      <CspEmptyState
        v-else-if="candidature.cv === 'absent'"
        icon="ri:file-list-line"
        title="La candidature ne contient pas de CV"
        description="Les autres pièces du dossier sont consultables dans l'onglet Documents."
      />
      <CspEmptyState
        v-else
        icon="ri:file-list-line"
        title="Le CV ne peut pas être affiché ici."
        description="Vous pouvez le télécharger pour le consulter."
      >
        <template #action>
          <CspButton
            label="Télécharger le CV"
            variant="secondary"
            icon="ri:download-line"
            is-icon-left
          />
        </template>
      </CspEmptyState>
    </div>
  </section>

  <CspDialog
    v-model:open="pleinePage"
    size="lg"
    title="Curriculum vitae"
    close-label="Fermer"
  >
    <CvFictif :candidat="candidature.candidat" />
  </CspDialog>
</template>

<style scoped lang="scss">
.onglet-cv {
  display: flex;
  flex-direction: column;
  overflow: hidden;
  border: 1px solid var(--border-default-grey);
  border-radius: 0.25rem;
  background: var(--background-default-grey);
}

.onglet-cv__header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: var(--csp-space-3);
  min-height: 2.75rem;
  padding: var(--csp-space-1) var(--csp-space-2) var(--csp-space-1) var(--csp-space-4);
  background: var(--background-alt-grey);
  border-bottom: 1px solid var(--border-default-grey);
}

.onglet-cv__title {
  margin: 0;
  font-size: 0.875rem;
  font-weight: 700;
  color: var(--text-title-grey);
}

.onglet-cv__body {
  min-height: 20rem;
}
</style>
