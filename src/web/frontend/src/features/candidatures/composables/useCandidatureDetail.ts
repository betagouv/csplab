import type { MaybeRefOrGetter } from 'vue'
import type { CandidatureParams } from '../types'
import { useQuery } from '@pinia/colada'
import { computed, toValue } from 'vue'
import { isHttpStatus } from '@/api/errors'
import { candidatureDetailQuery } from '../queries'

export function useCandidatureDetail(candidature: MaybeRefOrGetter<CandidatureParams>) {
  const query = useQuery(() => candidatureDetailQuery(toValue(candidature)))

  const notFound = computed(() => isHttpStatus(query.error.value, 404))

  return {
    candidature: query.data,
    pending: query.isPending,
    error: query.error,
    notFound,
  }
}
