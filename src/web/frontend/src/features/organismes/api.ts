import type { AgentOrganisme, AgentRecherche, CreateOrganismePayload, OrganismeDetail, OrganismesList, SetAgentRolePayload, UpdateAgentRolePayload, UpdateOrganismePayload } from './types'
import { api } from '@/api/client'
import { isHttpStatus } from '@/api/errors'

export async function getOrganismesList(): Promise<OrganismesList[]> {
  const { data } = await api.GET('/recruteur/organismes')
  return data!
}

export async function getOrganismeDetail(organismeUuid: string): Promise<OrganismeDetail> {
  const { data } = await api.GET('/recruteur/organismes/{organisme_uuid}', {
    params: { path: { organisme_uuid: organismeUuid } },
  })
  return data!
}

export async function createOrganisme(payload: CreateOrganismePayload): Promise<OrganismeDetail> {
  const { data } = await api.POST('/recruteur/organismes', { body: payload })
  return data!
}

export async function updateOrganisme(
  organismeUuid: string,
  payload: UpdateOrganismePayload,
): Promise<OrganismeDetail> {
  const { data } = await api.PUT('/recruteur/organismes/{organisme_uuid}', {
    params: { path: { organisme_uuid: organismeUuid } },
    body: payload,
  })
  return data!
}

export async function getOrganismeAgents(organismeUuid: string): Promise<AgentOrganisme[]> {
  const { data } = await api.GET('/recruteur/organismes/{organisme_uuid}/parametres/agents', {
    params: { path: { organisme_uuid: organismeUuid } },
  })
  return data!
}

export async function setAgentRole(
  organismeUuid: string,
  payload: SetAgentRolePayload,
): Promise<AgentOrganisme> {
  const { data } = await api.POST('/recruteur/organismes/{organisme_uuid}/parametres/agents', {
    params: { path: { organisme_uuid: organismeUuid } },
    body: payload,
  })
  return data!
}

export async function updateAgentRole(
  organismeUuid: string,
  payload: UpdateAgentRolePayload,
): Promise<AgentOrganisme> {
  const { data } = await api.PUT('/recruteur/organismes/{organisme_uuid}/parametres/agents', {
    params: { path: { organisme_uuid: organismeUuid } },
    body: payload,
  })
  return data!
}

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
    if (isHttpStatus(error, 404))
      return null
    throw error
  }
}
