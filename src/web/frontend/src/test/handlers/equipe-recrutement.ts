import type { MembreEquipe, MembreEquipePayload } from '@/features/equipe-recrutement/types'
import { EQUIPE, MEMBRE_EQUIPE } from '@/test/fixtures/equipe'
import { failure, http } from './http'

const EQUIPE_PATH = '/recruteur/organismes/{organisme_uuid}/recrutements/{recrutement_uuid}/parametres/agents'

export function equipe(
  membres: MembreEquipe[] = EQUIPE,
  onRequest?: (organismeUuid: string, recrutementUuid: string) => void,
) {
  return http.get(EQUIPE_PATH, ({ params, response }) => {
    onRequest?.(params.organisme_uuid, params.recrutement_uuid)
    return response(200).json({ count: membres.length, results: membres })
  })
}

export function membreAddition(
  membre: MembreEquipe = MEMBRE_EQUIPE,
  onRequest?: (organismeUuid: string, recrutementUuid: string, payload: MembreEquipePayload) => void,
) {
  return http.post(EQUIPE_PATH, async ({ params, request, response }) => {
    onRequest?.(params.organisme_uuid, params.recrutement_uuid, await request.json())
    return response(201).json(membre)
  })
}

export function membreAdditionFailure(status: number) {
  return http.post(EQUIPE_PATH, ({ response }) => response.untyped(failure(status)))
}

export function membreUpdate(
  onRequest?: (organismeUuid: string, recrutementUuid: string, payload: MembreEquipePayload) => void,
) {
  return http.put(EQUIPE_PATH, async ({ params, request, response }) => {
    const payload = await request.json()
    onRequest?.(params.organisme_uuid, params.recrutement_uuid, payload)
    return response(200).json(payload)
  })
}

export function membreUpdateFailure(status: number) {
  return http.put(EQUIPE_PATH, ({ response }) => response.untyped(failure(status)))
}

export const equipeRecrutementHandlers = [
  equipe(),
  membreAddition(),
  membreUpdate(),
]
