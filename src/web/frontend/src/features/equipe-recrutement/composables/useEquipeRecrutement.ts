import type { MembreEquipe, RecrutementRole } from '../types'
import { useMutation, useQuery, useQueryCache } from '@pinia/colada'
import { computed } from 'vue'
import { updateMembreEquipe } from '../api'
import { equipeRecrutementQuery, invalidateEquipeRecrutement } from '../queries'

export function useEquipeRecrutement(organismeUuid: string, recrutementUuid: string) {
  const queryCache = useQueryCache()
  const query = useQuery(() => equipeRecrutementQuery({ organismeUuid, recrutementUuid }))

  function invalidate() {
    return invalidateEquipeRecrutement(queryCache, { organismeUuid, recrutementUuid })
  }

  const revokeMutation = useMutation({
    mutation: (membre: MembreEquipe) => updateMembreEquipe(organismeUuid, recrutementUuid, {
      agent_id: membre.uuid,
      recrutement_role: membre.recrutement_role,
      date_revocation_recrutement: new Date().toISOString(),
    }),
    onSettled: invalidate,
  })

  const roleMutation = useMutation({
    mutation: ({ membre, role }: { membre: MembreEquipe, role: RecrutementRole }) =>
      updateMembreEquipe(organismeUuid, recrutementUuid, {
        agent_id: membre.uuid,
        recrutement_role: role,
      }),
    onSettled: invalidate,
  })

  return {
    membres: computed(() => query.data.value ?? []),
    pending: query.isPending,
    error: query.error,
    revoke: revokeMutation.mutateAsync,
    revoking: revokeMutation.isLoading,
    changeRole: roleMutation.mutateAsync,
    changingRole: roleMutation.isLoading,
  }
}
