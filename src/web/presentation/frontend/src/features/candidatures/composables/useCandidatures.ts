import type {
  Candidature,
  RecrutementDetailKanban,
} from '../types'
import { defineQuery, useQuery, useQueryCache } from '@pinia/colada'
import { computed, watch } from 'vue'
import { useRoute } from 'vue-router'
import { TEMP_ORGANISME_UUID } from '@/constants/organisme'
import { peekRecrutementIntitule } from '@/features/recrutements/queries'
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

  const queryCache = useQueryCache()

  const kanban = useQuery(() => ({
    ...recrutementKanbanQuery({
      organismeUuid: TEMP_ORGANISME_UUID,
      recrutementUuid: recrutementUuid.value ?? '',
    }),
    enabled: recrutementUuid.value !== null,
  }))

  const liste = useQuery(() => ({
    ...candidatureListeQuery({
      organismeUuid: TEMP_ORGANISME_UUID,
      recrutementUuid: recrutementUuid.value ?? '',
    }),
    enabled: recrutementUuid.value !== null,
  }))

  const recrutementDetail = computed<RecrutementDetailKanban | null>(
    () => kanban.data.value ?? null,
  )
  const candidatureListe = liste.data

  const intitule = computed<string | null>(() =>
    recrutementDetail.value?.intitule
    ?? (recrutementUuid.value
      ? peekRecrutementIntitule(queryCache, TEMP_ORGANISME_UUID, recrutementUuid.value)
      : null),
  )

  const etapes = computed(() => kanban.data.value?.etapes ?? [])

  const pending = computed(() => kanban.isPending.value || liste.isPending.value)
  const error = computed<unknown>(() => kanban.error.value ?? liste.error.value)

  const totalCount = computed(() =>
    etapes.value.reduce((sum, etape) => sum + etape.candidatures.length, 0),
  )

  function moveCandidature(params: MoveCandidatureParams): void {
    const { sourceColumnId, targetColumnId, cardId } = params

    if (sourceColumnId === targetColumnId)
      return

    const detail = kanban.data.value
    if (!detail)
      return

    const sourceEtape = detail.etapes.find(e => e.etape_uuid === sourceColumnId)
    const targetEtape = detail.etapes.find(e => e.etape_uuid === targetColumnId)

    if (!sourceEtape || !targetEtape)
      return

    const candidatureIndex = sourceEtape.candidatures.findIndex(c => c.uuid === cardId)
    if (candidatureIndex === -1)
      return

    const candidature = sourceEtape.candidatures[candidatureIndex] as Candidature

    const newEtapes = detail.etapes.map((etape) => {
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
    queryCache.setQueryData(key, { ...detail, etapes: newEtapes })
  }

  function moveCandidaturesBatch(params: MoveCandidaturesBatchParams): void {
    const { candidaturesByEtape, targetColumnId } = params

    const detail = kanban.data.value
    if (!detail)
      return

    const targetEtape = detail.etapes.find(e => e.etape_uuid === targetColumnId)
    if (!targetEtape)
      return

    const candidaturesToMove: Candidature[] = []

    for (const [sourceEtapeUuid, candidatureUuids] of candidaturesByEtape) {
      if (sourceEtapeUuid === targetColumnId)
        continue

      const sourceEtape = detail.etapes.find(e => e.etape_uuid === sourceEtapeUuid)
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

    const newEtapes = detail.etapes.map((etape) => {
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
    queryCache.setQueryData(key, { ...detail, etapes: newEtapes })
  }

  const filters = useCandidaturesFilters(etapes, candidatureListe)

  watch(recrutementUuid, () => {
    filters.reset()
  })

  return {
    recrutementUuid,
    recrutementDetail,
    intitule,
    candidatureListe,
    etapes,
    totalCount,
    pending,
    error,
    moveCandidature,
    moveCandidaturesBatch,
    filters,
  }
})
