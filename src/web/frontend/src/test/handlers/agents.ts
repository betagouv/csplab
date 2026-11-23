import type { Agent, AgentRecherche, CreateAgentPayload } from '@/features/agents/types'
import { AGENT_RECHERCHE, CREATED_AGENT } from '@/test/fixtures/agents'
import { failure, http } from './http'

const SEARCH_PATH = '/recruteur/organismes/{organisme_uuid}/parametres/agents/recherche'
const AGENTS_PATH = '/recruteur/agents'

export function agentSearch(
  agent: AgentRecherche = AGENT_RECHERCHE,
  onRequest?: (organismeUuid: string, email: string | null) => void,
) {
  return http.get(SEARCH_PATH, ({ params, query, response }) => {
    onRequest?.(params.organisme_uuid, query.get('email'))
    return response(200).json(agent)
  })
}

export function agentSearchFailure(status: number) {
  return http.get(SEARCH_PATH, ({ response }) => response.untyped(failure(status)))
}

export function agentCreation(
  agent: Agent = CREATED_AGENT,
  onRequest?: (payload: CreateAgentPayload) => void | Promise<void>,
) {
  return http.post(AGENTS_PATH, async ({ request, response }) => {
    await onRequest?.(await request.json())
    return response(201).json(agent)
  })
}

export const agentsHandlers = [
  agentSearch(),
  agentCreation(),
]
