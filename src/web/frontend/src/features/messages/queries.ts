import type { CandidatureParams } from '@/features/candidatures/types'
import { defineQueryOptions } from '@pinia/colada'
import { getConversations } from './api'

export const MESSAGES_QUERY_KEYS = {
  root: ['messages'] as const,
  conversations: ({ organismeUuid, recrutementUuid, candidatureUuid }: CandidatureParams) =>
    [...MESSAGES_QUERY_KEYS.root, organismeUuid, recrutementUuid, candidatureUuid, 'conversations'] as const,
}

export const conversationsQuery = defineQueryOptions(
  (candidature: CandidatureParams) => ({
    key: MESSAGES_QUERY_KEYS.conversations(candidature),
    query: () => getConversations(candidature),
  }),
)
