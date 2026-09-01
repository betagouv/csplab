import type { RouteRecordRaw } from 'vue-router'
import { UUID_ROUTE_PARAM } from '@/router/params'

export const CANDIDATURES_TAB_ROUTE_NAMES = {
  'candidatures': 'recrutement-candidatures-kanban',
  'activites-et-taches': 'recrutement-activites',
} as const

export const candidaturesRoutes: RouteRecordRaw[] = [
  {
    path: `/mes-recrutements/:recrutementUuid${UUID_ROUTE_PARAM}/activites`,
    name: CANDIDATURES_TAB_ROUTE_NAMES['activites-et-taches'],
    component: () => import('./views/CandidaturesView.vue'),
    meta: { tab: 'activites-et-taches' },
  },
  {
    path: `/mes-recrutements/:recrutementUuid${UUID_ROUTE_PARAM}`,
    component: () => import('./views/CandidaturesView.vue'),
    meta: { tab: 'candidatures' },
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
