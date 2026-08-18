import type { RouteRecordRaw } from 'vue-router'

export const organismesRoutes: RouteRecordRaw[] = [
  {
    path: '/parametres/organismes/:organismeUuid',
    name: 'parametres-organisme',
    component: () => import('./views/OrganismeParametresView.vue'),
  },
]
