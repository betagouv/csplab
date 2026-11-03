import type { AgentOrganisme, CreateOrganismePayload, OrganismeDetail, OrganismeRecherche, OrganismesList, SetAgentRolePayload, UpdateAgentRolePayload, UpdateOrganismePayload } from './types'
import type { OrganismeParams } from '@/api/params'
import { api } from '@/api/client'

export async function getOrganismesList(): Promise<OrganismesList[]> {
  async function fetchPage(taille?: number) {
    const { data } = await api.GET('/recruteur/organismes', {
      params: { query: { taille } },
    })
    return data!
  }

  const firstPage = await fetchPage()
  if (firstPage.results.length >= firstPage.count) {
    return firstPage.results
  }
  return (await fetchPage(firstPage.count)).results
}

export async function searchOrganismes(nom: string): Promise<OrganismeRecherche[]> {
  const { data } = await api.GET('/recruteur/organismes/recherche', {
    params: { query: { nom } },
  })
  return data!
}

export async function getOrganismeDetail({ organismeUuid }: OrganismeParams): Promise<OrganismeDetail> {
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
