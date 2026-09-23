import type { MaybeRefOrGetter } from 'vue'
import type { CandidatureParams, Note } from '../types'
import { useMutation, useQuery, useQueryCache } from '@pinia/colada'
import { computed, toValue } from 'vue'
import { createCandidatureNote } from '../api'
import { candidatureNotesQuery, CANDIDATURES_QUERY_KEYS } from '../queries'

export function useCandidatureNotes(candidature: MaybeRefOrGetter<CandidatureParams>) {
  const query = useQuery(() => candidatureNotesQuery(toValue(candidature)))

  return {
    notes: computed<Note[]>(() => query.data.value?.results ?? []),
    total: computed(() => query.data.value?.count ?? 0),
    pending: computed(() => query.isPending.value),
    error: computed(() => query.error.value),
  }
}

export function useCreateCandidatureNote(candidature: MaybeRefOrGetter<CandidatureParams>) {
  const queryCache = useQueryCache()

  const mutation = useMutation({
    mutation: (message: string) => createCandidatureNote(toValue(candidature), message),
    onSuccess: () => {
      queryCache.invalidateQueries({ key: CANDIDATURES_QUERY_KEYS.notes(toValue(candidature)) })
    },
  })

  return {
    create: mutation.mutateAsync,
    creating: mutation.isLoading,
  }
}
