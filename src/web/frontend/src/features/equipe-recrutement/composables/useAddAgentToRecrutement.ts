import type { MaybeRefOrGetter } from 'vue'
import type { RecrutementRole } from '../types'
import { useQueryCache } from '@pinia/colada'
import { computed, toValue } from 'vue'
import { useFindOrCreateAgent } from '@/features/agents/composables/useFindOrCreateAgent'
import { addMembreEquipe } from '../api'
import { invalidateEquipeRecrutement } from '../queries'

export function useAddAgentToRecrutement(
  organismeUuid: MaybeRefOrGetter<string>,
  recrutementUuid: MaybeRefOrGetter<string>,
) {
  const queryCache = useQueryCache()
  const params = computed(() => ({
    organismeUuid: toValue(organismeUuid),
    recrutementUuid: toValue(recrutementUuid),
  }))

  const { run: add, ...agentSearch } = useFindOrCreateAgent(organismeUuid, {
    action: (agent, role: RecrutementRole) =>
      addMembreEquipe(params.value, {
        agent_id: agent.uuid,
        recrutement_role: role,
      }),
    onSettled: () => invalidateEquipeRecrutement(queryCache, params.value),
  })

  return { ...agentSearch, add }
}
