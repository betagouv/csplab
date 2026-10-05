import type { Ref } from 'vue'
import type { CandidatureDetail, MotifRefus } from '../types'
import { useToast } from '@/composables/ui/useToast'
import { formatCandidatNom } from '../utils/candidat'
import { useCandidatures } from './useCandidatures'
import { useEtapeChangeMutation } from './useEtapeChangeMutation'
import { useRefusCandidature } from './useRefusCandidature'

export function useEtapeChange(
  candidature: Ref<CandidatureDetail | undefined>,
  leaveMovedCandidature: () => void,
) {
  const { recrutementParams, recrutementEtapes } = useCandidatures()
  const { changeEtape } = useEtapeChangeMutation(recrutementParams)
  const { addToast, dismissToast } = useToast()
  const refus = useRefusCandidature()

  let lastToastId: number | null = null

  async function confirm(targetEtapeUuid: string, motifRefus?: MotifRefus): Promise<void> {
    const moved = candidature.value
    const target = recrutementEtapes.value.find(candidate => candidate.uuid === targetEtapeUuid)
    if (!moved || !target) {
      return
    }

    leaveMovedCandidature()
    const saved = changeEtape({ etapeCibleUuid: targetEtapeUuid, candidatureUuids: [moved.uuid], motifRefus })

    if (!await saved) {
      return
    }

    if (lastToastId !== null) {
      dismissToast(lastToastId)
    }
    lastToastId = addToast({
      variant: 'success',
      title: `${formatCandidatNom(moved.candidat)} est passé à l'étape ${target.nom}`,
    })
  }

  function request(targetEtapeUuid: string): void {
    const target = recrutementEtapes.value.find(candidate => candidate.uuid === targetEtapeUuid)
    if (target?.categorie === 'REFUS' && candidature.value) {
      refus.request([candidature.value.candidat], motifRefus => void confirm(targetEtapeUuid, motifRefus))
    }
    else {
      void confirm(targetEtapeUuid)
    }
  }

  return { etapes: recrutementEtapes, request, refus }
}
