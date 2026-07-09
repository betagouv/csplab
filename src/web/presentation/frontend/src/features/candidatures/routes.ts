import type { RouteRecordRaw } from 'vue-router'

export const candidaturesRoutes: RouteRecordRaw[] = [
  {
    path: '/mes-recrutements/:recrutementUuid/kanban',
    name: 'recrutement-candidatures-kanban',
    component: () => import('./views/CandidaturesKanbanView.vue'),
  },
]
