import type { RouteRecordRaw } from 'vue-router'
import { ORGANISME_PATH_PREFIX, UUID_ROUTE_PARAM } from '@/router/params'

export const etapesRecrutementRoutes: RouteRecordRaw[] = [
  {
    path: `${ORGANISME_PATH_PREFIX}/recrutements/:recrutementUuid${UUID_ROUTE_PARAM}/etapes-recrutement`,
    name: 'recrutement-etapes-recrutement',
    component: () => import('./views/OffreEtapesRecrutementView.vue'),
  },
]
