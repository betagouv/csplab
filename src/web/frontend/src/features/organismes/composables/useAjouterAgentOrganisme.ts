import type { MaybeRefOrGetter } from 'vue'
import type { Role } from '../types'
import { useQueryCache } from '@pinia/colada'
import { toValue } from 'vue'
import { useTrouverOuCreerAgent } from '@/features/agents/composables/useTrouverOuCreerAgent'
import { setAgentRole } from '../api'
import { invalidateOrganisme } from '../queries'

export function useAjouterAgentOrganisme(organismeUuid: MaybeRefOrGetter<string>) {
  const queryCache = useQueryCache()

  const { run: add, ...recherche } = useTrouverOuCreerAgent(organismeUuid, {
    action: (agent, role: Role) =>
      setAgentRole(toValue(organismeUuid), { agent_id: agent.uuid, role }),
    onSettled: () => invalidateOrganisme(queryCache, { organismeUuid: toValue(organismeUuid) }),
  })

  return { ...recherche, add }
}
