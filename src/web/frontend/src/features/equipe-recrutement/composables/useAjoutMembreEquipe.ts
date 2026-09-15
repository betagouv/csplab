import type { AjoutMembrePayload } from '../types'
import { useMutation, useQuery, useQueryCache } from '@pinia/colada'
import { computed } from 'vue'
import { organismeAgentsQuery } from '@/features/organismes/queries'
import { addMembreEquipe } from '../api'
import { EQUIPE_RECRUTEMENT_QUERY_KEYS, equipeRecrutementQuery } from '../queries'

export function useAjoutMembreEquipe(organismeUuid: string, recrutementUuid: string) {
  const queryCache = useQueryCache()

  const agentsQuery = useQuery(() => organismeAgentsQuery({ organismeUuid }))
  const equipeQuery = useQuery(() => equipeRecrutementQuery({ organismeUuid, recrutementUuid }))

  const agentsDisponibles = computed(() => {
    const membres = new Set((equipeQuery.data.value ?? []).map(membre => membre.agent_id))
    return (agentsQuery.data.value ?? []).filter(agent => !membres.has(agent.agent_id))
  })

  const addMutation = useMutation({
    mutation: (payload: AjoutMembrePayload) =>
      addMembreEquipe(organismeUuid, recrutementUuid, payload),
    onSettled: () => queryCache.invalidateQueries({
      key: EQUIPE_RECRUTEMENT_QUERY_KEYS.byRecrutement(organismeUuid, recrutementUuid),
    }),
  })

  return {
    agentsDisponibles,
    pendingAgents: agentsQuery.isPending,
    errorAgents: agentsQuery.error,
    add: addMutation.mutateAsync,
    submitting: addMutation.isLoading,
  }
}
