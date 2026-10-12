import type { MaybeRefOrGetter } from 'vue'
import type { AgentRecherche, CreateAgentPayload } from '../types'
import { useMutation } from '@pinia/colada'
import { ref, toValue } from 'vue'
import { createAgent, searchAgentByEmail } from '../api'

export type AgentSearchStatus = 'idle' | 'found' | 'not-found'

export function useAgentParEmail(organismeUuid: MaybeRefOrGetter<string>) {
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
      const agent = await searchAgentByEmail(toValue(organismeUuid), email)
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

  async function resolve(): Promise<AgentRecherche> {
    if (status.value === 'not-found') {
      const agent = await createMutation.mutateAsync({
        email: searchedEmail.value,
        organisme_id: toValue(organismeUuid),
      })
      foundAgent.value = agent
      status.value = 'found'
      return agent
    }
    if (!foundAgent.value) {
      throw new Error('Aucun agent n\'a été recherché.')
    }
    return foundAgent.value
  }

  return {
    status,
    foundAgent,
    searching,
    creating: createMutation.isLoading,
    search,
    resolve,
    reset,
  }
}
