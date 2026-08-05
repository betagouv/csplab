import type { Candidature } from '../types'
import type { RecrutementDetail } from '@/features/recrutements/types'
import { defineQuery, useQuery, useQueryCache } from '@pinia/colada'
import { computed, watch } from 'vue'
import { useRoute } from 'vue-router'
import { TEMP_ORGANISME_UUID } from '@/constants/organisme'
import { peekRecrutementIntitule, recrutementDetailQuery } from '@/features/recrutements/queries'
import { candidatureListeQuery, recrutementKanbanQuery } from '../queries'
import { useCandidaturesFilters } from './useCandidaturesFilters'

export interface MoveCandidatureParams {
  sourceColumnId: string
  targetColumnId: string
  cardId: string
}

export interface MoveCandidaturesBatchParams {
  candidaturesByEtape: Map<string, string[]>
  targetColumnId: string
}

export const useCandidatures = defineQuery(() => {
  const route = useRoute()
  const recrutementUuid = computed<string | null>(() => {
    const param = route.params.recrutementUuid
    return typeof param === 'string' && param !== '' ? param : null
  })

  const isKanbanRoute = computed(() => route.name === 'recrutement-candidatures-kanban')
  const isListeRoute = computed(() => route.name === 'recrutement-candidatures')

  const queryCache = useQueryCache()

  const detail = useQuery(() => ({
    ...recrutementDetailQuery({
      organismeUuid: TEMP_ORGANISME_UUID,
      recrutementUuid: recrutementUuid.value ?? '',
    }),
    enabled: recrutementUuid.value !== null,
  }))

  const kanban = useQuery(() => ({
    ...recrutementKanbanQuery({
      organismeUuid: TEMP_ORGANISME_UUID,
      recrutementUuid: recrutementUuid.value ?? '',
    }),
    enabled: recrutementUuid.value !== null && isKanbanRoute.value,
  }))

  const liste = useQuery(() => ({
    ...candidatureListeQuery({
      organismeUuid: TEMP_ORGANISME_UUID,
      recrutementUuid: recrutementUuid.value ?? '',
    }),
    enabled: recrutementUuid.value !== null && isListeRoute.value,
  }))

  const recrutementDetail = computed<RecrutementDetail | null>(
    () => detail.data.value ?? null,
  )
  const candidatureListe = liste.data

  const intitule = computed<string | null>(() =>
    recrutementDetail.value?.intitule
    ?? (recrutementUuid.value
      ? peekRecrutementIntitule(queryCache, TEMP_ORGANISME_UUID, recrutementUuid.value)
      : null),
  )

  const recrutementEtapes = computed(() => detail.data.value?.etapes ?? [])
  const candidatureKanban = computed(() => kanban.data.value?.etapes ?? [])

  const pendingDetail = computed(() => detail.isPending.value)
  const pendingKanban = computed(() => kanban.isPending.value)
  const pendingListe = computed(() => liste.isPending.value)

  const error = computed<unknown>(() =>
    detail.error.value ?? kanban.error.value ?? liste.error.value,
  )

  const totalCount = computed(() =>
    candidatureKanban.value.reduce((sum, etape) => sum + etape.candidatures.length, 0),
  )

  function moveCandidature(params: MoveCandidatureParams): void {
    const { sourceColumnId, targetColumnId, cardId } = params

    if (sourceColumnId === targetColumnId)
      return

    const kanbanData = kanban.data.value
    if (!kanbanData)
      return

    const sourceEtape = kanbanData.etapes.find(e => e.etape_uuid === sourceColumnId)
    const targetEtape = kanbanData.etapes.find(e => e.etape_uuid === targetColumnId)

    if (!sourceEtape || !targetEtape)
      return

    const candidatureIndex = sourceEtape.candidatures.findIndex(c => c.uuid === cardId)
    if (candidatureIndex === -1)
      return

    const candidature = sourceEtape.candidatures[candidatureIndex] as Candidature

    const newEtapes = kanbanData.etapes.map((etape) => {
      if (etape.etape_uuid === sourceColumnId) {
        return {
          ...etape,
          candidatures: etape.candidatures.filter(c => c.uuid !== cardId),
        }
      }
      if (etape.etape_uuid === targetColumnId) {
        return {
          ...etape,
          candidatures: [...etape.candidatures, candidature],
        }
      }
      return etape
    })

    const { key } = recrutementKanbanQuery({
      organismeUuid: TEMP_ORGANISME_UUID,
      recrutementUuid: recrutementUuid.value!,
    })
    queryCache.setQueryData(key, { ...kanbanData, etapes: newEtapes })
  }

  function moveCandidaturesBatch(params: MoveCandidaturesBatchParams): void {
    const { candidaturesByEtape, targetColumnId } = params

    const kanbanData = kanban.data.value
    if (!kanbanData)
      return

    const targetEtape = kanbanData.etapes.find(e => e.etape_uuid === targetColumnId)
    if (!targetEtape)
      return

    const candidaturesToMove: Candidature[] = []

    for (const [sourceEtapeUuid, candidatureUuids] of candidaturesByEtape) {
      if (sourceEtapeUuid === targetColumnId)
        continue

      const sourceEtape = kanbanData.etapes.find(e => e.etape_uuid === sourceEtapeUuid)
      if (!sourceEtape)
        continue

      for (const uuid of candidatureUuids) {
        const candidature = sourceEtape.candidatures.find(c => c.uuid === uuid)
        if (candidature) {
          candidaturesToMove.push(candidature as Candidature)
        }
      }
    }

    if (candidaturesToMove.length === 0)
      return

    const movedUuids = new Set(candidaturesToMove.map(c => c.uuid))

    const newEtapes = kanbanData.etapes.map((etape) => {
      if (etape.etape_uuid === targetColumnId) {
        return {
          ...etape,
          candidatures: [...etape.candidatures, ...candidaturesToMove],
        }
      }

      if (candidaturesByEtape.has(etape.etape_uuid)) {
        return {
          ...etape,
          candidatures: etape.candidatures.filter(c => !movedUuids.has(c.uuid)),
        }
      }

      return etape
    })

    const { key } = recrutementKanbanQuery({
      organismeUuid: TEMP_ORGANISME_UUID,
      recrutementUuid: recrutementUuid.value!,
    })
    queryCache.setQueryData(key, { ...kanbanData, etapes: newEtapes })
  }

  const filters = useCandidaturesFilters({
    recrutementEtapes,
    candidatureKanban,
    candidatureListe,
  })

  watch(recrutementUuid, () => {
    filters.reset()
  })

  return {
    recrutementUuid,
    recrutementDetail,
    intitule,
    candidatureListe,
    candidatureKanban,
    recrutementEtapes,
    totalCount,
    pendingDetail,
    pendingKanban,
    pendingListe,
    error,
    moveCandidature,
    moveCandidaturesBatch,
    filters,
  }
})
