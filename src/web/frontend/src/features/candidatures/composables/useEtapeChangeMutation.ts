import type { MaybeRefOrGetter } from 'vue'
import type { EtapeChange } from '../api'
import type { CandidaturesQueryParams } from '../queries'
import { useMutation, useQueryCache } from '@pinia/colada'
import { toValue } from 'vue'
import { useToast } from '@/composables/ui/useToast'
import { patchEtapeCandidatures } from '../api'
import { CANDIDATURES_QUERY_KEYS, recrutementKanbanQuery } from '../queries'
import { moveCandidaturesInKanban } from '../utils/kanban'

export function useEtapeChangeMutation(recrutement: MaybeRefOrGetter<CandidaturesQueryParams>) {
  const queryCache = useQueryCache()
  const { addToast } = useToast()

  const mutation = useMutation({
    mutation: (change: EtapeChange, { params }) =>
      patchEtapeCandidatures(params.organismeUuid, params.recrutementUuid, change),
    onMutate: ({ candidatureUuids, etapeCibleUuid }: EtapeChange) => {
      const params = { ...toValue(recrutement) }
      const key = recrutementKanbanQuery(params).key
      const previous = queryCache.getQueryData(key)
      const optimistic = previous && moveCandidaturesInKanban(previous, candidatureUuids, etapeCibleUuid)
      if (optimistic) {
        queryCache.cancelQueries({ key })
        queryCache.setQueryData(key, optimistic)
      }
      return { params, key, previous, optimistic }
    },
    onSuccess: ({ echecs }, _change, { key, optimistic }) => {
      if (queryCache.getQueryData(key) !== optimistic || echecs.length > 0) {
        void queryCache.invalidateQueries({ key })
      }
      if (echecs.length === 0) {
        return
      }
      addToast({
        variant: 'warning',
        title: 'Certaines candidatures n\'ont pas changé d\'étape',
      })
    },
    onError: (_error, _change, { key, previous, optimistic }) => {
      if (key && previous) {
        if (queryCache.getQueryData(key) === optimistic) {
          queryCache.setQueryData(key, previous)
        }
        else {
          void queryCache.invalidateQueries({ key })
        }
      }
      addToast({
        variant: 'error',
        title: 'Le changement d\'étape a échoué',
        description: 'Vos candidatures sont restées à leur étape actuelle.',
      })
    },
    onSettled: (_data, _error, { candidatureUuids }, { params }) => {
      if (!params) {
        return
      }
      void queryCache.invalidateQueries({ key: CANDIDATURES_QUERY_KEYS.liste(params.organismeUuid, params.recrutementUuid) })
      for (const candidatureUuid of candidatureUuids) {
        void queryCache.invalidateQueries({ key: CANDIDATURES_QUERY_KEYS.candidature({ ...params, candidatureUuid }) })
      }
    },
  })

  async function changeEtape(change: EtapeChange): Promise<boolean> {
    try {
      const { echecs } = await mutation.mutateAsync(change)
      return echecs.length === 0
    }
    catch {
      return false
    }
  }

  return { changeEtape }
}
