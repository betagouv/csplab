import type { MaybeRefOrGetter } from 'vue'
import type { MembreEquipe, RecrutementRole } from '../types'
import { useMutation, useQuery, useQueryCache } from '@pinia/colada'
import { computed, toValue } from 'vue'
import { updateMembreEquipe } from '../api'
import { equipeRecrutementQuery, invalidateEquipeRecrutement } from '../queries'

export function useEquipeRecrutement(
  organismeUuid: MaybeRefOrGetter<string>,
  recrutementUuid: MaybeRefOrGetter<string>,
) {
  const queryCache = useQueryCache()
  const params = computed(() => ({
    organismeUuid: toValue(organismeUuid),
    recrutementUuid: toValue(recrutementUuid),
  }))
  const query = useQuery(() => equipeRecrutementQuery(params.value))

  function invalidate() {
    return invalidateEquipeRecrutement(queryCache, params.value)
  }

  const revokeMutation = useMutation({
    mutation: (membre: MembreEquipe) => updateMembreEquipe(params.value.organismeUuid, params.value.recrutementUuid, {
      agent_id: membre.uuid,
      recrutement_role: membre.recrutement_role,
      date_revocation_recrutement: new Date().toISOString(),
    }),
    onSettled: invalidate,
  })

  const roleMutation = useMutation({
    mutation: ({ membre, role }: { membre: MembreEquipe, role: RecrutementRole }) =>
      updateMembreEquipe(params.value.organismeUuid, params.value.recrutementUuid, {
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
