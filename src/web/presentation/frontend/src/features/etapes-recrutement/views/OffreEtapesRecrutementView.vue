<script setup lang="ts">
import type { CspBreadcrumbItem } from '@/components/base/CspBreadcrumb/CspBreadcrumb.vue'
import { useQuery, useQueryCache } from '@pinia/colada'
import { computed } from 'vue'
import { useRoute } from 'vue-router'
import CspPageContainer from '@/components/layout/CspPageContainer/CspPageContainer.vue'
import CspPageHeader from '@/components/layout/CspPageHeader/CspPageHeader.vue'
import { TEMP_ORGANISME_UUID } from '@/constants/organisme'
import { recrutementKanbanQuery } from '@/features/candidatures/queries'
import { peekRecrutementIntitule } from '@/features/recrutements/queries'

const route = useRoute()
const recrutementUuid = route.params.recrutementUuid as string

const queryCache = useQueryCache()

const { data: recrutementDetail } = useQuery(() => recrutementKanbanQuery({
  organismeUuid: TEMP_ORGANISME_UUID,
  recrutementUuid,
}))

const intitule = computed<string | null>(() =>
  recrutementDetail.value?.intitule
  ?? peekRecrutementIntitule(queryCache, TEMP_ORGANISME_UUID, recrutementUuid),
)

const candidaturesRoute = computed(() => ({
  name: 'recrutement-candidatures-kanban',
  params: { recrutementUuid },
}))

const breadcrumb = computed<CspBreadcrumbItem[]>(() => [
  { label: 'Accueil', to: { name: 'home' } },
  { label: 'Mes recrutements', to: { name: 'mes-recrutements' } },
  ...(intitule.value ? [{ label: intitule.value, to: candidaturesRoute.value }] : []),
  { label: 'Étapes de recrutement' },
])
</script>

<template>
  <CspPageHeader
    :breadcrumb="breadcrumb"
    title="Personnaliser les étapes de recrutement"
    :back-link="{ to: candidaturesRoute, label: 'Retour à l’offre' }"
  />
  <CspPageContainer
    fill
    width="full"
  />
</template>
