import type { RouteRecordRaw } from 'vue-router'

export const organismesRoutes: RouteRecordRaw[] = [
  {
    path: '/organismes',
    name: 'organismes',
    component: () => import('./views/GestionOrganismesView.vue'),
  },
  {
    path: '/organismes/:organismeUuid',
    name: 'organisme',
    component: () => import('./views/OrganismeView.vue'),
  },
]
