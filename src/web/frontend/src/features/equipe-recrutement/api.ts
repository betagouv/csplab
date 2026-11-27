import type { MembreEquipe, MembreEquipePayload } from './types'
import type { MembreTagParams, RecrutementParams } from '@/api/params'
import { api } from '@/api/client'

export async function getEquipeRecrutement({ organismeUuid, recrutementUuid }: RecrutementParams): Promise<MembreEquipe[]> {
  const { data } = await api.GET(
    '/recruteur/organismes/{organisme_uuid}/recrutements/{recrutement_uuid}/parametres/agents',
    {
      params: {
        path: {
          organisme_uuid: organismeUuid,
          recrutement_uuid: recrutementUuid,
        },
      },
    },
  )
  return data!.results
}

export async function addMembreEquipe(
  { organismeUuid, recrutementUuid }: RecrutementParams,
  payload: MembreEquipePayload,
): Promise<MembreEquipe> {
  const { data } = await api.POST(
    '/recruteur/organismes/{organisme_uuid}/recrutements/{recrutement_uuid}/parametres/agents',
    {
      params: {
        path: {
          organisme_uuid: organismeUuid,
          recrutement_uuid: recrutementUuid,
        },
      },
      body: payload,
    },
  )
  return data!
}

export async function updateMembreEquipe(
  { organismeUuid, recrutementUuid }: RecrutementParams,
  payload: MembreEquipePayload,
): Promise<void> {
  await api.PUT(
    '/recruteur/organismes/{organisme_uuid}/recrutements/{recrutement_uuid}/parametres/agents',
    {
      params: {
        path: {
          organisme_uuid: organismeUuid,
          recrutement_uuid: recrutementUuid,
        },
      },
      body: payload,
    },
  )
}

function membreTagPath({ organismeUuid, recrutementUuid, agentUuid }: MembreTagParams) {
  return { organisme_uuid: organismeUuid, recrutement_uuid: recrutementUuid, agent_uuid: agentUuid }
}

export async function addMembreTag(params: MembreTagParams): Promise<void> {
  await api.POST(
    '/recruteur/organismes/{organisme_uuid}/recrutements/{recrutement_uuid}/agents/{agent_uuid}/tags',
    { params: { path: membreTagPath(params) }, body: { tag_uuid: params.tagUuid } },
  )
}

export async function removeMembreTag(params: MembreTagParams): Promise<void> {
  await api.DELETE(
    '/recruteur/organismes/{organisme_uuid}/recrutements/{recrutement_uuid}/agents/{agent_uuid}/tags/{tag_uuid}',
    { params: { path: { ...membreTagPath(params), tag_uuid: params.tagUuid } } },
  )
}
