import type { MaybeRefOrGetter } from 'vue'
import type { CreateTagPayload, UpdateTagPayload } from '../types'
import { useMutation, useQuery, useQueryCache } from '@pinia/colada'
import { toValue } from 'vue'
import { organismeKeys } from '@/api/queryKeys'
import { createTag, updateTag } from '../api'
import { tagsQuery } from '../queries'

export function useTags(organismeUuid: MaybeRefOrGetter<string>) {
  const queryCache = useQueryCache()
  const query = useQuery(() => tagsQuery({ organismeUuid: toValue(organismeUuid) }))

  const createMutation = useMutation({
    mutation: (payload: CreateTagPayload) => createTag(toValue(organismeUuid), payload),
    onSettled: () => queryCache.invalidateQueries({ key: organismeKeys.tags({ organismeUuid: toValue(organismeUuid) }) }),
  })

  const updateMutation = useMutation({
    mutation: ({ tagUuid, payload }: { tagUuid: string, payload: UpdateTagPayload }) => updateTag(toValue(organismeUuid), tagUuid, payload),
    onSettled: () => queryCache.invalidateQueries({ key: organismeKeys.tags({ organismeUuid: toValue(organismeUuid) }) }),
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
