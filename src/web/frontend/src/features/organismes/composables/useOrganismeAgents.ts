import type { MaybeRefOrGetter } from 'vue'
import type { UpdateAgentRolePayload } from '../types'
import { useMutation, useQuery, useQueryCache } from '@pinia/colada'
import { toValue } from 'vue'
import { updateAgentRole } from '../api'
import { invalidateOrganisme, organismeAgentsQuery } from '../queries'

export function useOrganismeAgents(organismeUuid: MaybeRefOrGetter<string>) {
  const queryCache = useQueryCache()
  const query = useQuery(() => organismeAgentsQuery({ organismeUuid: toValue(organismeUuid) }))

  const updateMutation = useMutation({
    mutation: (payload: UpdateAgentRolePayload) => updateAgentRole(toValue(organismeUuid), payload),
    onSettled: () => invalidateOrganisme(queryCache, { organismeUuid: toValue(organismeUuid) }),
  })

  return {
    agents: query.data,
    pending: query.isPending,
    error: query.error,
    updateAgent: updateMutation.mutateAsync,
    updatingAgent: updateMutation.isLoading,
  }
}
