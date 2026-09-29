import type { MaybeRefOrGetter } from 'vue'
import type { Activite, CandidatureParams } from '../types'
import { useQuery } from '@pinia/colada'
import { computed, toValue } from 'vue'
import { LATEST_ACTIVITES_LIMIT } from '../constants/candidature'
import { candidatureActivitesQuery } from '../queries'

export function useCandidatureActivites(candidature: MaybeRefOrGetter<CandidatureParams>) {
  const query = useQuery(() => candidatureActivitesQuery({ candidature: toValue(candidature), limit: LATEST_ACTIVITES_LIMIT }))

  return {
    activites: computed<Activite[]>(() => query.data.value?.results ?? []),
    pending: computed(() => query.isPending.value),
    error: computed(() => query.error.value),
  }
}
