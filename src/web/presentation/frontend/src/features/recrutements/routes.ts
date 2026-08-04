import type { RouteRecordRaw } from 'vue-router'
import type { RecrutementKey } from './types'

declare module 'vue-router' {
  interface RouteMeta {
    recrutementTab?: RecrutementKey
  }
}

export const RECRUTEMENTS_TAB_ROUTE_NAMES = {
  actifs: 'mes-recrutements',
  archives: 'mes-recrutements-archives',
} as const satisfies Record<RecrutementKey, string>

export const DEFAULT_RECRUTEMENT_TAB: RecrutementKey = 'actifs'

export const recrutementsRoutes: RouteRecordRaw[] = [
  {
    path: '/mes-recrutements',
    name: RECRUTEMENTS_TAB_ROUTE_NAMES.actifs,
    component: () => import('./views/MesRecrutementsView.vue'),
    meta: { recrutementTab: 'actifs' },
  },
  {
    path: '/mes-recrutements/archives',
    name: RECRUTEMENTS_TAB_ROUTE_NAMES.archives,
    component: () => import('./views/MesRecrutementsView.vue'),
    meta: { recrutementTab: 'archives' },
  },
]
