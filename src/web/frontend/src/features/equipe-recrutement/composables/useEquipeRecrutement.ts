import type { MembreEquipe } from '../types'
import { useMutation, useQuery, useQueryCache } from '@pinia/colada'
import { computed } from 'vue'
import { revokeMembreEquipe } from '../api'
import { EQUIPE_RECRUTEMENT_QUERY_KEYS, equipeRecrutementQuery } from '../queries'

export function useEquipeRecrutement(organismeUuid: string, recrutementUuid: string) {
  const queryCache = useQueryCache()
  const query = useQuery(() => equipeRecrutementQuery({ organismeUuid, recrutementUuid }))

  const revokeMutation = useMutation({
    mutation: (membre: MembreEquipe) => revokeMembreEquipe(organismeUuid, recrutementUuid, {
      agent_id: membre.agent_id,
      recrutement_role: membre.recrutement_role,
      date_revocation_recrutement: new Date().toISOString(),
    }),
    onSettled: () => queryCache.invalidateQueries({
      key: EQUIPE_RECRUTEMENT_QUERY_KEYS.byRecrutement(organismeUuid, recrutementUuid),
    }),
  })

  return {
    membres: computed(() => query.data.value ?? []),
    pending: query.isPending,
    error: query.error,
    revoke: revokeMutation.mutateAsync,
    revoking: revokeMutation.isLoading,
  }
}
