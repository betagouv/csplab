import type { RouteRecordRaw } from 'vue-router'

export const candidaturesRoutes: RouteRecordRaw[] = [
  {
    path: '/mes-recrutements/:recrutementUuid',
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
