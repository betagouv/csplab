import type { components } from '@/types/api'

export type Conversation = components['schemas']['Conversation']

export type PaginatedConversationList = components['schemas']['PaginatedConversationList']

export type ConversationMessage = components['schemas']['ConversationMessage']

export type PaginatedConversationMessageList = components['schemas']['PaginatedConversationMessageList']

export type CreateMessagePayload = Omit<components['schemas']['CreateMessage'], 'documents'> & {
  documents?: File[]
}

export type CreateConversationPayload = Omit<components['schemas']['CreateConversation'], 'documents'> & {
  documents?: File[]
}
