import type { MaybeRefOrGetter } from 'vue'
import type { Candidature, EtapeRecrutementDetailedCandidatures, RecrutementDetailKanban } from '../types'
import { computed, ref, shallowRef, toValue } from 'vue'
import { useAsyncState } from '@/composables/async/useAsyncState'
import { getRecrutementKanban } from '../api'

export interface MoveCandidatureParams {
  sourceColumnId: string
  targetColumnId: string
  cardId: string
}

export function useCandidaturesKanban(
  organismeUuid: MaybeRefOrGetter<string>,
  recrutementUuid: MaybeRefOrGetter<string>,
) {
  const { pending, error, run } = useAsyncState(true)
  const kanban = ref<RecrutementDetailKanban | null>(null)
  const etapes = shallowRef<EtapeRecrutementDetailedCandidatures[]>([])

  const totalCount = computed(() =>
    etapes.value.reduce((sum, etape) => sum + etape.candidatures.length, 0),
  )

  async function load(): Promise<void> {
    await run(async () => {
      const data = await getRecrutementKanban(
        toValue(organismeUuid),
        toValue(recrutementUuid),
      )
      kanban.value = data
      etapes.value = structuredClone(data.etapes)
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

    // TODO: call API to persist the move
  }

  return {
    kanban,
    etapes,
    totalCount,
    pending,
    error,
    load,
    moveCandidature,
  }
}
