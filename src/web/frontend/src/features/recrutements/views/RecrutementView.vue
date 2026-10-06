<script setup lang="ts">
import type { RecrutementDetailTabKey } from '../constants/recrutement'
import type { CspBreadcrumbItem } from '@/components/base/CspBreadcrumb/CspBreadcrumb.vue'
import { computed } from 'vue'
import { useRouter } from 'vue-router'
import { isHttpStatus } from '@/api/errors'
import CspButton from '@/components/base/CspButton/CspButton.vue'
import CspDropdownMenu from '@/components/base/CspDropdownMenu/CspDropdownMenu.vue'
import CspMetaList from '@/components/base/CspMeta/CspMetaList.vue'
import CspPageContainer from '@/components/layout/CspPageContainer/CspPageContainer.vue'
import CspPageHeader from '@/components/layout/CspPageHeader/CspPageHeader.vue'
import { useMinimumPending } from '@/composables/async/useMinimumPending'
import { tabItems } from '@/composables/navigation/tabs'
import { useRouteTab } from '@/composables/navigation/useRouteTab'
import { useDocumentTitle } from '@/composables/ui/useDocumentTitle'
import { HOME_BREADCRUMB_ITEM, recrutementsBreadcrumbItem } from '@/router/breadcrumb'
import { RECRUTEMENT_DETAIL_TAB_ROUTE_NAMES, RECRUTEMENT_ETAPES_ROUTE_NAME, recrutementsListLocation } from '@/router/names'
import { useCurrentUser } from '@/stores/currentUser'
import { useRouteOrganisme } from '@/stores/routeOrganisme'
import ForbiddenView from '@/views/ForbiddenView.vue'
import { useRecrutementDetail } from '../composables/useRecrutementDetail'
import { RECRUTEMENT_DETAIL_TAB_ICONS, RECRUTEMENT_DETAIL_TAB_LABELS } from '../constants/recrutement'
import { formatRecrutementMeta } from '../format'

const props = defineProps<{
  organismeUuid: string
  recrutementUuid: string
}>()
const router = useRouter()
const { recrutementDetail, intitule, pending: pendingDetail, error } = useRecrutementDetail(() => props)

const showTitleSkeleton = useMinimumPending(
  computed(() => pendingDetail.value && !intitule.value),
)
const showSubtitleSkeleton = useMinimumPending(
  computed(() => pendingDetail.value && !recrutementDetail.value),
)

const recrutementsListLink = computed(() => recrutementsListLocation(props.organismeUuid, recrutementDetail.value?.archive))

const title = computed(() => intitule.value ?? 'Candidatures')

const breadcrumb = computed<CspBreadcrumbItem[]>(() => [
  HOME_BREADCRUMB_ITEM,
  recrutementsBreadcrumbItem(props.organismeUuid, recrutementDetail.value?.archive),
  ...(intitule.value ? [{ label: intitule.value }] : []),
])

const metaItems = computed(() =>
  recrutementDetail.value ? formatRecrutementMeta(recrutementDetail.value) : [],
)

const { user } = useCurrentUser()
const { canManageOrganisme } = useRouteOrganisme()

const TABS = tabItems(RECRUTEMENT_DETAIL_TAB_LABELS, RECRUTEMENT_DETAIL_TAB_ICONS)
const visibleTabs = computed(() =>
  canManageOrganisme.value ? TABS : TABS.filter(tab => tab.value !== 'equipe'),
)
const activeTab = useRouteTab<RecrutementDetailTabKey>(RECRUTEMENT_DETAIL_TAB_ROUTE_NAMES, 'candidatures')

useDocumentTitle(() => RECRUTEMENT_DETAIL_TAB_LABELS[activeTab.value], intitule)

const equipeForbidden = computed(() =>
  activeTab.value === 'equipe' && Boolean(user.value) && !canManageOrganisme.value,
)

const forbidden = computed(() => isHttpStatus(error.value, 403) || equipeForbidden.value)

const headerMenuSections = [{
  items: [{
    label: 'Personnaliser les étapes de recrutement',
    icon: 'ri:table-line',
    onSelect: () => router.push({
      name: RECRUTEMENT_ETAPES_ROUTE_NAME,
      params: { organismeUuid: props.organismeUuid, recrutementUuid: props.recrutementUuid },
    }),
  }],
}]
</script>

<template>
  <ForbiddenView v-if="forbidden" />
  <template v-else>
    <CspPageHeader
      :breadcrumb="breadcrumb"
      :title="title"
      :back-link="{ to: recrutementsListLink, label: 'Retour aux recrutements' }"
      :show-title-skeleton="showTitleSkeleton"
      :show-subtitle-skeleton="showSubtitleSkeleton"
    >
      <template #actions>
        <CspDropdownMenu
          :sections="headerMenuSections"
          side="bottom"
          align="end"
        >
          <template #trigger>
            <CspButton
              icon="ri:more-fill"
              variant="tertiary"
              size="sm"
              aria-label="Actions sur l’offre"
            />
          </template>
        </CspDropdownMenu>
      </template>
      <template #subtitle>
        <CspMetaList :items="metaItems" />
      </template>
    </CspPageHeader>
    <CspPageContainer
      v-model:active-tab="activeTab"
      fill
      width="full"
      :tabs="visibleTabs"
    >
      <template #tab>
        <router-view />
      </template>
    </CspPageContainer>
  </template>
</template>
