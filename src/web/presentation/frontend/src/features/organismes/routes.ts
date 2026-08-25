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
  {
    path: '/mon-organisme',
    name: 'mon-organisme',
    component: () => import('./views/OrganismeView.vue'),
    meta: { requiresCurrentOrganisme: true },
  },
]
