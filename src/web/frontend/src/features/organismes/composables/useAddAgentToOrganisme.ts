import type { MaybeRefOrGetter } from 'vue'
import type { Role } from '../types'
import { useQueryCache } from '@pinia/colada'
import { toValue } from 'vue'
import { useFindOrCreateAgent } from '@/features/agents/composables/useFindOrCreateAgent'
import { setAgentRole } from '../api'
import { invalidateOrganisme } from '../queries'

export function useAddAgentToOrganisme(organismeUuid: MaybeRefOrGetter<string>) {
  const queryCache = useQueryCache()

  const { run: add, ...agentSearch } = useFindOrCreateAgent(organismeUuid, {
    action: (agent, role: Role) =>
      setAgentRole(toValue(organismeUuid), { agent_id: agent.uuid, role }),
    onSettled: () => invalidateOrganisme(queryCache, { organismeUuid: toValue(organismeUuid) }),
  })

  return { ...agentSearch, add }
}
