import type { MaybeRefOrGetter } from 'vue'
import { useQuery } from '@pinia/colada'
import { computed, toValue } from 'vue'
import { HttpError } from '@/api/errors'
import { organismeDetailQuery } from '../queries'

export function useOrganismeDetail(organismeUuid: MaybeRefOrGetter<string>) {
  const query = useQuery(() => organismeDetailQuery({ organismeUuid: toValue(organismeUuid) }))

  const notFound = computed(
    () => query.error.value instanceof HttpError && query.error.value.status === 404,
  )

  return {
    organisme: query.data,
    pending: query.isPending,
    error: query.error,
    notFound,
  }
}
