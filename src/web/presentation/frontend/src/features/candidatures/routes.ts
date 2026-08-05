import type { RouteRecordRaw } from 'vue-router'
import { UUID_ROUTE_PARAM } from '@/router/params'

export const candidaturesRoutes: RouteRecordRaw[] = [
  {
    path: `/mes-recrutements/:recrutementUuid${UUID_ROUTE_PARAM}`,
    component: () => import('./views/CandidaturesView.vue'),
    children: [
      {
        path: '',
        name: 'recrutement-candidatures-kanban',
        component: () => import('./views/CandidaturesKanbanView.vue'),
      },
      {
        path: 'liste',
        name: 'recrutement-candidatures',
        component: () => import('./views/CandidaturesListeView.vue'),
      },
    ],
  },
]
