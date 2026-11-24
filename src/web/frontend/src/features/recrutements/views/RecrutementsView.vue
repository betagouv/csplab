<script setup lang="ts">
import type { RecrutementKey } from '../types'
import type { CspBreadcrumbItem } from '@/components/base/CspBreadcrumb/CspBreadcrumb.vue'
import { computed } from 'vue'
import { isHttpStatus } from '@/api/errors'
import CspErrorState from '@/components/base/CspErrorState/CspErrorState.vue'
import CspPageContainer from '@/components/layout/CspPageContainer/CspPageContainer.vue'
import CspPageHeader from '@/components/layout/CspPageHeader/CspPageHeader.vue'
import { tabItems } from '@/composables/navigation/tabs'
import { useRouteTab } from '@/composables/navigation/useRouteTab'
import { useDocumentTitle } from '@/composables/ui/useDocumentTitle'
import { homeBreadcrumbItem, RECRUTEMENTS_BREADCRUMB_LABEL } from '@/router/breadcrumb'
import { RECRUTEMENTS_TAB_ROUTE_NAMES } from '@/router/names'
import { useRouteOrganisme } from '@/stores/routeOrganisme'
import ForbiddenView from '@/views/ForbiddenView.vue'
import { useRecrutements } from '../composables/useRecrutements'
import { RECRUTEMENT_TAB_ICONS, RECRUTEMENT_TAB_LABELS } from '../constants/recrutement'

const props = defineProps<{
  organismeUuid: string
}>()

const breadcrumb = computed<CspBreadcrumbItem[]>(() => [
  homeBreadcrumbItem(props.organismeUuid),
  { label: RECRUTEMENTS_BREADCRUMB_LABEL },
])

const activeTab = useRouteTab<RecrutementKey>(RECRUTEMENTS_TAB_ROUTE_NAMES, 'actifs')

const { organisme: routeOrganisme } = useRouteOrganisme()
useDocumentTitle(() => RECRUTEMENT_TAB_LABELS[activeTab.value], () => routeOrganisme.value?.nom)

const TABS = tabItems(RECRUTEMENT_TAB_LABELS, RECRUTEMENT_TAB_ICONS)

const { error: recrutementsError } = useRecrutements(() => props.organismeUuid, activeTab)

const forbidden = computed(() => isHttpStatus(recrutementsError.value, 403))
</script>

<template>
  <ForbiddenView v-if="forbidden" />
  <template v-else>
    <CspPageHeader
      title="Recrutements"
      subtitle="Retrouvez ici l’ensemble des recrutements en cours et terminés."
      :breadcrumb="breadcrumb"
    />
    <CspPageContainer
      v-model:active-tab="activeTab"
      class="mes-recrutement-view"
      :tabs="TABS"
    >
      <template
        v-if="recrutementsError"
        #shared
      >
        <CspErrorState
          title="Une erreur est survenue lors du chargement des recrutements."
        />
      </template>
      <template
        v-if="!recrutementsError"
        #tab
      >
        <router-view v-slot="{ Component }">
          <KeepAlive
            :key="organismeUuid"
            include="RecrutementsActifsView,RecrutementsArchivesView"
          >
            <component :is="Component" />
          </KeepAlive>
        </router-view>
      </template>
    </CspPageContainer>
  </template>
</template>
