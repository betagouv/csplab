import type { ChangerEtapeResultat, PaginatedCandidatureListeList, RecrutementDetailKanban } from './types'
import { api } from '@/api/client'

export async function getRecrutementKanban(
  organismeUuid: string,
  recrutementUuid: string,
): Promise<RecrutementDetailKanban> {
  const { data } = await api.GET(
    '/recruteur/organisme/{organisme_uuid}/recrutements/{recrutement_uuid}/kanban',
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

export async function getCandidatureListe(
  organismeUuid: string,
  recrutementUuid: string,
): Promise<PaginatedCandidatureListeList> {
  const { data } = await api.GET(
    '/recruteur/organisme/{organisme_uuid}/recrutements/{recrutement_uuid}/liste',
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

export async function patchEtapeCandidatures(
  organismeUuid: string,
  recrutementUuid: string,
  etapeCibleUuid: string,
  candidatureUuids: string[],
): Promise<ChangerEtapeResultat> {
  const { data } = await api.PATCH(
    '/recruteur/organisme/{organisme_uuid}/recrutements/{recrutement_uuid}/candidatures/etape',
    {
      params: {
        path: {
          organisme_uuid: organismeUuid,
          recrutement_uuid: recrutementUuid,
        },
      },
      body: {
        etape_cible_uuid: etapeCibleUuid,
        candidatures: candidatureUuids.map(uuid => ({ candidature_uuid: uuid })),
      },
    },
  )
  return data!
}
