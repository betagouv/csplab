import type { MaybeRefOrGetter } from 'vue'
import type { CandidatureParams } from '@/features/candidatures/types'
import { useQuery } from '@pinia/colada'
import { computed, toValue } from 'vue'
import { conversationsQuery } from '../queries'

export function useConversations(candidature: MaybeRefOrGetter<CandidatureParams>) {
  const query = useQuery(() => conversationsQuery(toValue(candidature)))

  const conversations = computed(() => query.data.value?.results ?? [])
  const count = computed(() => query.data.value?.count ?? 0)

  return {
    conversations,
    count,
    pending: query.isPending,
    error: query.error,
  }
}
