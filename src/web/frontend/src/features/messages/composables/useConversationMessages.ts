import type { MaybeRefOrGetter } from 'vue'
import type { ConversationMessagesParams } from '../queries'
import type { ConversationMessage, CreateMessagePayload, PaginatedConversationList, PaginatedConversationMessageList } from '../types'
import { useMutation, useQuery, useQueryCache } from '@pinia/colada'
import { computed, toValue } from 'vue'
import { replyToConversation } from '../api'
import { conversationMessagesQuery, MESSAGES_QUERY_KEYS } from '../queries'

export function useConversationMessages(params: MaybeRefOrGetter<ConversationMessagesParams>) {
  const query = useQuery(() => conversationMessagesQuery(toValue(params)))

  return {
    messages: computed(() => query.data.value?.results ?? []),
    pending: query.isPending,
    error: query.error,
  }
}

export function useReplyConversation(params: MaybeRefOrGetter<ConversationMessagesParams>) {
  const queryCache = useQueryCache()

  function appendToThread({ candidature, conversationUuid }: ConversationMessagesParams, message: ConversationMessage) {
    const key = MESSAGES_QUERY_KEYS.conversation(candidature, conversationUuid)
    const thread = queryCache.getQueryData<PaginatedConversationMessageList>(key)
    if (!thread)
      return
    queryCache.setQueryData(key, {
      ...thread,
      count: thread.count + 1,
      results: [...thread.results, message],
    })
  }

  function moveConversationToTop({ candidature, conversationUuid }: ConversationMessagesParams, message: ConversationMessage) {
    const key = MESSAGES_QUERY_KEYS.conversations(candidature)
    const list = queryCache.getQueryData<PaginatedConversationList>(key)
    const conversation = list?.results.find(({ uuid }) => uuid === conversationUuid)
    if (!list || !conversation)
      return
    queryCache.setQueryData(key, {
      ...list,
      results: [
        {
          ...conversation,
          last_message_content: message.content,
          last_message_author: message.author,
          last_message_created_at: message.created_at,
        },
        ...list.results.filter(({ uuid }) => uuid !== conversationUuid),
      ],
    })
  }

  const mutation = useMutation({
    mutation: ({ target, payload }: { target: ConversationMessagesParams, payload: CreateMessagePayload }) =>
      replyToConversation(target.candidature, target.conversationUuid, payload),
    onSuccess: (message, { target }) => {
      appendToThread(target, message)
      moveConversationToTop(target, message)
    },
  })

  return {
    reply: (payload: CreateMessagePayload) => mutation.mutateAsync({ target: toValue(params), payload }),
    replying: mutation.isLoading,
  }
}
