import type { MaybeRefOrGetter } from 'vue'
import type { MotifRefus } from '../types'
import type { CandidatureParams } from '@/api/params'
import { useMutation, useQueryCache } from '@pinia/colada'
import { toValue } from 'vue'
import { candidatureKeys, recrutementKeys } from '@/api/queryKeys'
import { useToast } from '@/composables/ui/useToast'
import { patchEtapeCandidatures } from '../api'

interface MotifRefusModification {
  etapeUuid: string
  motifRefus: MotifRefus
}

export function useMotifRefusModification(candidature: MaybeRefOrGetter<CandidatureParams>) {
  const queryCache = useQueryCache()
  const { addToast } = useToast()

  const mutation = useMutation({
    mutation: async ({ etapeUuid, motifRefus }: MotifRefusModification) => {
      const { organismeUuid, recrutementUuid, candidatureUuid } = toValue(candidature)
      const { echecs } = await patchEtapeCandidatures(organismeUuid, recrutementUuid, {
        etapeCibleUuid: etapeUuid,
        candidatureUuids: [candidatureUuid],
        motifRefus,
      })
      if (echecs.length > 0) {
        throw new Error(echecs[0]!.raison)
      }
    },
    onSuccess: () => {
      addToast({ variant: 'success', title: 'Le motif de refus a été modifié' })
    },
    onError: () => {
      addToast({ variant: 'error', title: 'La modification du motif de refus a échoué' })
    },
    onSettled: () => {
      void queryCache.invalidateQueries({ key: candidatureKeys.root(toValue(candidature)) })
      void queryCache.invalidateQueries({ key: recrutementKeys.liste(toValue(candidature)) })
    },
  })

  return {
    modifier: mutation.mutate,
    modifying: mutation.isLoading,
  }
}
