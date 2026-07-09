import type { RouteRecordRaw } from 'vue-router'

export const recrutementsRoutes: RouteRecordRaw[] = [
  {
    path: '/mes-recrutements',
    name: 'mes-recrutements',
    component: () => import('./views/MesRecrutementsView.vue'),
  },
  {
    path: '/mes-recrutements/:recrutementUuid',
    name: 'recrutement-candidatures',
    component: () => import('./views/RecrutementCandidaturesView.vue'),
  },
]
