import type { UpdateEtapeRecrutement } from '@/features/etapes-recrutement/types'
import type { EtapeFixture } from '@/test/fixtures/etapes-recrutement'
import type { EtapeAction } from '@/utils/authorizedActions'
import { ETAPES } from '@/test/fixtures/etapes-recrutement'
import { failure, http } from './http'

const ORGANISME_ETAPES_PATH = '/recruteur/organismes/{organisme_uuid}/parametres/etapes'
const ORGANISME_INIT_PATH = '/recruteur/organismes/{organisme_uuid}/parametres/etapes/init'
const OFFRE_ETAPES_PATH = '/recruteur/organismes/{organisme_uuid}/recrutements/{recrutement_uuid}/etapes'
const OFFRE_INIT_PATH = '/recruteur/organismes/{organisme_uuid}/recrutements/{recrutement_uuid}/etapes/init'

type EtapeServie = EtapeFixture & { etape_actions?: EtapeAction[] }

const ETAPE_ACTIONS_PAR_CATEGORIE: Record<EtapeFixture['categorie'], EtapeAction[]> = {
  ENTREE: ['rename_etape', 'insert_etape_after'],
  EN_COURS: ['rename_etape', 'move_etape', 'delete_etape', 'insert_etape_before', 'insert_etape_after'],
  REFUS: ['rename_etape', 'insert_etape_before'],
  ACCEPTE: ['rename_etape'],
}

function withActions(etapes: EtapeServie[]) {
  return etapes.map(etape => ({
    ...etape,
    motif_refus_required: etape.categorie === 'REFUS',
    etape_actions: etape.etape_actions ?? ETAPE_ACTIONS_PAR_CATEGORIE[etape.categorie],
  }))
}

export function etapesOrganisme(
  etapes: EtapeServie[] = ETAPES,
  onRequest?: (organismeUuid: string) => void,
) {
  return http.get(ORGANISME_ETAPES_PATH, ({ params, response }) => {
    onRequest?.(params.organisme_uuid)
    return response(200).json(withActions(etapes))
  })
}

export function etapesOrganismeUpdate(
  etapes: EtapeServie[] = ETAPES,
  onRequest?: (organismeUuid: string, payload: UpdateEtapeRecrutement[]) => void,
) {
  return http.put(ORGANISME_ETAPES_PATH, async ({ params, request, response }) => {
    onRequest?.(params.organisme_uuid, await request.json())
    return response(200).json(withActions(etapes))
  })
}

export function etapesOrganismeInit(
  etapes: EtapeServie[] = ETAPES,
  onRequest?: (organismeUuid: string) => void,
) {
  return http.post(ORGANISME_INIT_PATH, ({ params, response }) => {
    onRequest?.(params.organisme_uuid)
    return response(201).json(withActions(etapes))
  })
}

export function etapesOffre(
  etapes: EtapeServie[] = ETAPES,
  onRequest?: (organismeUuid: string, recrutementUuid: string) => void,
) {
  return http.get(OFFRE_ETAPES_PATH, ({ params, response }) => {
    onRequest?.(params.organisme_uuid, params.recrutement_uuid)
    return response(200).json(withActions(etapes))
  })
}

export function etapesOffreUpdate(
  etapes: EtapeServie[] = ETAPES,
  onRequest?: (organismeUuid: string, recrutementUuid: string, payload: UpdateEtapeRecrutement[]) => void,
) {
  return http.patch(OFFRE_ETAPES_PATH, async ({ params, request, response }) => {
    onRequest?.(params.organisme_uuid, params.recrutement_uuid, await request.json())
    return response(200).json(withActions(etapes))
  })
}

export function etapesOffreUpdateFailure(status: number, body?: Record<string, unknown>) {
  return http.patch(OFFRE_ETAPES_PATH, ({ response }) => response.untyped(failure(status, body)))
}

export function etapesOffreInit(
  etapes: EtapeServie[] = ETAPES,
  onRequest?: (organismeUuid: string, recrutementUuid: string) => void,
) {
  return http.post(OFFRE_INIT_PATH, ({ params, response }) => {
    onRequest?.(params.organisme_uuid, params.recrutement_uuid)
    return response(201).json(withActions(etapes))
  })
}

export function etapesOffreInitFailure(status: number) {
  return http.post(OFFRE_INIT_PATH, ({ response }) => response.untyped(failure(status)))
}

export const etapesRecrutementHandlers = [
  etapesOrganisme(),
  etapesOrganismeUpdate(),
  etapesOrganismeInit(),
  etapesOffre(),
  etapesOffreUpdate(),
  etapesOffreInit(),
]
