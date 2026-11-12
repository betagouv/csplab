import type { MaybeRefOrGetter } from 'vue'
import type { Candidat, EtapeRecrutement, MotifRefus } from '../types'
import { useQuery } from '@pinia/colada'
import { computed, shallowRef, toValue } from 'vue'
import { motifsRefusQuery } from '../queries'

interface PendingRefus {
  candidats: Candidat[]
  apply: (motifRefus: MotifRefus) => void
}

export function useRefusCandidature(
  organismeUuid: MaybeRefOrGetter<string>,
  etapes: MaybeRefOrGetter<EtapeRecrutement[]>,
) {
  const pending = shallowRef<PendingRefus | null>(null)

  const motifs = useQuery(() => motifsRefusQuery({ organismeUuid: toValue(organismeUuid) }))

  const refusEtapeUuid = computed(() => toValue(etapes).find(etape => etape.categorie === 'REFUS')?.uuid ?? null)

  function moveOrAskRejectionReason(
    etapeCibleUuid: string,
    candidats: Candidat[],
    move: (motifRefus?: MotifRefus) => void,
  ): void {
    if (etapeCibleUuid === refusEtapeUuid.value) {
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
