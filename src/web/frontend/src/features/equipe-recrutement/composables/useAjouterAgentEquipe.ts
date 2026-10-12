import type { MaybeRefOrGetter } from 'vue'
import type { RecrutementRole } from '../types'
import { useQueryCache } from '@pinia/colada'
import { toValue } from 'vue'
import { recrutementKeys } from '@/api/queryKeys'
import { useTrouverOuCreerAgent } from '@/features/agents/composables/useTrouverOuCreerAgent'
import { addMembreEquipe } from '../api'

export function useAjouterAgentEquipe(
  organismeUuid: MaybeRefOrGetter<string>,
  recrutementUuid: MaybeRefOrGetter<string>,
) {
  const queryCache = useQueryCache()

  const { run: add, ...recherche } = useTrouverOuCreerAgent(organismeUuid, {
    action: (agent, role: RecrutementRole) =>
      addMembreEquipe(toValue(organismeUuid), toValue(recrutementUuid), {
        agent_id: agent.uuid,
        recrutement_role: role,
      }),
    onSettled: () => queryCache.invalidateQueries({
      key: recrutementKeys.equipe({ organismeUuid: toValue(organismeUuid), recrutementUuid: toValue(recrutementUuid) }),
    }),
  })

  return { ...recherche, add }
}
