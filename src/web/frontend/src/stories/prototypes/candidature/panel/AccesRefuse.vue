<script setup lang="ts">
import type { CspBreadcrumbItem } from '@/components/base/CspBreadcrumb/CspBreadcrumb.vue'
import CspButton from '@/components/base/CspButton/CspButton.vue'
import CspCallout from '@/components/base/CspCallout/CspCallout.vue'
import CspCard from '@/components/base/CspCard/CspCard.vue'
import CspPageContainer from '@/components/layout/CspPageContainer/CspPageContainer.vue'
import CspPageHeader from '@/components/layout/CspPageHeader/CspPageHeader.vue'

const breadcrumb: CspBreadcrumbItem[] = [
  { label: 'Accueil', to: '/' },
  { label: 'Recrutements', to: '/' },
  { label: 'Candidature' },
]
</script>

<template>
  <CspPageHeader
    :breadcrumb="breadcrumb"
    title="Candidature"
    :back-link="{ to: '/', label: 'Retour aux recrutements' }"
  />
  <CspPageContainer width="wide">
    <div class="acces-refuse">
      <CspCallout
        icon="ri:lock-line"
        title="Cette candidature n'est pas accessible."
        description="Elle n'existe pas ou ne vous est pas accessible. Contactez le responsable de votre organisme si besoin."
      />
      <CspCard
        title="Besoin d'aide ?"
        description="Si vous pensez qu'il s'agit d'une erreur, contactez le responsable de votre organisme ou le responsable du recrutement concerné."
      >
        <template #end>
          <div class="acces-refuse__actions">
            <CspButton
              label="Contacter le support"
              variant="secondary"
              icon="ri:chat-3-line"
              is-icon-left
            />
            <CspButton
              label="Consulter l'aide en ligne"
              variant="secondary"
              icon="ri:external-link-line"
              is-icon-left
            />
          </div>
        </template>
      </CspCard>
    </div>
  </CspPageContainer>
</template>

<style scoped lang="scss">
.acces-refuse {
  display: flex;
  flex-direction: column;
  gap: var(--csp-space-6);
}

.acces-refuse__actions {
  display: flex;
  flex-wrap: wrap;
  gap: var(--csp-space-3);
}
</style>
