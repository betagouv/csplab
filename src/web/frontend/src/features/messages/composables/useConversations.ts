import type { MaybeRefOrGetter } from 'vue'
import type { Conversation, CreateConversationPayload, PaginatedConversationList } from '../types'
import type { CandidatureParams } from '@/api/params'
import { useMutation, useQuery, useQueryCache } from '@pinia/colada'
import { computed, toValue } from 'vue'
import { candidatureKeys } from '@/api/queryKeys'
import { createConversation } from '../api'
import { conversationsQuery } from '../queries'

export function useConversations(candidature: MaybeRefOrGetter<CandidatureParams>) {
  const query = useQuery(() => conversationsQuery(toValue(candidature)))

  const conversations = computed(() => query.data.value?.results ?? [])
  const count = computed(() => query.data.value?.count ?? 0)
  const hasUnread = computed(() => conversations.value.some(conversation => conversation.is_unread))

  return {
    conversations,
    count,
    hasUnread,
    pending: query.isPending,
    error: query.error,
  }
}

export function useCreateConversation(candidature: MaybeRefOrGetter<CandidatureParams>) {
  const queryCache = useQueryCache()

  function prependToList(target: CandidatureParams, conversation: Conversation) {
    const key = candidatureKeys.conversations(target)
    const list = queryCache.getQueryData<PaginatedConversationList>(key)
    if (!list) {
      return
    }
    queryCache.setQueryData(key, {
      ...list,
      count: list.count + 1,
      results: [conversation, ...list.results],
    })
  }

  const mutation = useMutation({
    mutation: ({ target, payload }: { target: CandidatureParams, payload: CreateConversationPayload }) =>
      createConversation(target, payload),
    onSuccess: (conversation, { target }) => {
      prependToList(target, conversation)
      void queryCache.invalidateQueries({ key: candidatureKeys.conversations(target), exact: true })
    },
  })

  return {
    create: (payload: CreateConversationPayload) => mutation.mutateAsync({ target: toValue(candidature), payload }),
    creating: mutation.isLoading,
  }
}
