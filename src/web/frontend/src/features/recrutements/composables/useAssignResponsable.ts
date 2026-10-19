import type { MaybeRefOrGetter } from 'vue'
import { useQueryCache } from '@pinia/colada'
import { toValue } from 'vue'
import { organismeKeys } from '@/api/queryKeys'
import { useFindOrCreateAgent } from '@/features/agents/composables/useFindOrCreateAgent'
import { setRecrutementsResponsable } from '../api'

export function useAssignResponsable(organismeUuid: MaybeRefOrGetter<string>) {
  const queryCache = useQueryCache()

  const { run: assign, ...agentSearch } = useFindOrCreateAgent(organismeUuid, {
    action: (agent, recrutementIds: string[]) =>
      setRecrutementsResponsable(toValue(organismeUuid), {
        recrutement_ids: recrutementIds,
        agent_id: agent.uuid,
      }),
    onSettled: () => Promise.all([
      queryCache.invalidateQueries({ key: organismeKeys.root({ organismeUuid: toValue(organismeUuid) }) }),
      queryCache.invalidateQueries({ key: organismeKeys.list() }),
    ]),
  })

  return { ...agentSearch, assign }
}
