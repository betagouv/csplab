import type { MaybeRefOrGetter, Ref } from 'vue'
import type { CandidatureDetail, MotifRefus } from '../types'
import type { RecrutementParams } from '@/api/params'
import { toValue } from 'vue'
import { useRecrutementDetail } from '@/features/recrutements/composables/useRecrutementDetail'
import { useEtapeChangeMutation } from './useEtapeChangeMutation'
import { useRefusCandidature } from './useRefusCandidature'

export function useEtapeChange(
  recrutement: MaybeRefOrGetter<RecrutementParams>,
  candidature: Ref<CandidatureDetail | undefined>,
  leaveMovedCandidature: () => void,
) {
  const { etapes: recrutementEtapes } = useRecrutementDetail(recrutement)
  const { changeEtape } = useEtapeChangeMutation(recrutement)
  const refus = useRefusCandidature(() => toValue(recrutement).organismeUuid, recrutementEtapes)

  function confirm(targetEtapeUuid: string, motifRefus?: MotifRefus): void {
    const moved = candidature.value
    const target = recrutementEtapes.value.find(candidate => candidate.uuid === targetEtapeUuid)
    if (!moved || !target) {
      return
    }

    leaveMovedCandidature()
    void changeEtape({ etapeCibleUuid: targetEtapeUuid, candidatureUuids: [moved.uuid], motifRefus }, [moved.candidat])
  }

  function request(targetEtapeUuid: string): void {
    if (!candidature.value) {
      return
    }
    refus.moveOrAskRejectionReason(
      targetEtapeUuid,
      [candidature.value.candidat],
      motifRefus => confirm(targetEtapeUuid, motifRefus),
    )
  }

  return { etapes: recrutementEtapes, request, refus }
}
