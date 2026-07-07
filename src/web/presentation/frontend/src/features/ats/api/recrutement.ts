import type { components } from '@/types/api'
import { api } from '@/utils/api'

export type EtapeRecrutement = components['schemas']['EtapeRecrutement']
export type UpdateEtapeRecrutement = components['schemas']['UpdateEtapeRecrutement']

export type PaginatedRecrutementsActifsResponse = components['schemas']['PaginatedRecrutementsActifsResponse']
export type PaginatedRecrutementsArchivesResponse = components['schemas']['PaginatedRecrutementsArchivesResponse']
export type PaginatedRecrutements = PaginatedRecrutementsActifsResponse | PaginatedRecrutementsArchivesResponse

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

export async function getRecrutementsActifs(organismeUuid: string): Promise<PaginatedRecrutementsActifsResponse> {
  const { data } = await api.GET('/recruteur/organisme/{organisme_uuid}/recrutements-actifs', {
    params: { path: { organisme_uuid: organismeUuid } },
  })
  return data!
}

export async function getRecrutementsArchives(organismeUuid: string): Promise<PaginatedRecrutementsArchivesResponse> {
  const { data } = await api.GET('/recruteur/organisme/{organisme_uuid}/recrutements-archives', {
    params: { path: { organisme_uuid: organismeUuid } },
  })
  return data!
}
