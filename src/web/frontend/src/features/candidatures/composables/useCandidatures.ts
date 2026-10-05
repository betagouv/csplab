import type { CandidaturesQueryParams } from '../queries'
import type { Candidature } from '../types'
import type { RecrutementDetail } from '@/features/recrutements/types'
import { defineQuery, useQuery, useQueryCache } from '@pinia/colada'
import { computed, watch } from 'vue'
import { useRoute } from 'vue-router'
import { peekRecrutementIntitule, recrutementDetailQuery } from '@/features/recrutements/queries'
import { candidatureListeQuery, recrutementKanbanQuery } from '../queries'
import { useCandidaturesFilters } from './useCandidaturesFilters'

export const useCandidatures = defineQuery(() => {
  const route = useRoute()
  const recrutementUuid = computed<string | null>(() => {
    const param = route.params.recrutementUuid
    return typeof param === 'string' && param !== '' ? param : null
  })

  const organismeUuid = computed<string | null>(() => {
    const param = route.params.organismeUuid
    return typeof param === 'string' && param !== '' ? param : null
  })

  const recrutementParams = computed<CandidaturesQueryParams>(() => ({
    organismeUuid: organismeUuid.value ?? '',
    recrutementUuid: recrutementUuid.value ?? '',
  }))

  const isKanbanRoute = computed(() => route.matched.some(record => record.name === 'recrutement-candidatures-kanban'))
  const isListeRoute = computed(() => route.name === 'recrutement-candidatures')

  const queryCache = useQueryCache()

  const detail = useQuery(() => ({
    ...recrutementDetailQuery(recrutementParams.value),
    enabled: (
      recrutementUuid.value !== null
      && organismeUuid.value !== null
    ),
  }))

  const kanban = useQuery(() => ({
    ...recrutementKanbanQuery(recrutementParams.value),
    enabled: (
      recrutementUuid.value !== null
      && isKanbanRoute.value
      && organismeUuid.value !== null
    ),
  }))

  const liste = useQuery(() => ({
    ...candidatureListeQuery(recrutementParams.value),
    enabled: (
      recrutementUuid.value !== null
      && isListeRoute.value
      && organismeUuid.value !== null
    ),
  }))

  const recrutementDetail = computed<RecrutementDetail | null>(
    () => detail.data.value ?? null,
  )
  const candidatureListe = liste.data

  const intitule = computed<string | null>(() => {
    if (recrutementDetail.value?.intitule) {
      return recrutementDetail.value.intitule
    }
    if (!organismeUuid.value || !recrutementUuid.value) {
      return null
    }
    return peekRecrutementIntitule(queryCache, organismeUuid.value, recrutementUuid.value)
  })

  const recrutementEtapes = computed(() => detail.data.value?.etapes ?? [])
  const candidatureKanban = computed(() => kanban.data.value?.etapes ?? [])

  const pendingDetail = computed(() => detail.isPending.value)
  const pendingKanban = computed(() => kanban.isPending.value)
  const pendingListe = computed(() => liste.isPending.value)

  const error = computed<unknown>(() =>
    detail.error.value ?? kanban.error.value ?? liste.error.value,
  )

  function findCandidature(uuid: string): Candidature | null {
    for (const etape of candidatureKanban.value) {
      const found = etape.candidatures.find(c => c.uuid === uuid)
      if (found) {
        return found
      }
    }
    return null
  }

  const totalCount = computed(() =>
    candidatureKanban.value.reduce((sum, etape) => sum + etape.candidatures.length, 0),
  )

  const filters = useCandidaturesFilters({
    recrutementEtapes,
    candidatureKanban,
    candidatureListe,
  })

  watch(recrutementUuid, () => {
    filters.reset()
  })

  return {
    organismeUuid,
    recrutementUuid,
    recrutementParams,
    recrutementDetail,
    intitule,
    findCandidature,
    candidatureListe,
    candidatureKanban,
    recrutementEtapes,
    totalCount,
    pendingDetail,
    pendingKanban,
    pendingListe,
    error,
    filters,
  }
})
