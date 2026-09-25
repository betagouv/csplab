import type { MaybeRefOrGetter } from 'vue'
import type { ConversationMessagesParams } from '../queries'
import { useQuery } from '@pinia/colada'
import { computed, toValue } from 'vue'
import { conversationMessagesQuery } from '../queries'

export function useConversationMessages(params: MaybeRefOrGetter<ConversationMessagesParams>) {
  const query = useQuery(() => conversationMessagesQuery(toValue(params)))

  return {
    messages: computed(() => query.data.value?.results ?? []),
    pending: query.isPending,
    error: query.error,
  }
}
