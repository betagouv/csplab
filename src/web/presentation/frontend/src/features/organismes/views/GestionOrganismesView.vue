<script setup lang="ts">
import type { CspBreadcrumbItem } from '@/components/base/CspBreadcrumb/CspBreadcrumb.vue'
import CspPageContainer from '@/components/layout/CspPageContainer/CspPageContainer.vue'
import CspPageHeader from '@/components/layout/CspPageHeader/CspPageHeader.vue'
import OrganismesSection from '../components/OrganismesSection.vue'

const breadcrumb: CspBreadcrumbItem[] = [
  { label: 'Accueil', to: { name: 'home' } },
  { label: 'Gestion des organismes', to: { name: 'organismes' } },
]
</script>

<template>
  <CspPageHeader
    :breadcrumb="breadcrumb"
    title="Gestion des organismes"
  />
  <CspPageContainer width="full">
    <OrganismesSection />
  </CspPageContainer>
</template>
