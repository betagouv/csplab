<script setup lang="ts">
import type { CspBreadcrumbItem } from '@/components/base/CspBreadcrumb/CspBreadcrumb.vue'
import CspPageContainer from '@/components/layout/CspPageContainer/CspPageContainer.vue'
import CspPageHeader from '@/components/layout/CspPageHeader/CspPageHeader.vue'
import { useDocumentTitle } from '@/composables/ui/useDocumentTitle'
import { HOME_ROUTE_NAME, ORGANISMES_ROUTE_NAME } from '@/router/names'
import OrganismesSection from '../components/OrganismesSection.vue'

const TITLE = 'Gestion des organismes'

const breadcrumb: CspBreadcrumbItem[] = [
  { label: 'Accueil', to: { name: HOME_ROUTE_NAME } },
  { label: TITLE, to: { name: ORGANISMES_ROUTE_NAME } },
]

useDocumentTitle(TITLE)
</script>

<template>
  <CspPageHeader
    :breadcrumb="breadcrumb"
    :title="TITLE"
    subtitle="Les organismes permettent d'organiser les recrutements. Chaque organisme dispose de ses propres utilisateurs, offres et paramètres."
  />
  <CspPageContainer width="large">
    <OrganismesSection />
  </CspPageContainer>
</template>
