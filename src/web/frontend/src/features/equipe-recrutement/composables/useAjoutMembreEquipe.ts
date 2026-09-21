import type { MaybeRefOrGetter } from 'vue'
import type { MembreEquipePayload, RecrutementRole } from '../types'
import { useMutation, useQueryCache } from '@pinia/colada'
import { computed, toValue } from 'vue'
import { useAgentParEmail } from '@/features/organismes/composables/useAgentParEmail'
import { addMembreEquipe } from '../api'
import { EQUIPE_RECRUTEMENT_QUERY_KEYS } from '../queries'

export function useAjoutMembreEquipe(
  organismeUuid: MaybeRefOrGetter<string>,
  recrutementUuid: MaybeRefOrGetter<string>,
) {
  const queryCache = useQueryCache()

  const { status, foundAgent, searching, creating, search, resolve, reset }
    = useAgentParEmail(organismeUuid)

  const addMutation = useMutation({
    mutation: (payload: MembreEquipePayload) =>
      addMembreEquipe(toValue(organismeUuid), toValue(recrutementUuid), payload),
    onSettled: () => queryCache.invalidateQueries({
      key: EQUIPE_RECRUTEMENT_QUERY_KEYS.byRecrutement(
        toValue(organismeUuid),
        toValue(recrutementUuid),
      ),
    }),
  })

  async function add(role: RecrutementRole) {
    const agent = await resolve()
    return addMutation.mutateAsync({
      agent_id: agent.agent_id,
      recrutement_role: role,
    })
  }

  const submitting = computed(() => creating.value || addMutation.isLoading.value)

  return {
    status,
    foundAgent,
    searching,
    search,
    add,
    submitting,
    reset,
  }
}
