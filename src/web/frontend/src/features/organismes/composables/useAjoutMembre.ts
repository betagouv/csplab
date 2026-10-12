import type { MaybeRefOrGetter } from 'vue'
import type { Role, SetAgentRolePayload } from '../types'
import { useMutation, useQueryCache } from '@pinia/colada'
import { computed, toValue } from 'vue'
import { useTrouverOuCreerAgent } from '@/features/agents/composables/useTrouverOuCreerAgent'
import { setAgentRole } from '../api'
import { invalidateOrganisme } from '../queries'

export function useAjoutMembre(organismeUuid: MaybeRefOrGetter<string>) {
  const queryCache = useQueryCache()

  const { status, foundAgent, searching, creating, search, resolve, reset }
    = useTrouverOuCreerAgent(organismeUuid)

  const attachMutation = useMutation({
    mutation: (payload: SetAgentRolePayload) =>
      setAgentRole(toValue(organismeUuid), payload),
    onSettled: () => invalidateOrganisme(queryCache, { organismeUuid: toValue(organismeUuid) }),
  })

  async function add(role: Role) {
    const agent = await resolve()
    return attachMutation.mutateAsync({ agent_id: agent.uuid, role })
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
