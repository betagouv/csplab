import type { Ref } from 'vue'
import type { Candidature, EtapeRecrutement, EtapeRecrutementDetailedCandidatures } from '../types'
import type { MoveCandidatureParams } from './useCandidatures'
import type { KanbanDropEvent } from '@/composables/dnd/useKanbanDnd'
import { computed, ref } from 'vue'
import { formatCandidatNom } from '../utils/candidat'

interface UseRefusCandidatureOptions {
  recrutementEtapes: Ref<EtapeRecrutement[]>
  candidatureKanban: Ref<EtapeRecrutementDetailedCandidatures[]>
  moveCandidature: (params: MoveCandidatureParams) => void
}

export function useRefusCandidature(options: UseRefusCandidatureOptions) {
  const pendingMove = ref<KanbanDropEvent | null>(null)

  const refusEtapeUuid = computed(() =>
    options.recrutementEtapes.value.find(etape => etape.categorie === 'REFUS')?.etape_uuid ?? null,
  )

  const pendingCandidature = computed<Candidature | null>(() => {
    const move = pendingMove.value
    if (!move)
      return null
    const etape = options.candidatureKanban.value.find(e => e.etape_uuid === move.sourceColumnId)
    return etape?.candidatures.find(c => c.uuid === move.cardId) ?? null
  })

  const isDialogOpen = computed(() => pendingMove.value !== null)

  const description = computed(() => {
    const candidat = pendingCandidature.value ? formatCandidatNom(pendingCandidature.value.candidat) : 'ce candidat'
    return `Vous êtes sur le point de refuser la candidature de ${candidat}. `
      + `Cette action n'est pas définitive, néanmoins le candidat sera informé du changement `
      + `de statut de sa candidature.`
  })

  function handleMove(event: KanbanDropEvent): void {
    if (event.sourceColumnId !== event.targetColumnId && event.targetColumnId === refusEtapeUuid.value) {
      pendingMove.value = event
      return
    }
    options.moveCandidature(event)
  }

  function confirm(): void {
    if (!pendingMove.value)
      return
    options.moveCandidature(pendingMove.value)
    pendingMove.value = null
  }

  function cancel(): void {
    pendingMove.value = null
  }

  return {
    refusEtapeUuid,
    pendingCandidature,
    isDialogOpen,
    description,
    handleMove,
    confirm,
    cancel,
  }
}
