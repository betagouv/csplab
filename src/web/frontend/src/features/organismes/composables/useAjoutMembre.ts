import type { MaybeRefOrGetter } from 'vue'
import type { Role, SetAgentRolePayload } from '../types'
import { useMutation, useQueryCache } from '@pinia/colada'
import { computed, toValue } from 'vue'
import { setAgentRole } from '../api'
import { ORGANISMES_QUERY_KEYS } from '../queries'
import { useAgentParEmail } from './useAgentParEmail'

export type { AgentSearchStatus } from './useAgentParEmail'

export function useAjoutMembre(organismeUuid: MaybeRefOrGetter<string>) {
  const queryCache = useQueryCache()

  const { status, foundAgent, searching, creating, search, resolve, reset }
    = useAgentParEmail(organismeUuid)

  const attachMutation = useMutation({
    mutation: (payload: SetAgentRolePayload) =>
      setAgentRole(toValue(organismeUuid), payload),
    onSettled: () => queryCache.invalidateQueries({ key: ORGANISMES_QUERY_KEYS.root }),
  })

  async function add(role: Role) {
    const agent = await resolve()
    return attachMutation.mutateAsync({ agent_id: agent.agent_id, role })
  }

  const submitting = computed(
    () => creating.value || attachMutation.isLoading.value,
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
