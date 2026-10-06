import type { MaybeRefOrGetter } from 'vue'
import type { RecrutementParams } from '../queries'
import { useQuery, useQueryCache } from '@pinia/colada'
import { computed, toValue } from 'vue'
import { peekRecrutementIntitule, recrutementDetailQuery } from '../queries'

export function useRecrutementDetail(params: MaybeRefOrGetter<RecrutementParams>) {
  const queryCache = useQueryCache()
  const query = useQuery(() => recrutementDetailQuery(toValue(params)))

  const intitule = computed<string | null>(() => {
    if (query.data.value?.intitule) {
      return query.data.value.intitule
    }
    const { organismeUuid, recrutementUuid } = toValue(params)
    return peekRecrutementIntitule(queryCache, organismeUuid, recrutementUuid)
  })

  const etapes = computed(() => query.data.value?.etapes ?? [])

  return {
    recrutementDetail: query.data,
    etapes,
    intitule,
    pending: query.isPending,
    error: query.error,
  }
}
