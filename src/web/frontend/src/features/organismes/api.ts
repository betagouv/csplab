import type { AgentOrganisme, CreateOrganismePayload, OrganismeDetail, OrganismeRead, OrganismeRecherche, OrganismesList, SetAgentRolePayload, UpdateAgentRolePayload, UpdateOrganismePayload } from './types'
import type { OrganismeParams } from '@/api/params'
import { api } from '@/api/client'

const MAX_PAGE_SIZE = 1_000

export async function getOrganismesList(): Promise<OrganismesList[]> {
  async function fetchPage(page: number) {
    const { data } = await api.GET('/recruteur/organismes', {
      params: { query: { page, taille: MAX_PAGE_SIZE } },
    })
    return data!
  }

  const firstPage = await fetchPage(1)
  const pageCount = Math.ceil(firstPage.count / MAX_PAGE_SIZE)
  const otherPages = await Promise.all(
    Array.from({ length: pageCount - 1 }, (_, index) => fetchPage(index + 2)),
  )
  return [firstPage, ...otherPages].flatMap(page => page.results)
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
