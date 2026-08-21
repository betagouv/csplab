import type { AgentOrganisme, CreateOrganismePayload, ModifierAgentPayload, OrganismeDetail, OrganismesList, RattacherAgentPayload, UpdateOrganismePayload } from './types'
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

export async function rattacherAgent(
  organismeUuid: string,
  payload: RattacherAgentPayload,
): Promise<AgentOrganisme> {
  const { data } = await api.POST('/recruteur/organismes/{organisme_uuid}/parametres/agents', {
    params: { path: { organisme_uuid: organismeUuid } },
    body: payload,
  })
  return data!
}

export async function updateOrganismeAgent(
  organismeUuid: string,
  payload: ModifierAgentPayload,
): Promise<AgentOrganisme> {
  const { data } = await api.PATCH('/recruteur/organismes/{organisme_uuid}/parametres/agents', {
    params: { path: { organisme_uuid: organismeUuid } },
    body: payload,
  })
  return data!
}
