<script setup lang="ts">
import type { CspBreadcrumbItem } from '@/components/base/CspBreadcrumb/CspBreadcrumb.vue'
import { computed } from 'vue'
import { isHttpStatus } from '@/api/errors'
import CspPageContainer from '@/components/layout/CspPageContainer/CspPageContainer.vue'
import CspPageHeader from '@/components/layout/CspPageHeader/CspPageHeader.vue'
import { useDocumentTitle } from '@/composables/ui/useDocumentTitle'
import { useRecrutementDetail } from '@/features/recrutements/composables/useRecrutementDetail'
import { homeBreadcrumbItem, recrutementsBreadcrumbItem } from '@/router/breadcrumb'
import { CANDIDATURES_VIEW_ROUTE_NAMES } from '@/router/names'
import { can } from '@/utils/authorizedActions'
import ForbiddenView from '@/views/ForbiddenView.vue'
import EtapesRecrutementList from '../components/EtapesRecrutementList.vue'
import { ETAPES_TEXTS_OFFRE } from '../constants/etape-recrutement'

const props = defineProps<{
  organismeUuid: string
  recrutementUuid: string
}>()

const { recrutementDetail, intitule, error } = useRecrutementDetail(() => props)

const forbidden = computed(() =>
  isHttpStatus(error.value, 403)
  || (Boolean(recrutementDetail.value) && !can(recrutementDetail.value?.authorized_actions, 'update_recrutement_etapes')),
)

const candidaturesRoute = computed(() => ({
  name: CANDIDATURES_VIEW_ROUTE_NAMES.kanban,
  params: { organismeUuid: props.organismeUuid, recrutementUuid: props.recrutementUuid },
}))

const ETAPES_LABEL = 'Étapes de recrutement'

useDocumentTitle(ETAPES_LABEL, intitule)

const breadcrumb = computed<CspBreadcrumbItem[]>(() => [
  homeBreadcrumbItem(props.organismeUuid),
  recrutementsBreadcrumbItem(props.organismeUuid, recrutementDetail.value?.archive),
  ...(intitule.value ? [{ label: intitule.value, to: candidaturesRoute.value }] : []),
  { label: ETAPES_LABEL },
])
</script>

<template>
  <ForbiddenView v-if="forbidden" />
  <template v-else>
    <CspPageHeader
      :breadcrumb="breadcrumb"
      title="Personnaliser les étapes de ce recrutement"
      :back-link="{ to: candidaturesRoute, label: 'Retour au recrutement' }"
    />
    <CspPageContainer width="reading">
      <EtapesRecrutementList
        :params="{ type: 'offre', organismeUuid, recrutementUuid }"
        :texts="ETAPES_TEXTS_OFFRE"
      />
    </CspPageContainer>
  </template>
</template>
