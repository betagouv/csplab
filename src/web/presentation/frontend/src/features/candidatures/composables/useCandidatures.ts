import type { InjectionKey, Ref, ShallowRef } from 'vue'
import type {
  Candidature,
  EtapeRecrutementDetailedCandidatures,
  PaginatedCandidatureListeList,
  RecrutementDetailKanban,
} from '../types'
import type { CandidaturesFiltersContext } from './useCandidaturesFilters'
import { useQuery, useQueryCache } from '@pinia/colada'
import { computed, inject, provide, shallowRef, watch } from 'vue'
import { peekRecrutementIntitule } from '@/features/recrutements/queries'
import { candidatureListeQuery, recrutementKanbanQuery } from '../queries'
import { useCandidaturesFilters } from './useCandidaturesFilters'

export interface MoveCandidatureParams {
  sourceColumnId: string
  targetColumnId: string
  cardId: string
}

export interface CandidaturesContext {
  recrutementUuid: string
  recrutementDetail: Ref<RecrutementDetailKanban | null>
  intitule: Ref<string | null>
  candidatureListe: Ref<PaginatedCandidatureListeList | undefined>
  etapes: ShallowRef<EtapeRecrutementDetailedCandidatures[]>
  totalCount: Ref<number>
  pending: Ref<boolean>
  error: Ref<unknown>
  moveCandidature: (params: MoveCandidatureParams) => void
  filters: CandidaturesFiltersContext
}

const CANDIDATURES_KEY: InjectionKey<CandidaturesContext> = Symbol('candidatures')

export function provideCandidatures(
  organismeUuid: string,
  recrutementUuid: string,
): CandidaturesContext {
  const kanban = useQuery(recrutementKanbanQuery({ organismeUuid, recrutementUuid }))
  const liste = useQuery(candidatureListeQuery({ organismeUuid, recrutementUuid }))

  const recrutementDetail = computed<RecrutementDetailKanban | null>(
    () => kanban.data.value ?? null,
  )
  const candidatureListe = liste.data as Ref<PaginatedCandidatureListeList | undefined>
  const etapes = shallowRef<EtapeRecrutementDetailedCandidatures[]>([])

  watch(kanban.data, (data) => {
    etapes.value = data ? structuredClone(data.etapes) : []
  }, { immediate: true })

  const queryCache = useQueryCache()
  const intitule = computed<string | null>(() =>
    recrutementDetail.value?.intitule
    ?? peekRecrutementIntitule(queryCache, organismeUuid, recrutementUuid),
  )

  const pending = computed(() => kanban.isPending.value || liste.isPending.value)
  const error = computed<unknown>(() => kanban.error.value ?? liste.error.value)

  const totalCount = computed(() =>
    etapes.value.reduce((sum, etape) => sum + etape.candidatures.length, 0),
  )

  function moveCandidature(params: MoveCandidatureParams): void {
    const { sourceColumnId, targetColumnId, cardId } = params

    if (sourceColumnId === targetColumnId)
      return

    const sourceEtape = etapes.value.find(e => e.etape_uuid === sourceColumnId)
    const targetEtape = etapes.value.find(e => e.etape_uuid === targetColumnId)

    if (!sourceEtape || !targetEtape)
      return

    const candidatureIndex = sourceEtape.candidatures.findIndex(c => c.uuid === cardId)
    if (candidatureIndex === -1)
      return

    const candidature = sourceEtape.candidatures[candidatureIndex] as Candidature

    const newEtapes = etapes.value.map((etape) => {
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

    etapes.value = newEtapes
  }

  const filters = useCandidaturesFilters(etapes, candidatureListe)

  const context: CandidaturesContext = {
    recrutementUuid,
    recrutementDetail,
    intitule,
    candidatureListe,
    etapes,
    totalCount,
    pending,
    error,
    moveCandidature,
    filters,
  }

  provide(CANDIDATURES_KEY, context)

  return context
}

export function useCandidatures(): CandidaturesContext {
  const context = inject(CANDIDATURES_KEY)
  if (!context) {
    throw new Error('useCandidatures must be used within CandidaturesView')
  }
  return context
}
