import type { MaybeRefOrGetter } from 'vue'
import type { CandidatureParams } from '@/api/params'
import { useMutation, useQueryCache } from '@pinia/colada'
import { toValue } from 'vue'
import { candidatureKeys, recrutementKeys } from '@/api/queryKeys'
import { addCandidatureTag, removeCandidatureTag } from '../api'

export function useCandidatureTags(candidature: MaybeRefOrGetter<CandidatureParams>) {
  const queryCache = useQueryCache()

  function invalidate(): void {
    void queryCache.invalidateQueries({ key: candidatureKeys.detail(toValue(candidature)) })
    void queryCache.invalidateQueries({ key: recrutementKeys.liste(toValue(candidature)) })
  }

  const addMutation = useMutation({
    mutation: (tagUuid: string) => addCandidatureTag({ ...toValue(candidature), tagUuid }),
    onSettled: invalidate,
  })

  const removeMutation = useMutation({
    mutation: (tagUuid: string) => removeCandidatureTag({ ...toValue(candidature), tagUuid }),
    onSettled: invalidate,
  })

  return {
    addTag: addMutation.mutateAsync,
    removeTag: removeMutation.mutateAsync,
  }
}
