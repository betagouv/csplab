import type { Agent, AgentRecherche, CreateAgentPayload, Role, SetAgentRolePayload } from '../types'
import { useMutation, useQueryCache } from '@pinia/colada'
import { computed, ref } from 'vue'
import { createAgent, searchAgentByEmail, setAgentRole } from '../api'
import { ORGANISMES_QUERY_KEYS } from '../queries'

export type AgentSearchStatus = 'idle' | 'found' | 'not-found'

export function useAjoutMembre(organismeUuid: string) {
  const queryCache = useQueryCache()

  const status = ref<AgentSearchStatus>('idle')
  const foundAgent = ref<AgentRecherche | null>(null)
  const searchedEmail = ref('')
  const searching = ref(false)

  function reset(): void {
    status.value = 'idle'
    foundAgent.value = null
    searchedEmail.value = ''
  }

  async function search(email: string): Promise<AgentSearchStatus> {
    reset()
    searching.value = true
    try {
      const agent = await searchAgentByEmail(organismeUuid, email)
      foundAgent.value = agent
      searchedEmail.value = email
      status.value = agent ? 'found' : 'not-found'
      return status.value
    }
    finally {
      searching.value = false
    }
  }

  const createMutation = useMutation({
    mutation: (payload: CreateAgentPayload) => createAgent(payload),
  })

  const attachMutation = useMutation({
    mutation: (payload: SetAgentRolePayload) => setAgentRole(organismeUuid, payload),
    onSettled: () => queryCache.invalidateQueries({ key: ORGANISMES_QUERY_KEYS.root }),
  })

  async function create(): Promise<Agent> {
    const agent = await createMutation.mutateAsync({
      email: searchedEmail.value,
      organisme_id: organismeUuid,
    })
    foundAgent.value = agent
    status.value = 'found'
    return agent
  }

  async function add(role: Role) {
    const agent = status.value === 'not-found' ? await create() : foundAgent.value
    if (!agent)
      throw new Error('Aucun agent à ajouter.')
    return attachMutation.mutateAsync({ agent_id: agent.agent_id, role })
  }

  const submitting = computed(
    () => createMutation.isLoading.value || attachMutation.isLoading.value,
  )

  return {
    status,
    foundAgent,
    searching,
    search,
    add,
    submitting,
    reset,
  }
}
