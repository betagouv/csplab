import type { Candidature, RecrutementDetailKanban } from '../types'
import type { RecrutementDetail } from '@/features/recrutements/types'
import { defineQuery, useQuery, useQueryCache } from '@pinia/colada'
import { computed, watch } from 'vue'
import { useRoute } from 'vue-router'
import { useToast } from '@/composables/ui/useToast'
import { peekRecrutementIntitule, recrutementDetailQuery } from '@/features/recrutements/queries'
import { useCurrentOrganisme } from '@/stores/currentOrganisme'
import { patchEtapeCandidatures } from '../api'
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

  const { organismeUuid } = useCurrentOrganisme()

  const isKanbanRoute = computed(() => route.name === 'recrutement-candidatures-kanban')
  const isListeRoute = computed(() => route.name === 'recrutement-candidatures')

  const queryCache = useQueryCache()

  const detail = useQuery(() => ({
    ...recrutementDetailQuery({
      organismeUuid: organismeUuid.value ?? '',
      recrutementUuid: recrutementUuid.value ?? '',
    }),
    enabled: (
      recrutementUuid.value !== null
      && organismeUuid.value !== null
    ),
  }))

  const kanban = useQuery(() => ({
    ...recrutementKanbanQuery({
      organismeUuid: organismeUuid.value ?? '',
      recrutementUuid: recrutementUuid.value ?? '',
    }),
    enabled: (
      recrutementUuid.value !== null
      && isKanbanRoute.value
      && organismeUuid.value !== null
    ),
  }))

  const liste = useQuery(() => ({
    ...candidatureListeQuery({
      organismeUuid: organismeUuid.value ?? '',
      recrutementUuid: recrutementUuid.value ?? '',
    }),
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

  const totalCount = computed(() =>
    candidatureKanban.value.reduce((sum, etape) => sum + etape.candidatures.length, 0),
  )

  const { addToast } = useToast()

  function kanbanQueryKey() {
    return recrutementKanbanQuery({
      organismeUuid: organismeUuid.value!,
      recrutementUuid: recrutementUuid.value!,
    }).key
  }

  async function persistEtapeChange(
    targetColumnId: string,
    candidatureUuids: string[],
    previousData: RecrutementDetailKanban,
  ): Promise<void> {
    const key = kanbanQueryKey()
    try {
      const resultat = await patchEtapeCandidatures(
        organismeUuid.value!,
        recrutementUuid.value!,
        targetColumnId,
        candidatureUuids,
      )
      if (resultat.echecs.length > 0) {
        await queryCache.invalidateQueries({ key })
        addToast({
          variant: 'warning',
          title: 'Certaines candidatures n\'ont pas changé d\'étape',
        })
      }
    }
    catch {
      queryCache.setQueryData(key, previousData)
      addToast({
        variant: 'error',
        title: 'Le changement d\'étape a échoué',
        description: 'Vos candidatures sont restées à leur étape actuelle.',
      })
    }
  }

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

    queryCache.setQueryData(kanbanQueryKey(), { ...kanbanData, etapes: newEtapes })
    void persistEtapeChange(targetColumnId, [cardId], kanbanData)
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

    queryCache.setQueryData(kanbanQueryKey(), { ...kanbanData, etapes: newEtapes })
    void persistEtapeChange(
      targetColumnId,
      candidaturesToMove.map(c => c.uuid),
      kanbanData,
    )
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
