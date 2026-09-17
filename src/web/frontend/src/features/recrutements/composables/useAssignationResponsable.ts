import type { AssignationResponsablePayload } from '../types'
import { useMutation, useQuery, useQueryCache } from '@pinia/colada'
import { computed } from 'vue'
import { organismeAgentsQuery } from '@/features/organismes/queries'
import { setRecrutementsResponsable } from '../api'
import { RECRUTEMENTS_QUERY_KEYS } from '../queries'

export function useAssignationResponsable(organismeUuid: string) {
  const queryCache = useQueryCache()

  const agentsQuery = useQuery(() => organismeAgentsQuery({ organismeUuid }))

  const assignationMutation = useMutation({
    mutation: (payload: AssignationResponsablePayload) =>
      setRecrutementsResponsable(organismeUuid, payload),
    onSettled: () => queryCache.invalidateQueries({
      key: RECRUTEMENTS_QUERY_KEYS.actifs(organismeUuid),
    }),
  })

  return {
    agents: computed(() => agentsQuery.data.value ?? []),
    pendingAgents: agentsQuery.isPending,
    assigner: assignationMutation.mutateAsync,
    submitting: assignationMutation.isLoading,
  }
}
