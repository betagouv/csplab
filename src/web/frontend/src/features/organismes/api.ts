import type { AgentOrganisme, CreateOrganismePayload, OrganismeDetail, OrganismeRead, OrganismeRecherche, OrganismesPageParams, PaginatedOrganismesListList, SetAgentRolePayload, UpdateAgentRolePayload, UpdateOrganismePayload } from './types'
import type { OrganismeParams } from '@/api/params'
import { api } from '@/api/client'
import { ORGANISMES_PAGE_SIZE } from './constants/organisme'

export async function getOrganismesPage({ page, filter }: OrganismesPageParams): Promise<PaginatedOrganismesListList> {
  const { data } = await api.GET('/recruteur/organismes', {
    params: { query: { page, taille: ORGANISMES_PAGE_SIZE, filter } },
  })
  return data!
}

export async function searchOrganismes(nom: string): Promise<OrganismeRecherche[]> {
  const { data } = await api.GET('/recruteur/organismes/recherche', {
    params: { query: { nom } },
  })
  return data!
}

export async function getOrganismeDetail({ organismeUuid }: OrganismeParams): Promise<OrganismeRead> {
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

export async function getOrganismeAgents({ organismeUuid }: OrganismeParams): Promise<AgentOrganisme[]> {
  const { data } = await api.GET('/recruteur/organismes/{organisme_uuid}/parametres/agents', {
    params: { path: { organisme_uuid: organismeUuid } },
  })
  return data!
}

export async function setAgentRole(
  { organismeUuid }: OrganismeParams,
  payload: SetAgentRolePayload,
): Promise<AgentOrganisme> {
  const { data } = await api.POST('/recruteur/organismes/{organisme_uuid}/parametres/agents', {
    params: { path: { organisme_uuid: organismeUuid } },
    body: payload,
  })
  return data!
}

export async function updateAgentRole(
  { organismeUuid }: OrganismeParams,
  payload: UpdateAgentRolePayload,
): Promise<AgentOrganisme> {
  const { data } = await api.PUT('/recruteur/organismes/{organisme_uuid}/parametres/agents', {
    params: { path: { organisme_uuid: organismeUuid } },
    body: payload,
  })
  return data!
}
