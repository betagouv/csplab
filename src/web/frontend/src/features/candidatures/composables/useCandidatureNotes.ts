import type { MaybeRefOrGetter } from 'vue'
import type { Note } from '../types'
import type { CandidatureParams } from '@/api/params'
import { useMutation, useQuery, useQueryCache } from '@pinia/colada'
import { computed, toValue } from 'vue'
import { candidatureKeys } from '@/api/queryKeys'
import { createCandidatureNote } from '../api'
import { candidatureNotesQuery } from '../queries'

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
      queryCache.invalidateQueries({ key: candidatureKeys.notes(toValue(candidature)) })
      queryCache.invalidateQueries({ key: candidatureKeys.activites(toValue(candidature)) })
    },
  })

  return {
    create: mutation.mutateAsync,
    creating: mutation.isLoading,
  }
}
