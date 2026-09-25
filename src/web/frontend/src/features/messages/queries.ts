import type { CandidatureParams } from '@/features/candidatures/types'
import { defineQueryOptions } from '@pinia/colada'
import { getConversationMessages, getConversations } from './api'

export const MESSAGES_QUERY_KEYS = {
  root: ['messages'] as const,
  conversations: ({ organismeUuid, recrutementUuid, candidatureUuid }: CandidatureParams) =>
    [...MESSAGES_QUERY_KEYS.root, organismeUuid, recrutementUuid, candidatureUuid, 'conversations'] as const,
  conversation: (candidature: CandidatureParams, conversationUuid: string) =>
    [...MESSAGES_QUERY_KEYS.conversations(candidature), conversationUuid] as const,
}

export const conversationsQuery = defineQueryOptions(
  (candidature: CandidatureParams) => ({
    key: MESSAGES_QUERY_KEYS.conversations(candidature),
    query: () => getConversations(candidature),
  }),
)

export interface ConversationMessagesParams {
  candidature: CandidatureParams
  conversationUuid: string
}

export const conversationMessagesQuery = defineQueryOptions(
  ({ candidature, conversationUuid }: ConversationMessagesParams) => ({
    key: MESSAGES_QUERY_KEYS.conversation(candidature, conversationUuid),
    query: () => getConversationMessages(candidature, conversationUuid),
  }),
)
