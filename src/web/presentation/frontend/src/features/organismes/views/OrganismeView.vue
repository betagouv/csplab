<script setup lang="ts">
import type { CspBreadcrumbItem } from '@/components/base/CspBreadcrumb/CspBreadcrumb.vue'
import type { CspMetaItem } from '@/components/base/CspMeta/types'
import { useQuery } from '@pinia/colada'
import { computed } from 'vue'
import { useRoute } from 'vue-router'
import CspMetaList from '@/components/base/CspMeta/CspMetaList.vue'
import CspPageContainer from '@/components/layout/CspPageContainer/CspPageContainer.vue'
import CspPageHeader from '@/components/layout/CspPageHeader/CspPageHeader.vue'
import { tabItems } from '@/composables/navigation/tabs'
import { useRouteTab } from '@/composables/navigation/useRouteTab'
import EtapesRecrutementList from '@/features/etapes-recrutement/components/EtapesRecrutementList.vue'
import { ETAPES_TEXTS_ORGANISME } from '@/features/etapes-recrutement/constants/etape-recrutement'
import { useCurrentOrganisme } from '@/stores/currentOrganisme'
import { useCurrentUser } from '@/stores/currentUser'
import OrganismeAgentsSection from '../components/OrganismeAgentsSection.vue'
import { ORGANISME_TAB_LABELS } from '../constants/organisme'
import { organismesListQuery } from '../queries'
import { MON_ORGANISME_TAB_ROUTE_NAMES, ORGANISME_TAB_ROUTE_NAMES } from '../routes'

const route = useRoute()
const { user } = useCurrentUser()
const { organisme: currentOrganisme, organismeUuid: currentOrganismeUuid } = useCurrentOrganisme()

const organismeUuid = computed(() =>
  (route.params.organismeUuid as string | undefined) ?? currentOrganismeUuid.value ?? '',
)

const isCurrentOrganisme = computed(() =>
  currentOrganismeUuid.value !== null && currentOrganismeUuid.value === organismeUuid.value,
)

const organismesData = useQuery(() => ({
  ...organismesListQuery,
  enabled: user.value !== null && !isCurrentOrganisme.value,
}))

const organismeNom = computed(() => {
  if (isCurrentOrganisme.value)
    return currentOrganisme.value?.nom ?? null
  return organismesData.data.value
    ?.find(o => o.organisme_uuid === organismeUuid.value)
    ?.nom ?? null
})

const breadcrumb = computed<CspBreadcrumbItem[]>(() => [
  { label: 'Accueil', to: { name: 'home' } },
  ...(isCurrentOrganisme.value
    ? []
    : [{ label: 'Gestion des organismes', to: { name: 'organismes' } }]),
  { label: organismeNom.value ?? 'Organisme' },
])

const tabs = tabItems(ORGANISME_TAB_LABELS)

const activeTab = useRouteTab(
  () => (route.params.organismeUuid ? ORGANISME_TAB_ROUTE_NAMES : MON_ORGANISME_TAB_ROUTE_NAMES),
  'membres',
)

const metaItems = computed<CspMetaItem[]>(() =>
  organismeNom.value
    ? [{ icon: 'ri:government-line', label: organismeNom.value, srLabel: 'Organisme' }]
    : [],
)
</script>

<template>
  <CspPageHeader
    title="Paramètres de l'organisme"
    :breadcrumb="breadcrumb"
    :back-link="isCurrentOrganisme
      ? undefined
      : { to: { name: 'organismes' }, label: 'Retour à la gestion des organismes' }"
  >
    <template #subtitle>
      <CspMetaList :items="metaItems" />
    </template>
  </CspPageHeader>
  <CspPageContainer
    v-model:active-tab="activeTab"
    :tabs="tabs"
  >
    <template #tab-membres>
      <OrganismeAgentsSection
        v-if="organismeUuid"
        :key="organismeUuid"
        :organisme-uuid="organismeUuid"
      />
    </template>
    <template #tab-etapes>
      <EtapesRecrutementList
        v-if="organismeUuid"
        :params="{ type: 'organisme', organismeUuid }"
        :texts="ETAPES_TEXTS_ORGANISME"
      />
    </template>
  </CspPageContainer>
</template>
