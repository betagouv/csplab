<script setup lang="ts">
import type { CspBreadcrumbItem } from '@/components/base/CspBreadcrumb/CspBreadcrumb.vue'
import CspBadge from '@/components/base/CspBadge/CspBadge.vue'
import CspTabs from '@/components/base/CspTabs/CspTabs.vue'
import CspPageContainer from '@/components/layout/CspPageContainer/CspPageContainer.vue'
import CspPageHeader from '@/components/layout/CspPageHeader/CspPageHeader.vue'
import EtapesRecrutementList from '@/features/etapes-recrutement/components/EtapesRecrutementList.vue'

const BREADCRUMB: CspBreadcrumbItem[] = [
  { label: 'Accueil', to: { name: 'home' } },
  { label: 'Paramètres' },
]

const tabs = [
  { value: 'etapes', label: 'Gestion des étapes de recrutement' },
]
</script>

<template>
  <CspPageContainer>
    <CspPageHeader
      title="Paramètres de l'organisme"
      :breadcrumb="BREADCRUMB"
      class="parametres-view__header"
    >
      <template #subtitle>
        <CspBadge
          icon="ri:building-line"
          label="Ministère de la Transition Écologique"
        />
      </template>
    </CspPageHeader>

    <CspTabs
      :tabs="tabs"
      default-value="etapes"
    >
      <template #etapes>
        <EtapesRecrutementList />
      </template>
    </CspTabs>
  </CspPageContainer>
</template>

<style scoped lang="scss">
.parametres-view__header {
  margin-bottom: var(--csp-space-4);
}
</style>
