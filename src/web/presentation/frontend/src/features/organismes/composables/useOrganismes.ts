import type { CreateOrganismePayload } from '../types'
import { useMutation, useQuery, useQueryCache } from '@pinia/colada'
import { createOrganisme } from '../api'
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

  return {
    organismes: query.data,
    pending: query.isPending,
    error: query.error,
    create: createMutation.mutateAsync,
    creating: createMutation.isLoading,
  }
}
