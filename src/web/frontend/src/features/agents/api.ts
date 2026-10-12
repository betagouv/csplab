import type { Agent, AgentRecherche, CreateAgentPayload } from './types'
import { api } from '@/api/client'
import { isHttpStatus } from '@/api/errors'

export async function searchAgentByEmail(
  organismeUuid: string,
  email: string,
): Promise<AgentRecherche | null> {
  try {
    const { data } = await api.GET('/recruteur/organismes/{organisme_uuid}/parametres/agents/recherche', {
      params: {
        path: { organisme_uuid: organismeUuid },
        query: { email },
      },
    })
    return data!
  }
  catch (error) {
    if (isHttpStatus(error, 404)) {
      return null
    }
    throw error
  }
}

export async function createAgent(payload: CreateAgentPayload): Promise<Agent> {
  const { data } = await api.POST('/recruteur/agents', { body: payload })
  return data!
}
