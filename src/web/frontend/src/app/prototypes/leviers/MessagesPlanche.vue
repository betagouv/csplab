<script setup lang="ts">
import CspButton from '@/components/base/CspButton/CspButton.vue'
import CspCallout from '@/components/base/CspCallout/CspCallout.vue'
import CspEmptyState from '@/components/base/CspEmptyState/CspEmptyState.vue'
import CspToast from '@/components/base/CspToast/CspToast.vue'
import CspToastProvider from '@/components/base/CspToast/CspToastProvider.vue'
</script>

<template>
  <CspToastProvider>
    <div class="messages-planche">
      <div class="messages-planche__colonne">
        <CspEmptyState
          icon="ri:sticky-note-line"
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
          title="La candidature ne contient aucun document"
        />
      </div>
      <div class="messages-planche__colonne">
        <CspCallout
          variant="info"
          title="Modification des étapes de recrutement"
          description="Ce modèle d'étapes sera appliqué par défaut à tous les nouveaux recrutements."
        />
        <CspCallout
          variant="error"
          title="Le changement d'étape a échoué"
          description="Vos candidatures sont restées à leur étape actuelle."
        />
      </div>
    </div>
    <CspToast
      variant="success"
      title="Clara Fontaine est passée à l'étape Présélection"
      :default-open="true"
      :duration="86400000"
    />
    <CspToast
      variant="warning"
      title="Certaines candidatures n'ont pas changé d'étape"
      :default-open="true"
      :duration="86400000"
    />
  </CspToastProvider>
</template>

<style scoped lang="scss">
.messages-planche {
  display: grid;
  grid-template-columns: repeat(2, 22rem);
  gap: var(--csp-space-6);
  min-height: 35rem;
  padding: var(--csp-space-6);
  background-color: var(--csp-panel-canvas-background, var(--background-default-grey));
}

.messages-planche__colonne {
  display: flex;
  flex-direction: column;
  gap: var(--csp-space-4);
}
</style>
