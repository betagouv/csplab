import type { MaybeRefOrGetter } from 'vue'
import type { RecrutementRole } from '../types'
import { useQueryCache } from '@pinia/colada'
import { toValue } from 'vue'
import { useFindOrCreateAgent } from '@/features/agents/composables/useFindOrCreateAgent'
import { addMembreEquipe } from '../api'
import { invalidateEquipeRecrutement } from '../queries'

export function useAddAgentToRecrutement(
  organismeUuid: MaybeRefOrGetter<string>,
  recrutementUuid: MaybeRefOrGetter<string>,
) {
  const queryCache = useQueryCache()

  const { run: add, ...agentSearch } = useFindOrCreateAgent(organismeUuid, {
    action: (agent, role: RecrutementRole) =>
      addMembreEquipe(toValue(organismeUuid), toValue(recrutementUuid), {
        agent_id: agent.uuid,
        recrutement_role: role,
      }),
    onSettled: () => invalidateEquipeRecrutement(queryCache, {
      organismeUuid: toValue(organismeUuid),
      recrutementUuid: toValue(recrutementUuid),
    }),
  })

  return { ...agentSearch, add }
}
