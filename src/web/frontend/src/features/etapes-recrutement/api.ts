import type { EtapeRecrutement, UpdateEtapeRecrutement } from './types'
import type { OrganismeParams, RecrutementParams } from '@/api/params'
import { api } from '@/api/client'

export async function getEtapesRecrutement({ organismeUuid }: OrganismeParams): Promise<EtapeRecrutement[]> {
  const { data } = await api.GET('/recruteur/organismes/{organisme_uuid}/parametres/etapes', {
    params: { path: { organisme_uuid: organismeUuid } },
  })
  return data!
}

export async function updateEtapesRecrutement(
  { organismeUuid }: OrganismeParams,
  etapes: UpdateEtapeRecrutement[],
): Promise<EtapeRecrutement[]> {
  const { data } = await api.PUT('/recruteur/organismes/{organisme_uuid}/parametres/etapes', {
    params: { path: { organisme_uuid: organismeUuid } },
    body: etapes,
  })
  return data!
}

export async function initEtapesRecrutement({ organismeUuid }: OrganismeParams): Promise<EtapeRecrutement[]> {
  const { data } = await api.POST('/recruteur/organismes/{organisme_uuid}/parametres/etapes/init', {
    params: { path: { organisme_uuid: organismeUuid } },
  })
  return data!
}

export async function getEtapesOffre({ organismeUuid, recrutementUuid }: RecrutementParams): Promise<EtapeRecrutement[]> {
  const { data } = await api.GET(
    '/recruteur/organismes/{organisme_uuid}/recrutements/{recrutement_uuid}/etapes',
    {
      params: {
        path: {
          organisme_uuid: organismeUuid,
          recrutement_uuid: recrutementUuid,
        },
      },
    },
  )
  return data!
}

export async function updateEtapesOffre(
  { organismeUuid, recrutementUuid }: RecrutementParams,
  etapes: UpdateEtapeRecrutement[],
): Promise<EtapeRecrutement[]> {
  const { data } = await api.PATCH(
    '/recruteur/organismes/{organisme_uuid}/recrutements/{recrutement_uuid}/etapes',
    {
      params: {
        path: {
          organisme_uuid: organismeUuid,
          recrutement_uuid: recrutementUuid,
        },
      },
      body: etapes,
    },
  )
  return data!
}

export async function initEtapesOffre({ organismeUuid, recrutementUuid }: RecrutementParams): Promise<EtapeRecrutement[]> {
  const { data } = await api.POST(
    '/recruteur/organismes/{organisme_uuid}/recrutements/{recrutement_uuid}/etapes/init',
    {
      params: {
        path: {
          organisme_uuid: organismeUuid,
          recrutement_uuid: recrutementUuid,
        },
      },
    },
  )
  return data!
}
