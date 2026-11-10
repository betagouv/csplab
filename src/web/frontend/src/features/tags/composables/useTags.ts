import type { CreateTagPayload, UpdateTagPayload } from '../types'
import { useMutation, useQuery, useQueryCache } from '@pinia/colada'
import { organismeKeys } from '@/api/queryKeys'
import { createTag, updateTag } from '../api'
import { tagsQuery } from '../queries'

export function useTags(organismeUuid: string) {
  const queryCache = useQueryCache()
  const query = useQuery(() => tagsQuery({ organismeUuid }))

  const createMutation = useMutation({
    mutation: (payload: CreateTagPayload) => createTag(organismeUuid, payload),
    onSettled: () => queryCache.invalidateQueries({ key: organismeKeys.tags({ organismeUuid }) }),
  })

  const updateMutation = useMutation({
    mutation: ({ tagUuid, payload }: { tagUuid: string, payload: UpdateTagPayload }) => updateTag(organismeUuid, tagUuid, payload),
    onSettled: () => queryCache.invalidateQueries({ key: organismeKeys.tags({ organismeUuid }) }),
  })

  return {
    tags: query.data,
    pending: query.isPending,
    error: query.error,
    createTag: createMutation.mutateAsync,
    creatingTag: createMutation.isLoading,
    updateTag: updateMutation.mutateAsync,
    updatingTag: updateMutation.isLoading,
  }
}
