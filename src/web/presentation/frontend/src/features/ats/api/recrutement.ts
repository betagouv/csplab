import type { components, operations } from '@/types/api'
import { http } from '@/utils/http'

export type EtapeRecrutement = components['schemas']['EtapeRecrutement']

type EtapesParams = operations['recruteur_organisme_parametres_etapes_list']['parameters']['path']

export function getEtapesRecrutement(organismeUuid: EtapesParams['organisme_uuid']): Promise<EtapeRecrutement[]> {
  return http.get(`/recruteur/organisme/${organismeUuid}/parametres/etapes/`)
}
