<script setup lang="ts">
import type { CspBreadcrumbItem } from '@/components/base/CspBreadcrumb/CspBreadcrumb.vue'
import type { CspMetaItem } from '@/components/base/CspMeta/types'
import { computed } from 'vue'
import { useRoute } from 'vue-router'
import CspMetaList from '@/components/base/CspMeta/CspMetaList.vue'
import CspPageContainer from '@/components/layout/CspPageContainer/CspPageContainer.vue'
import CspPageHeader from '@/components/layout/CspPageHeader/CspPageHeader.vue'
import { tabItems } from '@/composables/navigation/tabs'
import { useRouteTab } from '@/composables/navigation/useRouteTab'
import EtapesRecrutementList from '@/features/etapes-recrutement/components/EtapesRecrutementList.vue'
import { ETAPES_TEXTS_ORGANISME } from '@/features/etapes-recrutement/constants/etape-recrutement'
import NotFoundView from '@/views/NotFoundView.vue'
import OrganismeAgentsSection from '../components/OrganismeAgentsSection.vue'
import { useOrganismeDetail } from '../composables/useOrganismeDetail'
import { ORGANISME_TAB_LABELS } from '../constants/organisme'
import { ORGANISME_TAB_ROUTE_NAMES } from '../routes'

const route = useRoute()

const organismeUuid = computed(() => route.params.organismeUuid as string)

const { organisme, notFound } = useOrganismeDetail(organismeUuid)

const breadcrumb = computed<CspBreadcrumbItem[]>(() => [
  { label: 'Accueil', to: { name: 'home' } },
  { label: 'Gestion des organismes', to: { name: 'organismes' } },
  ...(organisme.value ? [{ label: organisme.value.nom }] : []),
])

const tabs = tabItems(ORGANISME_TAB_LABELS)

const activeTab = useRouteTab(ORGANISME_TAB_ROUTE_NAMES, 'membres')

const metaItems = computed<CspMetaItem[]>(() =>
  organisme.value
    ? [{ icon: 'ri:government-line', label: organisme.value.nom, srLabel: 'Organisme' }]
    : [],
)
</script>

<template>
  <NotFoundView v-if="notFound" />
  <template v-else>
    <CspPageHeader
      title="Paramètres de l'organisme"
      :breadcrumb="breadcrumb"
      :back-link="{ to: { name: 'organismes' }, label: 'Retour à la gestion des organismes' }"
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
</template>
