<script setup lang="ts">
import type { CspBreadcrumbItem } from '@/components/base/CspBreadcrumb/CspBreadcrumb.vue'
import { computed } from 'vue'
import CspEmptyState from '@/components/base/CspEmptyState/CspEmptyState.vue'
import CspPageContainer from '@/components/layout/CspPageContainer/CspPageContainer.vue'
import CspPageHeader from '@/components/layout/CspPageHeader/CspPageHeader.vue'
import { useEquipePrototypeContext } from '../shared/context'
import { formatAgentNom, formatListe } from '../shared/format'

const proto = useEquipePrototypeContext()

const BREADCRUMB: CspBreadcrumbItem[] = [
  { label: 'Accueil', to: '/' },
  { label: 'Recrutements' },
]

const description = computed(() => {
  const noms = proto.gestionnaires.value.map(formatAgentNom)
  const count = noms.length
  return `Pour rejoindre une équipe de recrutement, contactez ${formatListe(noms)}, ${count > 1 ? 'gestionnaires' : 'gestionnaire'} de votre organisme.`
})
</script>

<template>
  <CspPageHeader
    title="Recrutements"
    :breadcrumb="BREADCRUMB"
  />
  <CspPageContainer>
    <CspEmptyState
      title="Vous n'êtes rattaché à aucun recrutement."
      :description="description"
      icon="ri:team-line"
    />
  </CspPageContainer>
</template>
