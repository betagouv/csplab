<script setup lang="ts">
import type { CspBreadcrumbItem } from '@/components/base/CspBreadcrumb/CspBreadcrumb.vue'
import { computed } from 'vue'
import CspPageContainer from '@/components/layout/CspPageContainer/CspPageContainer.vue'
import CspPageHeader from '@/components/layout/CspPageHeader/CspPageHeader.vue'
import { useDocumentTitle } from '@/composables/ui/useDocumentTitle'
import { useRecrutementDetail } from '@/features/recrutements/composables/useRecrutementDetail'
import { HOME_BREADCRUMB_ITEM, recrutementsBreadcrumbItem } from '@/router/breadcrumb'
import { CANDIDATURES_VIEW_ROUTE_NAMES } from '@/router/names'
import EtapesRecrutementList from '../components/EtapesRecrutementList.vue'
import { ETAPES_TEXTS_OFFRE } from '../constants/etape-recrutement'

const props = defineProps<{
  organismeUuid: string
  recrutementUuid: string
}>()

const { recrutementDetail, intitule } = useRecrutementDetail(() => props)

const candidaturesRoute = computed(() => ({
  name: CANDIDATURES_VIEW_ROUTE_NAMES.kanban,
  params: { organismeUuid: props.organismeUuid, recrutementUuid: props.recrutementUuid },
}))

const ETAPES_LABEL = 'Étapes de recrutement'

useDocumentTitle(ETAPES_LABEL, intitule)

const breadcrumb = computed<CspBreadcrumbItem[]>(() => [
  HOME_BREADCRUMB_ITEM,
  recrutementsBreadcrumbItem(props.organismeUuid, recrutementDetail.value?.archive),
  ...(intitule.value ? [{ label: intitule.value, to: candidaturesRoute.value }] : []),
  { label: ETAPES_LABEL },
])
</script>

<template>
  <CspPageHeader
    :breadcrumb="breadcrumb"
    title="Personnaliser les étapes de recrutement de l'offre"
    :back-link="{ to: candidaturesRoute, label: 'Retour à l’offre' }"
  />
  <CspPageContainer width="reading">
    <EtapesRecrutementList
      :params="{ type: 'offre', organismeUuid, recrutementUuid }"
      :texts="ETAPES_TEXTS_OFFRE"
    />
  </CspPageContainer>
</template>
