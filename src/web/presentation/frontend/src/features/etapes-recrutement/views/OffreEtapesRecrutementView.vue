<script setup lang="ts">
import type { CspBreadcrumbItem } from '@/components/base/CspBreadcrumb/CspBreadcrumb.vue'
import { useQuery, useQueryCache } from '@pinia/colada'
import { computed } from 'vue'
import { useRoute } from 'vue-router'
import CspPageContainer from '@/components/layout/CspPageContainer/CspPageContainer.vue'
import CspPageHeader from '@/components/layout/CspPageHeader/CspPageHeader.vue'
import { peekRecrutementIntitule, recrutementDetailQuery } from '@/features/recrutements/queries'
import { recrutementsListLocation } from '@/features/recrutements/routes'
import EtapesRecrutementList from '../components/EtapesRecrutementList.vue'
import { ETAPES_TEXTS_OFFRE } from '../constants/etape-recrutement'

const route = useRoute()
const recrutementUuid = route.params.recrutementUuid as string
const organismeUuid = route.params.organismeUuid as string

const queryCache = useQueryCache()

const { data: recrutementDetail } = useQuery(() => ({
  ...recrutementDetailQuery({
    organismeUuid,
    recrutementUuid,
  }),
}))

const intitule = computed<string | null>(() => {
  if (recrutementDetail.value?.intitule) {
    return recrutementDetail.value.intitule
  }
  return peekRecrutementIntitule(queryCache, organismeUuid, recrutementUuid)
})

const recrutementsListLink = computed(() =>
  recrutementsListLocation(organismeUuid, recrutementDetail.value?.archive),
)

const candidaturesRoute = computed(() => ({
  name: 'recrutement-candidatures-kanban',
  params: { organismeUuid, recrutementUuid },
}))

const breadcrumb = computed<CspBreadcrumbItem[]>(() => [
  { label: 'Accueil', to: { name: 'home' } },
  { label: 'Recrutements', to: recrutementsListLink.value },
  ...(intitule.value ? [{ label: intitule.value, to: candidaturesRoute.value }] : []),
  { label: 'Étapes de recrutement' },
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
