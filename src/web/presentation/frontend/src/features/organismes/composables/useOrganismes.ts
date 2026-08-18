import type { CreateOrganismePayload, UpdateOrganismePayload } from '../types'
import { useMutation, useQuery, useQueryCache } from '@pinia/colada'
import { createOrganisme, updateOrganisme } from '../api'
import { ORGANISMES_QUERY_KEYS, organismesQuery } from '../queries'

export function useOrganismes() {
  const queryCache = useQueryCache()
  const query = useQuery(organismesQuery)

  function invalidate() {
    return queryCache.invalidateQueries({ key: ORGANISMES_QUERY_KEYS.root })
  }

  const createMutation = useMutation({
    mutation: (payload: CreateOrganismePayload) => createOrganisme(payload),
    onSettled: invalidate,
  })

  const updateMutation = useMutation({
    mutation: ({ uuid, payload }: { uuid: string, payload: UpdateOrganismePayload }) =>
      updateOrganisme(uuid, payload),
    onSettled: invalidate,
  })

  return {
    organismes: query.data,
    pending: query.isPending,
    error: query.error,
    create: createMutation.mutateAsync,
    creating: createMutation.isLoading,
    update: updateMutation.mutateAsync,
    updating: updateMutation.isLoading,
  }
}
