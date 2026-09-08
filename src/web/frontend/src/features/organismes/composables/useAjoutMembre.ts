import type { AgentRecherche, Role, SetAgentRolePayload } from '../types'
import { useMutation, useQueryCache } from '@pinia/colada'
import { ref } from 'vue'
import { searchAgentByEmail, setAgentRole } from '../api'
import { ORGANISMES_QUERY_KEYS } from '../queries'

export type AgentSearchStatus = 'idle' | 'found' | 'not-found'

export function useAjoutMembre(organismeUuid: string) {
  const queryCache = useQueryCache()

  const status = ref<AgentSearchStatus>('idle')
  const foundAgent = ref<AgentRecherche | null>(null)
  const searching = ref(false)

  function reset(): void {
    status.value = 'idle'
    foundAgent.value = null
  }

  async function search(email: string): Promise<AgentSearchStatus> {
    reset()
    searching.value = true
    try {
      const agent = await searchAgentByEmail(organismeUuid, email)
      foundAgent.value = agent
      status.value = agent ? 'found' : 'not-found'
      return status.value
    }
    finally {
      searching.value = false
    }
  }

  const attachMutation = useMutation({
    mutation: (payload: SetAgentRolePayload) => setAgentRole(organismeUuid, payload),
    onSettled: () => queryCache.invalidateQueries({ key: ORGANISMES_QUERY_KEYS.root }),
  })

  function attach(role: Role) {
    if (!foundAgent.value)
      throw new Error('Aucun agent à rattacher.')
    return attachMutation.mutateAsync({ agent_id: foundAgent.value.agent_id, role })
  }

  return {
    status,
    foundAgent,
    searching,
    search,
    attach,
    attaching: attachMutation.isLoading,
    reset,
  }
}
