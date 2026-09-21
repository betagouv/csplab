import type { MaybeRefOrGetter } from 'vue'
import type { AssignationResponsablePayload, AssignationResponsableResultat } from '../types'
import { useMutation, useQueryCache } from '@pinia/colada'
import { computed, toValue } from 'vue'
import { useAgentParEmail } from '@/features/organismes/composables/useAgentParEmail'
import { setRecrutementsResponsable } from '../api'
import { RECRUTEMENTS_QUERY_KEYS } from '../queries'

export function useAssignationResponsable(organismeUuid: MaybeRefOrGetter<string>) {
  const queryCache = useQueryCache()

  const { status, foundAgent, searching, creating, search, resolve, reset }
    = useAgentParEmail(organismeUuid)

  const assignationMutation = useMutation({
    mutation: (payload: AssignationResponsablePayload) =>
      setRecrutementsResponsable(toValue(organismeUuid), payload),
    onSettled: () => queryCache.invalidateQueries({
      key: RECRUTEMENTS_QUERY_KEYS.actifs(toValue(organismeUuid)),
    }),
  })

  async function assign(recrutementIds: string[]): Promise<AssignationResponsableResultat> {
    const agent = await resolve()
    return assignationMutation.mutateAsync({
      recrutement_ids: recrutementIds,
      agent_id: agent.agent_id,
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
