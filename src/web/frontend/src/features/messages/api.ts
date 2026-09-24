import type { PaginatedConversationList } from './types'
import { api } from '@/api/client'

export const CONVERSATIONS_LIMIT = 100

export async function getConversations(
  organismeUuid: string,
  recrutementUuid: string,
  candidatureUuid: string,
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
