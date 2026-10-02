import type { Conversation, ConversationMessage, CreateConversationPayload, CreateMessagePayload, PaginatedConversationList, PaginatedConversationMessageList } from './types'
import type { CandidatureParams } from '@/features/candidatures/types'
import { api } from '@/api/client'
import { toMultipartFormData } from './multipart'

export const CONVERSATIONS_LIMIT = 100
export const MESSAGES_LIMIT = 100

export async function getConversations(
  { organismeUuid, recrutementUuid, candidatureUuid }: CandidatureParams,
): Promise<PaginatedConversationList> {
  const { data } = await api.GET(
    '/recruteur/organismes/{organisme_uuid}/recrutements/{recrutement_uuid}/candidatures/{candidature_uuid}/conversations',
    {
      params: {
        path: {
          organisme_uuid: organismeUuid,
          recrutement_uuid: recrutementUuid,
          candidature_uuid: candidatureUuid,
        },
        query: { limit: CONVERSATIONS_LIMIT },
      },
    },
  )
  return data!
}

export async function getConversationMessages(
  { organismeUuid, recrutementUuid, candidatureUuid }: CandidatureParams,
  conversationUuid: string,
): Promise<PaginatedConversationMessageList> {
  const { data } = await api.GET(
    '/recruteur/organismes/{organisme_uuid}/recrutements/{recrutement_uuid}/candidatures/{candidature_uuid}/conversations/{conversation_uuid}',
    {
      params: {
        path: {
          organisme_uuid: organismeUuid,
          recrutement_uuid: recrutementUuid,
          candidature_uuid: candidatureUuid,
          conversation_uuid: conversationUuid,
        },
        query: { limit: MESSAGES_LIMIT },
      },
    },
  )
  return data!
}

export async function replyToConversation(
  { organismeUuid, recrutementUuid, candidatureUuid }: CandidatureParams,
  conversationUuid: string,
  payload: CreateMessagePayload,
): Promise<ConversationMessage> {
  const { data } = await api.POST(
    '/recruteur/organismes/{organisme_uuid}/recrutements/{recrutement_uuid}/candidatures/{candidature_uuid}/conversations/{conversation_uuid}',
    {
      params: {
        path: {
          organisme_uuid: organismeUuid,
          recrutement_uuid: recrutementUuid,
          candidature_uuid: candidatureUuid,
          conversation_uuid: conversationUuid,
        },
      },
      body: toMultipartFormData(payload) as never,
    },
  )
  return data!
}

export async function createConversation(
  { organismeUuid, recrutementUuid, candidatureUuid }: CandidatureParams,
  payload: CreateConversationPayload,
): Promise<Conversation> {
  const { data } = await api.POST(
    '/recruteur/organismes/{organisme_uuid}/recrutements/{recrutement_uuid}/candidatures/{candidature_uuid}/conversations',
    {
      params: {
        path: {
          organisme_uuid: organismeUuid,
          recrutement_uuid: recrutementUuid,
          candidature_uuid: candidatureUuid,
        },
      },
      body: toMultipartFormData(payload) as never,
    },
  )
  return data!
}
