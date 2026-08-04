import type { RouteRecordRaw } from 'vue-router'
import { UUID_ROUTE_PARAM } from '@/router/params'

export const etapesRecrutementRoutes: RouteRecordRaw[] = [
  {
    path: `/mes-recrutements/:recrutementUuid${UUID_ROUTE_PARAM}/etapes-recrutement`,
    name: 'recrutement-etapes-recrutement',
    component: () => import('./views/OffreEtapesRecrutementView.vue'),
  },
]
