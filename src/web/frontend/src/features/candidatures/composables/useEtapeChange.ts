import type { MaybeRefOrGetter, Ref } from 'vue'
import type { CandidatureDetail, MotifRefus } from '../types'
import type { RecrutementParams } from '@/api/params'
import { toValue } from 'vue'
import { useToast } from '@/composables/ui/useToast'
import { useRecrutementDetail } from '@/features/recrutements/composables/useRecrutementDetail'
import { formatCandidatName } from '../format'
import { useEtapeChangeMutation } from './useEtapeChangeMutation'
import { useRefusCandidature } from './useRefusCandidature'

export function useEtapeChange(
  recrutement: MaybeRefOrGetter<RecrutementParams>,
  candidature: Ref<CandidatureDetail | undefined>,
  leaveMovedCandidature: () => void,
) {
  const { etapes: recrutementEtapes } = useRecrutementDetail(recrutement)
  const { changeEtape } = useEtapeChangeMutation(recrutement)
  const { addToast, dismissToast } = useToast()
  const refus = useRefusCandidature(() => toValue(recrutement).organismeUuid, recrutementEtapes)

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
      title: `${formatCandidatName(moved.candidat)} est passé à l'étape ${target.nom}`,
    })
  }

  function request(targetEtapeUuid: string): void {
    if (!candidature.value) {
      return
    }
    refus.moveOrAskRejectionReason(
      targetEtapeUuid,
      [candidature.value.candidat],
      motifRefus => void confirm(targetEtapeUuid, motifRefus),
    )
  }

  return { etapes: recrutementEtapes, request, refus }
}
