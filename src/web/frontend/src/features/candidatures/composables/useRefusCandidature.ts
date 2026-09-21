import type { Candidat, MotifRefus } from '../types'
import { useQuery } from '@pinia/colada'
import { computed, shallowRef } from 'vue'
import { motifsRefusQuery } from '../queries'
import { useCandidatures } from './useCandidatures'

interface PendingRefus {
  candidats: Candidat[]
  apply: (motifRefus: MotifRefus) => void
}

export function useRefusCandidature() {
  const { organismeUuid } = useCandidatures()
  const pending = shallowRef<PendingRefus | null>(null)

  const motifs = useQuery(() => ({
    ...motifsRefusQuery({ organismeUuid: organismeUuid.value ?? '' }),
    enabled: organismeUuid.value !== null,
  }))

  function request(candidats: Candidat[], apply: PendingRefus['apply']): void {
    pending.value = { candidats, apply }
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
    isOpen: computed(() => pending.value !== null),
    candidats: computed(() => pending.value?.candidats ?? []),
    motifs: computed(() => motifs.data.value ?? []),
    motifsUnavailable: computed(() => motifs.status.value === 'error'),
    request,
    confirm,
    cancel,
  }
}
