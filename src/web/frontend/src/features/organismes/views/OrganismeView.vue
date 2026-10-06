<script setup lang="ts">
import type { OrganismeTabKey } from '../constants/organisme'
import type { CspBreadcrumbItem } from '@/components/base/CspBreadcrumb/CspBreadcrumb.vue'
import type { CspMetaItem } from '@/components/base/CspMeta/types'
import { computed } from 'vue'
import CspMetaList from '@/components/base/CspMeta/CspMetaList.vue'
import CspPageContainer from '@/components/layout/CspPageContainer/CspPageContainer.vue'
import CspPageHeader from '@/components/layout/CspPageHeader/CspPageHeader.vue'
import { tabItems } from '@/composables/navigation/tabs'
import { useRouteTab } from '@/composables/navigation/useRouteTab'
import { useDocumentTitle } from '@/composables/ui/useDocumentTitle'
import EtapesRecrutementList from '@/features/etapes-recrutement/components/EtapesRecrutementList.vue'
import { ETAPES_TEXTS_ORGANISME } from '@/features/etapes-recrutement/constants/etape-recrutement'
import { HOME_ROUTE_NAME, ORGANISME_TAB_ROUTE_NAMES } from '@/router/names'
import ForbiddenView from '@/views/ForbiddenView.vue'
import NotFoundView from '@/views/NotFoundView.vue'
import OrganismeAgentsSection from '../components/OrganismeAgentsSection.vue'
import { useOrganismeDetail } from '../composables/useOrganismeDetail'
import { ORGANISME_TAB_ICONS, ORGANISME_TAB_LABELS } from '../constants/organisme'

const props = defineProps<{
  organismeUuid: string
}>()

const { organisme, notFound, forbidden } = useOrganismeDetail(() => props.organismeUuid)

const TITLE = 'Paramètres de l\'organisme'

const breadcrumb: CspBreadcrumbItem[] = [
  { label: 'Accueil', to: { name: HOME_ROUTE_NAME } },
  { label: TITLE },
]

const tabs = tabItems(ORGANISME_TAB_LABELS, ORGANISME_TAB_ICONS)

const activeTab = useRouteTab<OrganismeTabKey>(ORGANISME_TAB_ROUTE_NAMES, 'membres')

useDocumentTitle(() => ORGANISME_TAB_LABELS[activeTab.value], () => organisme.value?.nom)

const metaItems = computed<CspMetaItem[]>(() =>
  organisme.value
    ? [{ icon: 'ri:government-line', label: organisme.value.nom, srLabel: 'Organisme' }]
    : [],
)
</script>

<template>
  <NotFoundView v-if="notFound" />
  <ForbiddenView v-else-if="forbidden" />
  <template v-else>
    <CspPageHeader
      :title="TITLE"
      :breadcrumb="breadcrumb"
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
          :key="organismeUuid"
          :organisme-uuid="organismeUuid"
        />
      </template>
      <template #tab-etapes>
        <EtapesRecrutementList
          :params="{ type: 'organisme', organismeUuid }"
          :texts="ETAPES_TEXTS_ORGANISME"
        />
      </template>
    </CspPageContainer>
  </template>
</template>
