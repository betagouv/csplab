import type { UpdateAgentRolePayload } from '../types'
import { useMutation, useQuery, useQueryCache } from '@pinia/colada'
import { updateAgentRole } from '../api'
import { organismeAgentsQuery, ORGANISMES_QUERY_KEYS } from '../queries'

export function useOrganismeAgents(organismeUuid: string) {
  const queryCache = useQueryCache()
  const query = useQuery(() => organismeAgentsQuery({ organismeUuid }))

  function invalidate() {
    return queryCache.invalidateQueries({ key: ORGANISMES_QUERY_KEYS.root })
  }

  const updateMutation = useMutation({
    mutation: (payload: UpdateAgentRolePayload) => updateAgentRole(organismeUuid, payload),
    onSettled: invalidate,
  })

  return {
    agents: query.data,
    pending: query.isPending,
    error: query.error,
    updateAgent: updateMutation.mutateAsync,
    updatingAgent: updateMutation.isLoading,
  }
}
