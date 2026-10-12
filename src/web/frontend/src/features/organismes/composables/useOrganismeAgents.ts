import type { UpdateAgentRolePayload } from '../types'
import { useMutation, useQuery, useQueryCache } from '@pinia/colada'
import { updateAgentRole } from '../api'
import { invalidateOrganisme, organismeAgentsQuery } from '../queries'

export function useOrganismeAgents(organismeUuid: string) {
  const queryCache = useQueryCache()
  const query = useQuery(() => organismeAgentsQuery({ organismeUuid }))

  const updateMutation = useMutation({
    mutation: (payload: UpdateAgentRolePayload) => updateAgentRole(organismeUuid, payload),
    onSettled: () => invalidateOrganisme(queryCache, { organismeUuid }),
  })

  return {
    agents: query.data,
    pending: query.isPending,
    error: query.error,
    updateAgent: updateMutation.mutateAsync,
    updatingAgent: updateMutation.isLoading,
  }
}
