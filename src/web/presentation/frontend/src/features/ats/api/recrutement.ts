import type { components } from '@/types/api'
import { api } from '@/utils/api'

export type EtapeRecrutement = components['schemas']['EtapeRecrutement']

export async function getEtapesRecrutement(organismeUuid: string): Promise<EtapeRecrutement[]> {
  const { data } = await api.GET('/recruteur/organisme/{organisme_uuid}/parametres/etapes', {
    params: { path: { organisme_uuid: organismeUuid } },
  })
  return data!
}
