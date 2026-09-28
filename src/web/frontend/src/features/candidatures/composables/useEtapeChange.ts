import type { Ref } from 'vue'
import type { MotifRefus } from '../types'
import { useToast } from '@/composables/ui/useToast'
import { formatCandidatNom } from '../utils/candidat'
import { useCandidatureNavigation } from './useCandidatureNavigation'
import { useCandidatures } from './useCandidatures'
import { useRefusCandidature } from './useRefusCandidature'

export function useEtapeChange(candidatureUuid: Ref<string>, leavePanel: () => void) {
  const { moveCandidature, recrutementEtapes, findCandidature } = useCandidatures()
  const { position, etape, navigateTo } = useCandidatureNavigation(candidatureUuid)
  const { addToast, dismissToast } = useToast()
  const refus = useRefusCandidature()

  let lastToastId: number | null = null

  async function confirm(targetEtapeUuid: string, motifRefus?: MotifRefus): Promise<void> {
    const candidature = findCandidature(candidatureUuid.value)
    const target = recrutementEtapes.value.find(candidate => candidate.etape_uuid === targetEtapeUuid)
    if (!etape.value || !candidature || !target)
      return

    const movedUuid = candidatureUuid.value
    const nextUuid = position.value?.nextUuid ?? null

    const moved = moveCandidature({
      sourceColumnId: etape.value.etape_uuid,
      targetColumnId: targetEtapeUuid,
      cardId: movedUuid,
      motifRefus,
    })

    if (nextUuid)
      navigateTo(nextUuid)
    else
      leavePanel()

    if (!await moved)
      return

    if (lastToastId !== null)
      dismissToast(lastToastId)
    lastToastId = addToast({
      variant: 'success',
      title: `${formatCandidatNom(candidature.candidat)} est passé à l'étape ${target.nom}`,
    })
  }

  function request(targetEtapeUuid: string): void {
    const candidature = findCandidature(candidatureUuid.value)
    const target = recrutementEtapes.value.find(candidate => candidate.etape_uuid === targetEtapeUuid)
    if (target?.categorie === 'REFUS' && candidature)
      refus.request([candidature.candidat], motifRefus => void confirm(targetEtapeUuid, motifRefus))
    else
      void confirm(targetEtapeUuid)
  }

  return { etapes: recrutementEtapes, request, refus }
}
