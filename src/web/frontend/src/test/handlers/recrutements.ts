import type { AssignationResponsablePayload, AssignationResponsableResultat, RecrutementDetail, RecrutementsActifs, RecrutementsArchives } from '@/features/recrutements/types'
import { delay } from 'msw'
import { RECRUTEMENT_DETAIL } from '@/test/fixtures/candidatures'
import { RECRUTEMENTS_ACTIFS, RECRUTEMENTS_ARCHIVES } from '@/test/fixtures/recrutements'
import { failure, http } from './http'

const ACTIFS = '/recruteur/organismes/{organisme_uuid}/recrutements/actifs'
const ARCHIVES = '/recruteur/organismes/{organisme_uuid}/recrutements/archives'
const DETAIL = '/recruteur/organismes/{organisme_uuid}/recrutements/{recrutement_uuid}'
const RESPONSABLE = '/recruteur/organismes/{organisme_uuid}/recrutements/responsable'

const LIST_SEGMENTS = ['actifs', 'archives']

function detail(resolve: Parameters<typeof http.get<typeof DETAIL>>[1]) {
  return http.get(DETAIL, (info) => {
    if (LIST_SEGMENTS.includes(info.params.recrutement_uuid)) {
      return undefined
    }
    return resolve(info)
  })
}

export function recrutementsActifs(results: RecrutementsActifs[] = RECRUTEMENTS_ACTIFS) {
  return http.get(ACTIFS, ({ response }) => response(200).json({ count: results.length, results }))
}

export function recrutementsActifsFailure(status = 500) {
  return http.get(ACTIFS, ({ response }) => response.untyped(failure(status)))
}

export function recrutementsActifsPending() {
  return http.get(ACTIFS, () => delay('infinite'))
}

export function recrutementsArchives(
  results: RecrutementsArchives[] = RECRUTEMENTS_ARCHIVES,
  onRequest?: (organismeUuid: string) => void,
) {
  return http.get(ARCHIVES, ({ params, response }) => {
    onRequest?.(params.organisme_uuid)
    return response(200).json({ count: results.length, results })
  })
}

export function recrutementDetail(recrutement: RecrutementDetail = RECRUTEMENT_DETAIL) {
  return detail(({ response }) => response(200).json(recrutement))
}

export function recrutementDetailPending() {
  return detail(() => delay('infinite'))
}

export function responsableAssignment(
  resultat: AssignationResponsableResultat = { reussites: [], echecs: [] },
  onRequest?: (organismeUuid: string, payload: AssignationResponsablePayload) => void,
) {
  return http.put(RESPONSABLE, async ({ params, request, response }) => {
    onRequest?.(params.organisme_uuid, await request.json())
    return response(200).json(resultat)
  })
}

export const recrutementsHandlers = [
  recrutementsActifs(),
  recrutementsArchives(),
  recrutementDetail(),
  responsableAssignment(),
]
