import type { InjectionKey, Ref, ShallowRef } from 'vue'
import type {
  Candidature,
  EtapeRecrutementDetailedCandidatures,
  PaginatedCandidatureListeResponse,
  RecrutementDetailKanban,
} from '../types'
import { computed, inject, provide, ref, shallowRef } from 'vue'
import { useAsyncState } from '@/composables/async/useAsyncState'
import { getCandidatureListe, getRecrutementKanban } from '../api'

export interface MoveCandidatureParams {
  sourceColumnId: string
  targetColumnId: string
  cardId: string
}

export interface CandidaturesContext {
  recrutementUuid: string
  recrutementDetail: Ref<RecrutementDetailKanban | null>
  candidatureListe: Ref<PaginatedCandidatureListeResponse | undefined>
  etapes: ShallowRef<EtapeRecrutementDetailedCandidatures[]>
  totalCount: Ref<number>
  pending: Ref<boolean>
  error: Ref<unknown>
  moveCandidature: (params: MoveCandidatureParams) => void
}

const CANDIDATURES_KEY: InjectionKey<CandidaturesContext> = Symbol('candidatures')

export function provideCandidatures(
  organismeUuid: string,
  recrutementUuid: string,
): CandidaturesContext {
  const { pending, error, run } = useAsyncState(true)
  const recrutementDetail = ref<RecrutementDetailKanban | null>(null)
  const candidatureListe = ref<PaginatedCandidatureListeResponse>()
  const etapes = shallowRef<EtapeRecrutementDetailedCandidatures[]>([])

  const totalCount = computed(() =>
    etapes.value.reduce((sum, etape) => sum + etape.candidatures.length, 0),
  )

  async function load(): Promise<void> {
    await run(async () => {
      const [kanban, liste] = await Promise.all([
        getRecrutementKanban(organismeUuid, recrutementUuid),
        getCandidatureListe(organismeUuid, recrutementUuid),
      ])

      recrutementDetail.value = kanban
      etapes.value = structuredClone(kanban.etapes)
      candidatureListe.value = liste
    })
  }

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

  void load()

  const context: CandidaturesContext = {
    recrutementUuid,
    recrutementDetail,
    candidatureListe,
    etapes,
    totalCount,
    pending,
    error,
    moveCandidature,
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
