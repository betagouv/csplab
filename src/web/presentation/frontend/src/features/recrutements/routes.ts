import type { RouteRecordRaw } from 'vue-router'

export const recrutementsRoutes: RouteRecordRaw[] = [
  {
    path: '/mes-recrutements',
    name: 'mes-recrutements',
    component: () => import('./views/MesRecrutementsView.vue'),
  },
]
