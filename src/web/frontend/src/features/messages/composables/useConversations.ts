import type { MaybeRefOrGetter } from 'vue'
import type { ConversationsQueryParams } from '../queries'
import { useQuery } from '@pinia/colada'
import { computed, toValue } from 'vue'
import { conversationsQuery } from '../queries'

export function useConversations(params: MaybeRefOrGetter<ConversationsQueryParams>) {
  const query = useQuery(() => conversationsQuery(toValue(params)))

  const conversations = computed(() => query.data.value?.results ?? [])
  const count = computed(() => query.data.value?.count ?? 0)

  return {
    conversations,
    count,
    pending: query.isPending,
    error: query.error,
  }
}
