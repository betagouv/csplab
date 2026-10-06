<script setup lang="ts">
import type { CspBreadcrumbItem } from '@/components/base/CspBreadcrumb/CspBreadcrumb.vue'
import CspPageContainer from '@/components/layout/CspPageContainer/CspPageContainer.vue'
import CspPageHeader from '@/components/layout/CspPageHeader/CspPageHeader.vue'
import { HOME_ROUTE_NAME, ORGANISMES_ROUTE_NAME } from '@/router/names'
import OrganismesSection from '../components/OrganismesSection.vue'

const breadcrumb: CspBreadcrumbItem[] = [
  { label: 'Accueil', to: { name: HOME_ROUTE_NAME } },
  { label: 'Gestion des organismes', to: { name: ORGANISMES_ROUTE_NAME } },
]
</script>

<template>
  <CspPageHeader
    :breadcrumb="breadcrumb"
    title="Gestion des organismes"
    subtitle="Les organismes permettent d'organiser les recrutements. Chaque organisme dispose de ses propres utilisateurs, offres et paramètres."
  />
  <CspPageContainer width="large">
    <OrganismesSection />
  </CspPageContainer>
</template>
