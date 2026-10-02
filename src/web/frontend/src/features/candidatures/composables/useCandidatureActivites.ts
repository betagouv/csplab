import type { MaybeRefOrGetter } from 'vue'
import type { Activite, CandidatureParams } from '../types'
import { useQuery } from '@pinia/colada'
import { computed, toValue } from 'vue'
import { candidatureActivitesQuery } from '../queries'

export function useCandidatureActivites(candidature: MaybeRefOrGetter<CandidatureParams>, limit?: number) {
  const query = useQuery(() => candidatureActivitesQuery({ candidature: toValue(candidature), limit }))

  return {
    activites: computed<Activite[]>(() => query.data.value?.results ?? []),
    total: computed(() => query.data.value?.count ?? 0),
    pending: computed(() => query.isPending.value),
    error: computed(() => query.error.value),
  }
}
