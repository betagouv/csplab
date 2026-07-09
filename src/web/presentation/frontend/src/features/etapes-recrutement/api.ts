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
