import type { AgentOrganisme, Role } from '../types'
import { useMutation, useQuery, useQueryCache } from '@pinia/colada'
import { updateAgentRole } from '../api'
import { invalidateOrganisme, organismeAgentsQuery } from '../queries'

export function useOrganismeAgents(organismeUuid: string) {
  const queryCache = useQueryCache()
  const query = useQuery(() => organismeAgentsQuery({ organismeUuid }))

  function invalidate() {
    return invalidateOrganisme(queryCache, { organismeUuid })
  }

  const revokeMutation = useMutation({
    mutation: (agent: AgentOrganisme) => updateAgentRole(organismeUuid, {
      agent_id: agent.uuid,
      role: agent.role,
      date_revocation: new Date().toISOString(),
    }),
    onSettled: invalidate,
  })

  const roleMutation = useMutation({
    mutation: ({ agent, role }: { agent: AgentOrganisme, role: Role }) =>
      updateAgentRole(organismeUuid, {
        agent_id: agent.uuid,
        role,
      }),
    onSettled: invalidate,
  })

  return {
    agents: query.data,
    pending: query.isPending,
    error: query.error,
    revoke: revokeMutation.mutateAsync,
    revoking: revokeMutation.isLoading,
    changeRole: roleMutation.mutateAsync,
    changingRole: roleMutation.isLoading,
  }
}
