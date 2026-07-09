import type {
  PaginatedCandidatureListeResponse,
  PaginatedRecrutementsActifsResponse,
  PaginatedRecrutementsArchivesResponse,
  RecrutementDetail,
} from './types'
import { api } from '@/api/client'

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

export async function getRecrutementDetail(params: {
  organismeUuid: string
  recrutementUuid: string
}): Promise<RecrutementDetail> {
  const { data } = await api.GET('/recruteur/organisme/{organisme_uuid}/recrutements/{recrutement_uuid}/kanban', {
    params: { path: { organisme_uuid: params.organismeUuid, recrutement_uuid: params.recrutementUuid } },
  })
  return data!
}

export async function getCandidatureListe(params: {
  organismeUuid: string
  recrutementUuid: string
}): Promise<PaginatedCandidatureListeResponse> {
  const { data } = await api.GET('/recruteur/organisme/{organisme_uuid}/recrutements/{recrutement_uuid}/liste', {
    params: { path: { organisme_uuid: params.organismeUuid, recrutement_uuid: params.recrutementUuid } },
  })
  return data!
}
