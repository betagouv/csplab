import type { MaybeRefOrGetter } from 'vue'
import type { CreateNotePayload, Note, NoteVisibilitePayload, UpdateNotePayload } from '../types'
import type { CandidatureParams, NoteParams, NoteTagParams } from '@/api/params'
import { useMutation, useQuery, useQueryCache } from '@pinia/colada'
import { computed, toValue } from 'vue'
import { candidatureKeys } from '@/api/queryKeys'
import { addCandidatureNoteTag, createCandidatureNote, deleteCandidatureNote, removeCandidatureNoteTag, updateCandidatureNote, updateCandidatureNoteVisibilite } from '../api'
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
    mutation: (payload: CreateNotePayload) => createCandidatureNote(toValue(candidature), payload),
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

export function useUpdateCandidatureNote(candidature: MaybeRefOrGetter<CandidatureParams>) {
  const queryCache = useQueryCache()

  const mutation = useMutation({
    mutation: ({ noteUuid, ...payload }: Pick<NoteParams, 'noteUuid'> & UpdateNotePayload) =>
      updateCandidatureNote({ ...toValue(candidature), noteUuid }, payload),
    onSuccess: () => {
      queryCache.invalidateQueries({ key: candidatureKeys.notes(toValue(candidature)) })
      queryCache.invalidateQueries({ key: candidatureKeys.activites(toValue(candidature)) })
    },
  })

  return {
    update: mutation.mutateAsync,
    updating: mutation.isLoading,
  }
}

export function useUpdateCandidatureNoteVisibilite(candidature: MaybeRefOrGetter<CandidatureParams>) {
  const queryCache = useQueryCache()

  const mutation = useMutation({
    mutation: ({ noteUuid, ...payload }: Pick<NoteParams, 'noteUuid'> & NoteVisibilitePayload) =>
      updateCandidatureNoteVisibilite({ ...toValue(candidature), noteUuid }, payload),
    onSuccess: () => {
      queryCache.invalidateQueries({ key: candidatureKeys.notes(toValue(candidature)) })
      queryCache.invalidateQueries({ key: candidatureKeys.activites(toValue(candidature)) })
    },
  })

  return {
    updateVisibilite: mutation.mutateAsync,
    updatingVisibilite: mutation.isLoading,
  }
}

export function useDeleteCandidatureNote(candidature: MaybeRefOrGetter<CandidatureParams>) {
  const queryCache = useQueryCache()

  const mutation = useMutation({
    mutation: (noteUuid: string) => deleteCandidatureNote({ ...toValue(candidature), noteUuid }),
    onSuccess: () => {
      queryCache.invalidateQueries({ key: candidatureKeys.notes(toValue(candidature)) })
      queryCache.invalidateQueries({ key: candidatureKeys.activites(toValue(candidature)) })
    },
  })

  return {
    remove: mutation.mutateAsync,
    removing: mutation.isLoading,
  }
}

export function useCandidatureNoteTags(candidature: MaybeRefOrGetter<CandidatureParams>) {
  const queryCache = useQueryCache()

  const invalidateNotes = () => queryCache.invalidateQueries({ key: candidatureKeys.notes(toValue(candidature)) })

  const addMutation = useMutation({
    mutation: ({ noteUuid, tagUuid }: Pick<NoteTagParams, 'noteUuid' | 'tagUuid'>) =>
      addCandidatureNoteTag({ ...toValue(candidature), noteUuid, tagUuid }),
    onSettled: invalidateNotes,
  })

  const removeMutation = useMutation({
    mutation: ({ noteUuid, tagUuid }: Pick<NoteTagParams, 'noteUuid' | 'tagUuid'>) =>
      removeCandidatureNoteTag({ ...toValue(candidature), noteUuid, tagUuid }),
    onSettled: invalidateNotes,
  })

  return {
    addTag: addMutation.mutateAsync,
    removeTag: removeMutation.mutateAsync,
  }
}
