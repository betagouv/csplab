<script setup lang="ts">
import type { CspBreadcrumbItem } from '@/components/base/CspBreadcrumb/CspBreadcrumb.vue'
import type { CspMetaItem } from '@/components/base/CspMeta/types'
import { computed, ref } from 'vue'
import CspMetaList from '@/components/base/CspMeta/CspMetaList.vue'
import CspPageContainer from '@/components/layout/CspPageContainer/CspPageContainer.vue'
import CspPageHeader from '@/components/layout/CspPageHeader/CspPageHeader.vue'
import EtapesRecrutementList from '@/features/etapes-recrutement/components/EtapesRecrutementList.vue'
import { ETAPES_TEXTS_ORGANISME } from '@/features/etapes-recrutement/constants/etape-recrutement'
import { useCurrentOrganisme } from '@/stores/currentOrganisme'

const BREADCRUMB: CspBreadcrumbItem[] = [
  { label: 'Accueil', to: { name: 'home' } },
  { label: 'Paramètres' },
]

const tabs = [
  { value: 'etapes', label: 'Gestion des étapes de recrutement' },
]

const activeTab = ref('etapes')

const { organisme } = useCurrentOrganisme()

const metaItem = computed<CspMetaItem | null>(() => {
  if (!organisme.value) {
    return null
  }
  return {
    icon: 'ri:government-line',
    label: organisme.value.nom,
    srLabel: 'Organisme',
  }
})
</script>

<template>
  <CspPageHeader
    title="Paramètres de l'organisme"
    :breadcrumb="BREADCRUMB"
  >
    <template #subtitle>
      <CspMetaList
        v-if="metaItem"
        :items="[metaItem]"
      />
    </template>
  </CspPageHeader>
  <CspPageContainer
    v-model:active-tab="activeTab"
    width="reading"
    :tabs="tabs"
  >
    <template #tab-etapes>
      <EtapesRecrutementList
        v-if="organisme"
        :params="{ type: 'organisme', organismeUuid: organisme.organisme_uuid }"
        :texts="ETAPES_TEXTS_ORGANISME"
      />
    </template>
  </CspPageContainer>
</template>
