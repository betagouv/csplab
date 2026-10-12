import type { CreateOrganismePayload, UpdateOrganismePayload } from '../types'
import { useMutation, useQuery, useQueryCache } from '@pinia/colada'
import { organismeKeys } from '@/api/queryKeys'
import { createOrganisme, updateOrganisme } from '../api'
import { invalidateOrganisme, organismesListQuery } from '../queries'

export function useOrganismes() {
  const queryCache = useQueryCache()
  const query = useQuery(organismesListQuery)

  const createMutation = useMutation({
    mutation: (payload: CreateOrganismePayload) => createOrganisme(payload),
    onSettled: () => queryCache.invalidateQueries({ key: organismeKeys.list() }),
  })

  const updateMutation = useMutation({
    mutation: ({ organismeUuid, payload }: { organismeUuid: string, payload: UpdateOrganismePayload }) =>
      updateOrganisme(organismeUuid, payload),
    onSettled: (_data, _error, { organismeUuid }) => invalidateOrganisme(queryCache, { organismeUuid }),
  })

  return {
    organismesList: query.data,
    pending: query.isPending,
    error: query.error,
    create: createMutation.mutateAsync,
    creating: createMutation.isLoading,
    update: updateMutation.mutateAsync,
    updating: updateMutation.isLoading,
  }
}
