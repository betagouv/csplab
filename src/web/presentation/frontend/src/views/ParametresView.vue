<script setup lang="ts">
import type { CspBreadcrumbItem } from '@/components/base/CspBreadcrumb/CspBreadcrumb.vue'
import type { CspMetaItem } from '@/components/base/CspMeta/types'
import { ref } from 'vue'
import CspMetaList from '@/components/base/CspMeta/CspMetaList.vue'
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

const activeTab = ref('etapes')

const metaItem: CspMetaItem = {
  icon: 'ri:government-line',
  label: 'Ministère de la Transition Écologique',
  srLabel: 'Organisme',
}
</script>

<template>
  <CspPageHeader
    title="Paramètres de l'organisme"
    :breadcrumb="BREADCRUMB"
  >
    <template #subtitle>
      <CspMetaList :items="[metaItem]" />
    </template>
  </CspPageHeader>
  <CspPageContainer
    v-model:active-tab="activeTab"
    :tabs="tabs"
  >
    <template #tab-etapes>
      <EtapesRecrutementList />
    </template>
  </CspPageContainer>
</template>
