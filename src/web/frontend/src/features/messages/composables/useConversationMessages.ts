import type { MaybeRefOrGetter } from 'vue'
import type { ConversationMessage, CreateMessagePayload, PaginatedConversationList, PaginatedConversationMessageList } from '../types'
import type { ConversationParams } from '@/api/params'
import { useMutation, useQuery, useQueryCache } from '@pinia/colada'
import { computed, toValue } from 'vue'
import { candidatureKeys, organismeKeys, recrutementKeys } from '@/api/queryKeys'
import { replyToConversation } from '../api'
import { conversationMessagesQuery } from '../queries'

export function useConversationMessages(params: MaybeRefOrGetter<ConversationParams>) {
  const queryCache = useQueryCache()

  function markConversationAsRead(target: ConversationParams) {
    void queryCache.invalidateQueries({ key: recrutementKeys.liste(target) })
    void queryCache.invalidateQueries({ key: recrutementKeys.kanban(target) })
    void queryCache.invalidateQueries({ key: organismeKeys.recrutementsActifs(target) })

    const key = candidatureKeys.conversations(target)
    const list = queryCache.getQueryData<PaginatedConversationList>(key)
    if (!list) {
      return
    }
    queryCache.setQueryData(key, {
      ...list,
      results: list.results.map(conversation =>
        conversation.uuid === target.conversationUuid ? { ...conversation, is_unread: false } : conversation,
      ),
    })
  }

  const query = useQuery(() => {
    const target = toValue(params)
    const options = conversationMessagesQuery(target)
    return {
      ...options,
      query: async (context) => {
        const thread = await options.query(context)
        markConversationAsRead(target)
        return thread
      },
    }
  })

  return {
    messages: computed(() => query.data.value?.results ?? []),
    pending: query.isPending,
    error: query.error,
  }
}

export function useReplyConversation(params: MaybeRefOrGetter<ConversationParams>) {
  const queryCache = useQueryCache()

  function appendToThread(target: ConversationParams, message: ConversationMessage) {
    const key = candidatureKeys.conversation(target)
    const thread = queryCache.getQueryData<PaginatedConversationMessageList>(key)
    if (!thread) {
      return
    }
    queryCache.setQueryData(key, {
      ...thread,
      results: [...thread.results, message],
    })
  }

  function moveConversationToTop(target: ConversationParams, message: ConversationMessage) {
    const key = candidatureKeys.conversations(target)
    const list = queryCache.getQueryData<PaginatedConversationList>(key)
    const conversation = list?.results.find(({ uuid }) => uuid === target.conversationUuid)
    if (!list || !conversation) {
      return
    }
    queryCache.setQueryData(key, {
      ...list,
      results: [
        {
          ...conversation,
          last_message_content: message.content,
          last_message_author: message.author,
          last_message_created_at: message.created_at,
        },
        ...list.results.filter(({ uuid }) => uuid !== target.conversationUuid),
      ],
    })
  }

  const mutation = useMutation({
    mutation: ({ target, payload }: { target: ConversationParams, payload: CreateMessagePayload }) =>
      replyToConversation(target, target.conversationUuid, payload),
    onSuccess: (message, { target }) => {
      appendToThread(target, message)
      moveConversationToTop(target, message)
      void queryCache.invalidateQueries({ key: candidatureKeys.conversations(target) })
    },
  })

  return {
    reply: (payload: CreateMessagePayload) => mutation.mutateAsync({ target: toValue(params), payload }),
    replying: mutation.isLoading,
  }
}
