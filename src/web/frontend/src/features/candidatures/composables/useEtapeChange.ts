import type { Ref } from 'vue'
import { computed, ref } from 'vue'
import { useToast } from '@/composables/ui/useToast'
import { formatCandidatNom } from '../utils/candidat'
import { useCandidatureNavigation } from './useCandidatureNavigation'
import { useCandidatures } from './useCandidatures'

const TOAST_DURATION = 10_000

export function useEtapeChange(candidatureUuid: Ref<string>, leavePanel: () => void) {
  const { moveCandidature, recrutementEtapes, findCandidature } = useCandidatures()
  const { position, etape, navigateTo } = useCandidatureNavigation(candidatureUuid)
  const { addToast, dismissToast } = useToast()

  let lastToastId: number | null = null
  const pendingRefusEtapeUuid = ref<string | null>(null)
  const isRefusPending = computed(() => pendingRefusEtapeUuid.value !== null)

  function confirm(targetEtapeUuid: string): void {
    const candidature = findCandidature(candidatureUuid.value)
    const target = recrutementEtapes.value.find(candidate => candidate.etape_uuid === targetEtapeUuid)
    if (!etape.value || !candidature || !target)
      return

    const movedUuid = candidatureUuid.value
    const nextUuid = position.value?.nextUuid ?? null

    moveCandidature({
      sourceColumnId: etape.value.etape_uuid,
      targetColumnId: targetEtapeUuid,
      cardId: movedUuid,
    })

    if (lastToastId !== null)
      dismissToast(lastToastId)
    lastToastId = addToast({
      variant: 'success',
      title: `${formatCandidatNom(candidature.candidat)} est passé à l'étape ${target.nom}`,
      duration: TOAST_DURATION,
      action: { label: 'Revenir à cette candidature', icon: 'ri:arrow-go-back-line', onSelect: () => navigateTo(movedUuid) },
    })

    if (nextUuid)
      navigateTo(nextUuid)
    else
      leavePanel()
  }

  function request(targetEtapeUuid: string): void {
    const target = recrutementEtapes.value.find(candidate => candidate.etape_uuid === targetEtapeUuid)
    if (target?.categorie === 'REFUS')
      pendingRefusEtapeUuid.value = targetEtapeUuid
    else
      confirm(targetEtapeUuid)
  }

  function confirmRefus(): void {
    const targetEtapeUuid = pendingRefusEtapeUuid.value
    pendingRefusEtapeUuid.value = null
    if (targetEtapeUuid)
      confirm(targetEtapeUuid)
  }

  function cancelRefus(): void {
    pendingRefusEtapeUuid.value = null
  }

  return { etapes: recrutementEtapes, request, isRefusPending, confirmRefus, cancelRefus }
}
