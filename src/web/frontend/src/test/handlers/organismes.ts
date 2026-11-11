import type {
  AgentOrganisme,
  CreateOrganismePayload,
  OrganismeDetail,
  OrganismeRead,
  OrganismeRecherche,
  OrganismesList,
  SetAgentRolePayload,
  UpdateAgentRolePayload,
  UpdateOrganismePayload,
} from '@/features/organismes/types'
import { delay } from 'msw'
import { AGENT_ORGANISME, CREATED_ORGANISME, ORGANISME_DETAIL, ORGANISME_RECHERCHE, ORGANISMES } from '@/test/fixtures/organismes'
import { exceptSegments, failure, http } from './http'

const ORGANISMES_PATH = '/recruteur/organismes'
const SEARCH_PATH = '/recruteur/organismes/recherche'
const ORGANISME_PATH = '/recruteur/organismes/{organisme_uuid}'
const AGENTS_PATH = '/recruteur/organismes/{organisme_uuid}/parametres/agents'

const FIXED_SEGMENTS = ['recherche']

function detail(resolve: Parameters<typeof http.get<typeof ORGANISME_PATH>>[1]) {
  return http.get(ORGANISME_PATH, exceptSegments(FIXED_SEGMENTS, 'organisme_uuid', resolve))
}

export function organismes(results: OrganismesList[] = ORGANISMES, onRequest?: () => void) {
  return http.get(ORGANISMES_PATH, ({ response }) => {
    onRequest?.()
    return response(200).json({ count: results.length, results })
  })
}

export function organismeCreation(
  organisme: OrganismeDetail = CREATED_ORGANISME,
  onRequest?: (payload: CreateOrganismePayload) => void,
) {
  return http.post(ORGANISMES_PATH, async ({ request, response }) => {
    onRequest?.(await request.json())
    return response(201).json(organisme)
  })
}

export function organismeCreationFailure(status: number) {
  return http.post(ORGANISMES_PATH, ({ response }) => response.untyped(failure(status)))
}

export function organismeUpdate(
  organisme: OrganismeDetail = ORGANISME_DETAIL,
  onRequest?: (organismeUuid: string, payload: UpdateOrganismePayload) => void,
) {
  return http.put(ORGANISME_PATH, async ({ params, request, response }) => {
    onRequest?.(params.organisme_uuid, await request.json())
    return response(200).json(organisme)
  })
}

export function organismesSearch(
  results: OrganismeRecherche[] = [ORGANISME_RECHERCHE],
  onRequest?: (nom: string | null) => void,
) {
  return http.get(SEARCH_PATH, ({ query, response }) => {
    onRequest?.(query.get('nom'))
    return response(200).json(results)
  })
}

export function organismeDetail(
  organisme: OrganismeRead = ORGANISME_DETAIL,
  onRequest?: (organismeUuid: string) => void,
) {
  return detail(({ params, response }) => {
    onRequest?.(params.organisme_uuid)
    return response(200).json(organisme)
  })
}

export function organismeDetailPending() {
  return detail(() => delay('infinite'))
}

export function organismeDetailFailure(status: number) {
  return detail(({ response }) => response.untyped(failure(status)))
}

export function organismeAgents(
  agents: AgentOrganisme[] = [AGENT_ORGANISME],
  onRequest?: (organismeUuid: string) => void,
) {
  return http.get(AGENTS_PATH, ({ params, response }) => {
    onRequest?.(params.organisme_uuid)
    return response(200).json(agents)
  })
}

export function organismeAgentAddition(
  agent: AgentOrganisme = AGENT_ORGANISME,
  onRequest?: (organismeUuid: string, payload: SetAgentRolePayload) => void | Promise<void>,
) {
  return http.post(AGENTS_PATH, async ({ params, request, response }) => {
    await onRequest?.(params.organisme_uuid, await request.json())
    return response(201).json(agent)
  })
}

export function organismeAgentAdditionFailure(status: number) {
  return http.post(AGENTS_PATH, ({ response }) => response.untyped(failure(status)))
}

export function organismeAgentUpdate(
  agent: AgentOrganisme = AGENT_ORGANISME,
  onRequest?: (organismeUuid: string, payload: UpdateAgentRolePayload) => void,
) {
  return http.put(AGENTS_PATH, async ({ params, request, response }) => {
    onRequest?.(params.organisme_uuid, await request.json())
    return response(200).json(agent)
  })
}

export function organismeAgentUpdateFailure(status: number) {
  return http.put(AGENTS_PATH, ({ response }) => response.untyped(failure(status)))
}

export const organismesHandlers = [
  organismes(),
  organismeCreation(),
  organismeUpdate(),
  organismesSearch(),
  organismeDetail(),
  organismeAgents(),
  organismeAgentAddition(),
  organismeAgentUpdate(),
]
