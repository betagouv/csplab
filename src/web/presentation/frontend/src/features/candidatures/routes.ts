import type { RouteRecordRaw } from 'vue-router'

export const candidaturesRoutes: RouteRecordRaw[] = [
  {
    path: '/mes-recrutements/:recrutementUuid',
    name: 'recrutement-candidatures',
    component: () => import('./views/CandidaturesListeView.vue'),
  },
  {
    path: '/mes-recrutements/:recrutementUuid/kanban',
    name: 'recrutement-candidatures-kanban',
    component: () => import('./views/CandidaturesKanbanView.vue'),
  },
]
