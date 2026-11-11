import type { EtapeRecrutement, UpdateEtapeRecrutement } from '@/features/etapes-recrutement/types'
import { ETAPES } from '@/test/fixtures/etapes-recrutement'
import { failure, http } from './http'

const ORGANISME_ETAPES_PATH = '/recruteur/organismes/{organisme_uuid}/parametres/etapes'
const ORGANISME_INIT_PATH = '/recruteur/organismes/{organisme_uuid}/parametres/etapes/init'
const OFFRE_ETAPES_PATH = '/recruteur/organismes/{organisme_uuid}/recrutements/{recrutement_uuid}/etapes'
const OFFRE_INIT_PATH = '/recruteur/organismes/{organisme_uuid}/recrutements/{recrutement_uuid}/etapes/init'

export function etapesOrganisme(
  etapes: EtapeRecrutement[] = ETAPES,
  onRequest?: (organismeUuid: string) => void,
) {
  return http.get(ORGANISME_ETAPES_PATH, ({ params, response }) => {
    onRequest?.(params.organisme_uuid)
    return response(200).json(etapes)
  })
}

export function etapesOrganismeUpdate(
  etapes: EtapeRecrutement[] = ETAPES,
  onRequest?: (organismeUuid: string, payload: UpdateEtapeRecrutement[]) => void,
) {
  return http.put(ORGANISME_ETAPES_PATH, async ({ params, request, response }) => {
    onRequest?.(params.organisme_uuid, await request.json())
    return response(200).json(etapes)
  })
}

export function etapesOrganismeUpdateFailure(status: number) {
  return http.put(ORGANISME_ETAPES_PATH, ({ response }) => response.untyped(failure(status)))
}

export function etapesOrganismeInit(
  etapes: EtapeRecrutement[] = ETAPES,
  onRequest?: (organismeUuid: string) => void,
) {
  return http.post(ORGANISME_INIT_PATH, ({ params, response }) => {
    onRequest?.(params.organisme_uuid)
    return response(201).json(etapes)
  })
}

export function etapesOffre(
  etapes: EtapeRecrutement[] = ETAPES,
  onRequest?: (organismeUuid: string, recrutementUuid: string) => void,
) {
  return http.get(OFFRE_ETAPES_PATH, ({ params, response }) => {
    onRequest?.(params.organisme_uuid, params.recrutement_uuid)
    return response(200).json(etapes)
  })
}

export function etapesOffreUpdate(
  etapes: EtapeRecrutement[] = ETAPES,
  onRequest?: (organismeUuid: string, recrutementUuid: string, payload: UpdateEtapeRecrutement[]) => void,
) {
  return http.patch(OFFRE_ETAPES_PATH, async ({ params, request, response }) => {
    onRequest?.(params.organisme_uuid, params.recrutement_uuid, await request.json())
    return response(200).json(etapes)
  })
}

export function etapesOffreInit(
  etapes: EtapeRecrutement[] = ETAPES,
  onRequest?: (organismeUuid: string, recrutementUuid: string) => void,
) {
  return http.post(OFFRE_INIT_PATH, ({ params, response }) => {
    onRequest?.(params.organisme_uuid, params.recrutement_uuid)
    return response(201).json(etapes)
  })
}

export const etapesRecrutementHandlers = [
  etapesOrganisme(),
  etapesOrganismeUpdate(),
  etapesOrganismeInit(),
  etapesOffre(),
  etapesOffreUpdate(),
  etapesOffreInit(),
]
