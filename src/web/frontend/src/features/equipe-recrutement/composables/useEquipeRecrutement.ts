import type { MembreEquipe, RecrutementRole } from '../types'
import { useMutation, useQuery, useQueryCache } from '@pinia/colada'
import { computed } from 'vue'
import { addMembreTag, removeMembreTag, updateMembreEquipe } from '../api'
import { equipeRecrutementQuery, invalidateEquipeRecrutement } from '../queries'

export class TagNotReplacedError extends Error {}

export function useEquipeRecrutement(organismeUuid: string, recrutementUuid: string) {
  const queryCache = useQueryCache()
  const params = { organismeUuid, recrutementUuid }
  const query = useQuery(() => equipeRecrutementQuery(params))

  function invalidate() {
    return invalidateEquipeRecrutement(queryCache, params)
  }

  const revokeMutation = useMutation({
    mutation: (membre: MembreEquipe) => updateMembreEquipe(params, {
      agent_id: membre.uuid,
      recrutement_role: membre.recrutement_role,
      date_revocation_recrutement: new Date().toISOString(),
    }),
    onSettled: invalidate,
  })

  const roleMutation = useMutation({
    mutation: ({ membre, role }: { membre: MembreEquipe, role: RecrutementRole }) =>
      updateMembreEquipe(params, {
        agent_id: membre.uuid,
        recrutement_role: role,
      }),
    onSettled: invalidate,
  })

  const tagMutation = useMutation({
    mutation: async ({ membre, tagUuid }: { membre: MembreEquipe, tagUuid: string | null }) => {
      const current = membre.tags[0]?.uuid ?? null
      if (current === tagUuid) {
        return
      }
      if (current) {
        await removeMembreTag({ ...params, agentUuid: membre.uuid, tagUuid: current })
      }
      if (tagUuid) {
        await addMembreTag({ ...params, agentUuid: membre.uuid, tagUuid }).catch((error: unknown) => {
          throw current ? new TagNotReplacedError() : error
        })
      }
    },
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
    changeTag: tagMutation.mutateAsync,
    changingTag: tagMutation.isLoading,
  }
}
