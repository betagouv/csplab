import type { EtapeRecrutement, UpdateEtapeRecrutement } from './types'
import { api } from '@/api/client'

export async function getEtapesRecrutement(organismeUuid: string): Promise<EtapeRecrutement[]> {
  const { data } = await api.GET('/recruteur/organisme/{organisme_uuid}/parametres/etapes', {
    params: { path: { organisme_uuid: organismeUuid } },
  })
  return data!
}

export async function updateEtapesRecrutement(
  organismeUuid: string,
  etapes: UpdateEtapeRecrutement[],
): Promise<EtapeRecrutement[]> {
  const { data } = await api.PUT('/recruteur/organisme/{organisme_uuid}/parametres/etapes', {
    params: { path: { organisme_uuid: organismeUuid } },
    body: etapes,
  })
  return data!
}

export async function initEtapesRecrutement(organismeUuid: string): Promise<EtapeRecrutement[]> {
  const { data } = await api.POST('/recruteur/organisme/{organisme_uuid}/parametres/etapes/init', {
    params: { path: { organisme_uuid: organismeUuid } },
  })
  return data!
}

export async function getEtapesOffre(
  organismeUuid: string,
  recrutementUuid: string,
): Promise<EtapeRecrutement[]> {
  const { data } = await api.GET(
    '/recruteur/organisme/{organisme_uuid}/recrutements/{recrutement_uuid}/etapes',
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
  organismeUuid: string,
  recrutementUuid: string,
  etapes: UpdateEtapeRecrutement[],
): Promise<EtapeRecrutement[]> {
  const { data } = await api.PATCH(
    '/recruteur/organisme/{organisme_uuid}/recrutements/{recrutement_uuid}/etapes',
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

export async function initEtapesOffre(
  organismeUuid: string,
  recrutementUuid: string,
): Promise<EtapeRecrutement[]> {
  const { data } = await api.POST(
    '/recruteur/organisme/{organisme_uuid}/recrutements/{recrutement_uuid}/etapes/init',
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
