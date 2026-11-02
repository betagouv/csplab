import type { CreateTagPayload } from '../types'
import { useMutation, useQuery, useQueryCache } from '@pinia/colada'
import { organismeKeys } from '@/api/queryKeys'
import { createTag } from '../api'
import { tagsQuery } from '../queries'

export function useTags(organismeUuid: string) {
  const queryCache = useQueryCache()
  const query = useQuery(() => tagsQuery({ organismeUuid }))

  const createMutation = useMutation({
    mutation: (payload: CreateTagPayload) => createTag(organismeUuid, payload),
    onSettled: () => queryCache.invalidateQueries({ key: organismeKeys.tags({ organismeUuid }) }),
  })

  return {
    tags: query.data,
    pending: query.isPending,
    error: query.error,
    createTag: createMutation.mutateAsync,
    creatingTag: createMutation.isLoading,
  }
}
