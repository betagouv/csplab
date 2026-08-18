<script setup lang="ts">
import type { CspBreadcrumbItem } from '@/components/base/CspBreadcrumb/CspBreadcrumb.vue'
import CspPageContainer from '@/components/layout/CspPageContainer/CspPageContainer.vue'
import CspPageHeader from '@/components/layout/CspPageHeader/CspPageHeader.vue'
import OrganismesSection from '@/features/organismes/components/OrganismesSection.vue'

const BREADCRUMB: CspBreadcrumbItem[] = [
  { label: 'Accueil', to: { name: 'home' } },
  { label: 'Paramètres' },
]
</script>

<template>
  <CspPageHeader
    title="Paramètres"
    :breadcrumb="BREADCRUMB"
  />
  <CspPageContainer width="reading">
    <OrganismesSection />
  </CspPageContainer>
</template>
