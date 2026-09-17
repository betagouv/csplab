import type { MaybeRefOrGetter } from 'vue'
import type { AssignationResponsablePayload, AssignationResponsableResultat } from '../types'
import type { AgentRecherche, CreateAgentPayload } from '@/features/organismes/types'
import { useMutation, useQueryCache } from '@pinia/colada'
import { computed, ref, toValue } from 'vue'
import { createAgent, searchAgentByEmail } from '@/features/organismes/api'
import { setRecrutementsResponsable } from '../api'
import { RECRUTEMENTS_QUERY_KEYS } from '../queries'

export type ResponsableSearchStatus = 'idle' | 'found' | 'not-found'

export function useAssignationResponsable(organismeUuid: MaybeRefOrGetter<string>) {
  const queryCache = useQueryCache()

  const status = ref<ResponsableSearchStatus>('idle')
  const foundAgent = ref<AgentRecherche | null>(null)
  const searchedEmail = ref('')
  const searching = ref(false)

  function reset(): void {
    status.value = 'idle'
    foundAgent.value = null
    searchedEmail.value = ''
  }

  async function search(email: string): Promise<ResponsableSearchStatus> {
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

  const assignationMutation = useMutation({
    mutation: (payload: AssignationResponsablePayload) =>
      setRecrutementsResponsable(toValue(organismeUuid), payload),
    onSettled: () => queryCache.invalidateQueries({
      key: RECRUTEMENTS_QUERY_KEYS.actifs(toValue(organismeUuid)),
    }),
  })

  async function create(): Promise<AgentRecherche> {
    const agent = await createMutation.mutateAsync({
      email: searchedEmail.value,
      organisme_id: toValue(organismeUuid),
    })
    foundAgent.value = agent
    status.value = 'found'
    return agent
  }

  async function assigner(recrutementIds: string[]): Promise<AssignationResponsableResultat> {
    const agent = status.value === 'not-found' ? await create() : foundAgent.value
    if (!agent) {
      throw new Error('Aucun responsable à assigner.')
    }
    return assignationMutation.mutateAsync({
      recrutement_ids: recrutementIds,
      agent_id: agent.agent_id,
    })
  }

  const submitting = computed(
    () => createMutation.isLoading.value || assignationMutation.isLoading.value,
  )

  return {
    status,
    foundAgent,
    searching,
    search,
    assigner,
    submitting,
    reset,
  }
}
