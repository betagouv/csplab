import type { MaybeRefOrGetter } from 'vue'
import { useQuery } from '@pinia/colada'
import { computed, toValue } from 'vue'
import { isHttpStatus } from '@/api/errors'
import { organismeDetailQuery } from '../queries'

export function useOrganismeDetail(organismeUuid: MaybeRefOrGetter<string>) {
  const query = useQuery(() => organismeDetailQuery({ organismeUuid: toValue(organismeUuid) }))

  const notFound = computed(() => isHttpStatus(query.error.value, 404))
  const forbidden = computed(() => isHttpStatus(query.error.value, 403))

  return {
    organisme: query.data,
    pending: query.isPending,
    error: query.error,
    notFound,
    forbidden,
  }
}
