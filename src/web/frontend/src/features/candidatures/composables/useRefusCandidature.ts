import type { MaybeRefOrGetter } from 'vue'
import type { Candidat, MotifRefus, RecrutementListe } from '../types'
import { useQuery } from '@pinia/colada'
import { computed, shallowRef, toValue } from 'vue'
import { motifsRefusQuery } from '../queries'

interface PendingRefus {
  candidats: Candidat[]
  apply: (motifRefus: MotifRefus) => void
}

export function useRefusCandidature(
  organismeUuid: MaybeRefOrGetter<string>,
  etapes: MaybeRefOrGetter<RecrutementListe['etapes']>,
) {
  const pending = shallowRef<PendingRefus | null>(null)

  const motifs = useQuery(() => motifsRefusQuery({ organismeUuid: toValue(organismeUuid) }))

  const refusEtapeUuid = computed(() => toValue(etapes).find(etape => etape.motif_refus_required)?.uuid ?? null)

  function isMotifRequired(etapeUuid: string): boolean {
    return toValue(etapes).find(etape => etape.uuid === etapeUuid)?.motif_refus_required ?? false
  }

  function moveOrAskRejectionReason(
    etapeCibleUuid: string,
    candidats: Candidat[],
    move: (motifRefus?: MotifRefus) => void,
  ): void {
    if (isMotifRequired(etapeCibleUuid)) {
      pending.value = { candidats, apply: move }
    }
    else {
      move()
    }
  }

  function confirm(motifRefus: MotifRefus): void {
    const { apply } = pending.value ?? {}
    pending.value = null
    apply?.(motifRefus)
  }

  function cancel(): void {
    pending.value = null
  }

  return {
    refusEtapeUuid,
    isOpen: computed(() => pending.value !== null),
    candidats: computed(() => pending.value?.candidats ?? []),
    motifs: computed(() => motifs.data.value ?? []),
    motifsUnavailable: computed(() => motifs.status.value === 'error'),
    moveOrAskRejectionReason,
    confirm,
    cancel,
  }
}
