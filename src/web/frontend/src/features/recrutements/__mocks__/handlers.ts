import type { paths } from '@/types/api'
import { HttpResponse } from 'msw'
import { createOpenApiHttp } from 'openapi-msw'
import { paginated } from '@/api/__mocks__/demo'
import { DEMO_RECRUTEMENT_DETAIL, DEMO_RECRUTEMENTS_ACTIFS } from '@/features/recrutements/__mocks__/demo'

const http = createOpenApiHttp<paths>()

export const recrutementsHandlers = [
  http.get('/recruteur/organismes/{organisme_uuid}/recrutements/actifs', ({ response }) =>
    response(200).json(paginated(DEMO_RECRUTEMENTS_ACTIFS))),
  http.get('/recruteur/organismes/{organisme_uuid}/recrutements/archives', ({ response }) =>
    response(200).json(paginated([]))),
  http.get('/recruteur/organismes/{organisme_uuid}/recrutements/{recrutement_uuid}', ({ response }) =>
    response(200).json(DEMO_RECRUTEMENT_DETAIL)),
  http.put('/recruteur/organismes/{organisme_uuid}/recrutements/responsable', ({ response }) =>
    response(200).json({ reussites: [], echecs: [] })),
]

export const recrutementsActifsFailure = http.get('/recruteur/organismes/{organisme_uuid}/recrutements/actifs', ({ response }) =>
  response.untyped(new HttpResponse(null, { status: 500 })))
