import type { CandidatureParams, ConversationParams } from '@/api/params'
import { defineQueryOptions } from '@pinia/colada'
import { candidatureKeys } from '@/api/queryKeys'
import { getConversationMessages, getConversations } from './api'

export const conversationsQuery = defineQueryOptions((params: CandidatureParams) => {
  return {
    key: candidatureKeys.conversations(params),
    query: () => getConversations(params),
  }
})

export const conversationMessagesQuery = defineQueryOptions((params: ConversationParams) => {
  return {
    key: candidatureKeys.conversation(params),
    query: () => getConversationMessages(params),
  }
})
