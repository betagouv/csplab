import { defineQueryOptions } from '@pinia/colada'
import { getConversations } from './api'

export const MESSAGES_QUERY_KEYS = {
  root: ['messages'] as const,
  conversations: (organismeUuid: string, recrutementUuid: string, candidatureUuid: string) =>
    [...MESSAGES_QUERY_KEYS.root, organismeUuid, recrutementUuid, candidatureUuid, 'conversations'] as const,
}

export interface ConversationsQueryParams {
  organismeUuid: string
  recrutementUuid: string
  candidatureUuid: string
}

export const conversationsQuery = defineQueryOptions(
  ({ organismeUuid, recrutementUuid, candidatureUuid }: ConversationsQueryParams) => ({
    key: MESSAGES_QUERY_KEYS.conversations(organismeUuid, recrutementUuid, candidatureUuid),
    query: () => getConversations(organismeUuid, recrutementUuid, candidatureUuid),
  }),
)
