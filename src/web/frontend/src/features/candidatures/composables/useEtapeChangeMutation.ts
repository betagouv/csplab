import type { EntryKey, EntryKeyTagged } from '@pinia/colada'
import type { MaybeRefOrGetter } from 'vue'
import type { EtapeChange } from '../api'
import type { RecrutementParams } from '@/api/params'
import { useMutation, useQueryCache } from '@pinia/colada'
import { toValue } from 'vue'
import { candidatureKeys, recrutementKeys } from '@/api/queryKeys'
import { useToast } from '@/composables/ui/useToast'
import { recrutementDetailQuery } from '@/features/recrutements/queries'
import { patchEtapeCandidatures } from '../api'
import { candidatureDetailQuery, candidatureListeQuery, recrutementKanbanQuery } from '../queries'
import { moveCandidaturesInKanban } from '../utils/kanban'

interface Snapshot {
  key: EntryKey
  previous: unknown
  optimistic: unknown
}

export function useEtapeChangeMutation(recrutement: MaybeRefOrGetter<RecrutementParams>) {
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

  function applyOptimistic<TData>(key: EntryKeyTagged<TData>, update: (previous: TData) => TData): Snapshot | null {
    const previous = queryCache.getQueryData(key)
    if (!previous) {
      return null
    }
    const optimistic = update(previous)
    queryCache.cancelQueries({ key })
    queryCache.setQueryData(key, optimistic)
    return { key, previous, optimistic }
  }

  const mutation = useMutation({
    mutation: (change: EtapeChange, { params }) =>
      patchEtapeCandidatures(params.organismeUuid, params.recrutementUuid, change),
    onMutate: ({ candidatureUuids, etapeCibleUuid }: EtapeChange) => {
      const params = { ...toValue(recrutement) }
      const kanban = applyOptimistic(recrutementKanbanQuery(params).key, previous =>
        moveCandidaturesInKanban(previous, candidatureUuids, etapeCibleUuid))

      const snapshots: (Snapshot | null)[] = []
      const etapeCible = queryCache.getQueryData(recrutementDetailQuery(params).key)?.etapes.find(etape => etape.uuid === etapeCibleUuid)
      if (etapeCible) {
        const moved = new Set(candidatureUuids)
        snapshots.push(applyOptimistic(candidatureListeQuery(params).key, liste => ({
          ...liste,
          results: liste.results.map(row => moved.has(row.uuid) ? { ...row, etape: etapeCible } : row),
        })))
        for (const candidatureUuid of candidatureUuids) {
          snapshots.push(applyOptimistic(candidatureDetailQuery({ ...params, candidatureUuid }).key, detail => ({
            ...detail,
            etape_actuelle: { uuid: etapeCible.uuid, nom: etapeCible.nom },
          })))
        }
      }

      return { params, kanban, snapshots }
    },
    onSuccess: ({ echecs }, _change, { params, kanban }) => {
      const kanbanChangedMeanwhile = kanban && queryCache.getQueryData(kanban.key) !== kanban.optimistic
      if (kanbanChangedMeanwhile || echecs.length > 0) {
        void queryCache.invalidateQueries({ key: recrutementKanbanQuery(params).key })
      }
      if (echecs.length === 0) {
        return
      }
      addToast({
        variant: 'warning',
        title: 'Certaines candidatures n\'ont pas changé d\'étape',
      })
    },
    onError: (_error, _change, { kanban, snapshots }) => {
      for (const snapshot of [kanban, ...(snapshots ?? [])]) {
        if (snapshot) {
          restore(snapshot)
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
      void queryCache.invalidateQueries({ key: recrutementKeys.liste(params) })
      for (const candidatureUuid of candidatureUuids) {
        void queryCache.invalidateQueries({ key: candidatureKeys.root({ ...params, candidatureUuid }) })
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
