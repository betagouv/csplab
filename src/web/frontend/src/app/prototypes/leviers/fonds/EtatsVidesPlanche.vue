<script setup lang="ts">
import CspButton from '@/components/base/CspButton/CspButton.vue'
import CspEmptyState from '@/components/base/CspEmptyState/CspEmptyState.vue'
</script>

<template>
  <div class="etats-vides-planche">
    <CspEmptyState
      icon="ri:sticky-note-line"
      pictogram="document/document-add"
      title="Aucune note sur cette candidature"
    >
      <template #action>
        <CspButton
          variant="secondary"
          icon="ri:add-line"
          is-icon-left
          label="Ajouter une note"
        />
      </template>
    </CspEmptyState>
    <CspEmptyState
      icon="ri:file-list-line"
      pictogram="document/archive"
      title="La candidature ne contient aucun document"
    />
    <CspEmptyState
      icon="ri:mail-close-line"
      pictogram="digital/mail-send"
      title="Aucune conversation pour le moment"
      description="Créer une conversation pour échanger avec Clara Fontaine"
    />
    <CspEmptyState
      icon="ri:briefcase-line"
      pictogram="document/contract"
      title="Vous n’avez pas de recrutement en cours"
      description="Les recrutements auxquels vous participez apparaissent ici. Pour accéder à un recrutement, contactez la personne responsable dans votre organisation."
    />
  </div>
</template>

<style scoped lang="scss">
.etats-vides-planche {
  display: grid;
  grid-template-columns: repeat(2, 22rem);
  gap: var(--csp-space-6);
  padding: var(--csp-space-6);
  background-color: var(--csp-panel-background);
}
</style>
