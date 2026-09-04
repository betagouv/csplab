import type { SetAgentRolePayload, UpdateAgentRolePayload } from '../types'
import { useMutation, useQuery, useQueryCache } from '@pinia/colada'
import { setAgentRole, updateAgentRole } from '../api'
import { organismeAgentsQuery, ORGANISMES_QUERY_KEYS } from '../queries'

export function useOrganismeAgents(organismeUuid: string) {
  const queryCache = useQueryCache()
  const query = useQuery(() => organismeAgentsQuery({ organismeUuid }))

  function invalidate() {
    return queryCache.invalidateQueries({ key: ORGANISMES_QUERY_KEYS.root })
  }

  const attachMutation = useMutation({
    mutation: (payload: SetAgentRolePayload) => setAgentRole(organismeUuid, payload),
    onSettled: invalidate,
  })

  const updateMutation = useMutation({
    mutation: (payload: UpdateAgentRolePayload) => updateAgentRole(organismeUuid, payload),
    onSettled: invalidate,
  })

  return {
    agents: query.data,
    pending: query.isPending,
    error: query.error,
    attachAgent: attachMutation.mutateAsync,
    attachingAgent: attachMutation.isLoading,
    updateAgent: updateMutation.mutateAsync,
    updatingAgent: updateMutation.isLoading,
  }
}
