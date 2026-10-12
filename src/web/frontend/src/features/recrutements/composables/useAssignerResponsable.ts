import type { MaybeRefOrGetter } from 'vue'
import type { AssignationResponsablePayload, AssignationResponsableResultat } from '../types'
import { useMutation, useQueryCache } from '@pinia/colada'
import { computed, toValue } from 'vue'
import { organismeKeys } from '@/api/queryKeys'
import { useTrouverOuCreerAgent } from '@/features/agents/composables/useTrouverOuCreerAgent'
import { setRecrutementsResponsable } from '../api'

export function useAssignerResponsable(organismeUuid: MaybeRefOrGetter<string>) {
  const queryCache = useQueryCache()

  const { status, foundAgent, searching, creating, search, resolve, reset }
    = useTrouverOuCreerAgent(organismeUuid)

  const assignationMutation = useMutation({
    mutation: (payload: AssignationResponsablePayload) =>
      setRecrutementsResponsable(toValue(organismeUuid), payload),
    onSettled: () => Promise.all([
      queryCache.invalidateQueries({ key: organismeKeys.root({ organismeUuid: toValue(organismeUuid) }) }),
      queryCache.invalidateQueries({ key: organismeKeys.list() }),
    ]),
  })

  async function assign(recrutementIds: string[]): Promise<AssignationResponsableResultat> {
    const agent = await resolve()
    return assignationMutation.mutateAsync({
      recrutement_ids: recrutementIds,
      agent_id: agent.uuid,
    })
  }

  const submitting = computed(
    () => creating.value || assignationMutation.isLoading.value,
  )

  return {
    status,
    foundAgent,
    searching,
    search,
    assign,
    submitting,
    reset,
  }
}
