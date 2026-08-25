import type { AgentOrganisme, CreateOrganismePayload, OrganismeDetail, OrganismesList, SetAgentRolePayload, UpdateAgentRolePayload, UpdateOrganismePayload } from './types'
import { api } from '@/api/client'

export async function getOrganismesList(): Promise<OrganismesList[]> {
  const { data } = await api.GET('/recruteur/organismes')
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
