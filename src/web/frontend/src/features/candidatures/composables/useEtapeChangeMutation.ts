import type { EntryKey } from '@pinia/colada'
import type { MaybeRefOrGetter } from 'vue'
import type { EtapeChange } from '../api'
import type { CandidaturesQueryParams } from '../queries'
import { useMutation, useQueryCache } from '@pinia/colada'
import { toValue } from 'vue'
import { useToast } from '@/composables/ui/useToast'
import { recrutementDetailQuery } from '@/features/recrutements/queries'
import { patchEtapeCandidatures } from '../api'
import { candidatureDetailQuery, candidatureListeQuery, CANDIDATURES_QUERY_KEYS, recrutementKanbanQuery } from '../queries'
import { moveCandidaturesInKanban } from '../utils/kanban'

interface Snapshot {
  key: EntryKey
  previous: unknown
  optimistic: unknown
}

export function useEtapeChangeMutation(recrutement: MaybeRefOrGetter<CandidaturesQueryParams>) {
  const queryCache = useQueryCache()
  const { addToast } = useToast()

  function restore({ key, previous, optimistic }: Snapshot): void {
    if (queryCache.getQueryData(key) === optimistic) {
      queryCache.setQueryData(key, previous)
    }
    else {
      void queryCache.invalidateQueries({ key })
    }
  }

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

      const snapshots: Snapshot[] = []
      const etapeCible = queryCache.getQueryData(recrutementDetailQuery(params).key)?.etapes.find(etape => etape.uuid === etapeCibleUuid)
      if (etapeCible) {
        const moved = new Set(candidatureUuids)
        const listeKey = candidatureListeQuery(params).key
        const previousListe = queryCache.getQueryData(listeKey)
        if (previousListe) {
          const optimisticListe = {
            ...previousListe,
            results: previousListe.results.map(row => moved.has(row.uuid) ? { ...row, etape: etapeCible } : row),
          }
          queryCache.cancelQueries({ key: listeKey })
          queryCache.setQueryData(listeKey, optimisticListe)
          snapshots.push({ key: listeKey, previous: previousListe, optimistic: optimisticListe })
        }
        for (const candidatureUuid of candidatureUuids) {
          const detailKey = candidatureDetailQuery({ ...params, candidatureUuid }).key
          const previousDetail = queryCache.getQueryData(detailKey)
          if (!previousDetail) {
            continue
          }
          const optimisticDetail = { ...previousDetail, etape_actuelle: { uuid: etapeCible.uuid, nom: etapeCible.nom } }
          queryCache.cancelQueries({ key: detailKey })
          queryCache.setQueryData(detailKey, optimisticDetail)
          snapshots.push({ key: detailKey, previous: previousDetail, optimistic: optimisticDetail })
        }
      }

      return { params, key, previous, optimistic, snapshots }
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
    onError: (_error, _change, { key, previous, optimistic, snapshots }) => {
      if (key && previous) {
        restore({ key, previous, optimistic })
      }
      for (const snapshot of snapshots ?? []) {
        restore(snapshot)
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
