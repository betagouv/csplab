import type { MembreEquipe, MembreEquipePayload } from './types'
import { api } from '@/api/client'

export async function getEquipeRecrutement(
  organismeUuid: string,
  recrutementUuid: string,
): Promise<MembreEquipe[]> {
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
  organismeUuid: string,
  recrutementUuid: string,
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
  organismeUuid: string,
  recrutementUuid: string,
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
