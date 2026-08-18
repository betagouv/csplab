<script setup lang="ts">
import type { CspBreadcrumbItem } from '@/components/base/CspBreadcrumb/CspBreadcrumb.vue'
import type { CspMetaItem } from '@/components/base/CspMeta/types'
import { useQuery } from '@pinia/colada'
import { computed, ref } from 'vue'
import { useRoute } from 'vue-router'
import CspMetaList from '@/components/base/CspMeta/CspMetaList.vue'
import CspPageContainer from '@/components/layout/CspPageContainer/CspPageContainer.vue'
import CspPageHeader from '@/components/layout/CspPageHeader/CspPageHeader.vue'
import EtapesRecrutementList from '@/features/etapes-recrutement/components/EtapesRecrutementList.vue'
import { ETAPES_TEXTS_ORGANISME } from '@/features/etapes-recrutement/constants/etape-recrutement'
import { organismesQuery } from '@/features/organismes/queries'

const route = useRoute()
const organismeUuid = computed(() => String(route.params.organismeUuid))

const organismesData = useQuery(organismesQuery)
const organisme = computed(() =>
  organismesData.data.value?.find(o => o.uuid === organismeUuid.value) ?? null,
)

const breadcrumb = computed<CspBreadcrumbItem[]>(() => [
  { label: 'Accueil', to: { name: 'home' } },
  { label: 'Paramètres', to: { name: 'parametres' } },
  { label: organisme.value?.nom ?? 'Organisme' },
])

const tabs = [
  { value: 'etapes', label: 'Gestion des étapes de recrutement' },
]

const activeTab = ref('etapes')

const metaItems = computed<CspMetaItem[]>(() =>
  organisme.value
    ? [{ icon: 'ri:government-line', label: organisme.value.nom, srLabel: 'Organisme' }]
    : [],
)
</script>

<template>
  <CspPageHeader
    title="Paramètres de l'organisme"
    :breadcrumb="breadcrumb"
    :back-link="{ to: { name: 'parametres' }, label: 'Retour aux paramètres' }"
  >
    <template #subtitle>
      <CspMetaList :items="metaItems" />
    </template>
  </CspPageHeader>
  <CspPageContainer
    v-model:active-tab="activeTab"
    width="reading"
    :tabs="tabs"
  >
    <template #tab-etapes>
      <EtapesRecrutementList
        :params="{ type: 'organisme', organismeUuid }"
        :texts="ETAPES_TEXTS_ORGANISME"
      />
    </template>
  </CspPageContainer>
</template>
