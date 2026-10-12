import type { MaybeRefOrGetter } from 'vue'
import type { AgentRecherche, CreateAgentPayload } from '../types'
import { useMutation } from '@pinia/colada'
import { computed, ref, toValue } from 'vue'
import { createAgent, searchAgentByEmail } from '../api'

export type AgentSearchStatus = 'idle' | 'found' | 'not-found'

interface TrouverOuCreerAgentOptions<TVariables, TResult> {
  action: (agent: AgentRecherche, variables: TVariables) => Promise<TResult>
  onSettled: () => unknown
}

export function useTrouverOuCreerAgent<TVariables, TResult>(
  organismeUuid: MaybeRefOrGetter<string>,
  options: TrouverOuCreerAgentOptions<TVariables, TResult>,
) {
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

  const actionMutation = useMutation({
    mutation: ({ agent, variables }: { agent: AgentRecherche, variables: TVariables }) =>
      options.action(agent, variables),
    onSettled: options.onSettled,
  })

  async function run(variables: TVariables): Promise<TResult> {
    const agent = await resolve()
    return actionMutation.mutateAsync({ agent, variables })
  }

  const submitting = computed(() => createMutation.isLoading.value || actionMutation.isLoading.value)

  return {
    status,
    foundAgent,
    searching,
    search,
    run,
    submitting,
    reset,
  }
}
