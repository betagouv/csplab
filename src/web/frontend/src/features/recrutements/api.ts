import type {
  AssignationResponsablePayload,
  AssignationResponsableResultat,
  PaginatedRecrutementsActifsResponse,
  PaginatedRecrutementsArchivesResponse,
  RecrutementDetail,
} from './types'
import { api } from '@/api/client'

export async function getRecrutementDetail(
  organismeUuid: string,
  recrutementUuid: string,
): Promise<RecrutementDetail> {
  const { data } = await api.GET(
    '/recruteur/organismes/{organisme_uuid}/recrutements/{recrutement_uuid}',
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

export async function getRecrutementsActifs(organismeUuid: string): Promise<PaginatedRecrutementsActifsResponse> {
  const { data } = await api.GET('/recruteur/organismes/{organisme_uuid}/recrutements-actifs', {
    params: { path: { organisme_uuid: organismeUuid } },
  })
  return data!
}

export async function getRecrutementsArchives(organismeUuid: string): Promise<PaginatedRecrutementsArchivesResponse> {
  const { data } = await api.GET('/recruteur/organismes/{organisme_uuid}/recrutements-archives', {
    params: { path: { organisme_uuid: organismeUuid } },
  })
  return data!
}

export async function setRecrutementsResponsable(
  organismeUuid: string,
  payload: AssignationResponsablePayload,
): Promise<AssignationResponsableResultat> {
  const { data } = await api.PUT('/recruteur/organismes/{organisme_uuid}/recrutements/responsable', {
    params: { path: { organisme_uuid: organismeUuid } },
    body: payload,
  })
  return data!
}
