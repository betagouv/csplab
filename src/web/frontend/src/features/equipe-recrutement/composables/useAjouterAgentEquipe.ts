import type { MaybeRefOrGetter } from 'vue'
import type { MembreEquipePayload, RecrutementRole } from '../types'
import { useMutation, useQueryCache } from '@pinia/colada'
import { computed, toValue } from 'vue'
import { recrutementKeys } from '@/api/queryKeys'
import { useTrouverOuCreerAgent } from '@/features/agents/composables/useTrouverOuCreerAgent'
import { addMembreEquipe } from '../api'

export function useAjouterAgentEquipe(
  organismeUuid: MaybeRefOrGetter<string>,
  recrutementUuid: MaybeRefOrGetter<string>,
) {
  const queryCache = useQueryCache()

  const { status, foundAgent, searching, creating, search, resolve, reset }
    = useTrouverOuCreerAgent(organismeUuid)

  const addMutation = useMutation({
    mutation: (payload: MembreEquipePayload) =>
      addMembreEquipe(toValue(organismeUuid), toValue(recrutementUuid), payload),
    onSettled: () => queryCache.invalidateQueries({
      key: recrutementKeys.equipe({ organismeUuid: toValue(organismeUuid), recrutementUuid: toValue(recrutementUuid) }),
    }),
  })

  async function add(role: RecrutementRole) {
    const agent = await resolve()
    return addMutation.mutateAsync({
      agent_id: agent.uuid,
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
