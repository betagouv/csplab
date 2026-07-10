import type { RouteRecordRaw } from 'vue-router'

export const candidaturesRoutes: RouteRecordRaw[] = [
  {
    path: '/mes-recrutements/:recrutementUuid',
    component: () => import('./views/CandidaturesView.vue'),
    children: [
      {
        path: '',
        name: 'recrutement-candidatures',
        component: () => import('./views/CandidaturesListeView.vue'),
      },
      {
        path: 'kanban',
        name: 'recrutement-candidatures-kanban',
        component: () => import('./views/CandidaturesKanbanView.vue'),
      },
    ],
  },
]
