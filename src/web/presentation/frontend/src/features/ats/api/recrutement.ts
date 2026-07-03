import type { components } from '@/types/api'
import { api } from '@/utils/api'

export type EtapeRecrutement = components['schemas']['EtapeRecrutement']
export type UpdateEtapeRecrutement = components['schemas']['UpdateEtapeRecrutement']

export type PaginatedRecrutements = components['schemas']['PaginatedRecrutementsResponse']

export interface RecrutementsQuery {
  filtre?: 'actifs' | 'archives'
  page?: number
  size?: number
}

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

export async function getRecrutements(
  organismeUuid: string,
  query: RecrutementsQuery = {},
): Promise<PaginatedRecrutements> {
  const { data } = await api.GET('/recruteur/organisme/{organisme_uuid}/recrutements', {
    params: { path: { organisme_uuid: organismeUuid }, query },
  })
  return data!
}
