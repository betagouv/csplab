import type { RouteLocationRaw, RouteRecordRaw } from 'vue-router'
import type { RecrutementKey } from './types'

export const RECRUTEMENTS_TAB_ROUTE_NAMES = {
  actifs: 'mes-recrutements',
  archives: 'mes-recrutements-archives',
} as const satisfies Record<RecrutementKey, string>

export const DEFAULT_RECRUTEMENT_TAB: RecrutementKey = 'actifs'

export function recrutementsListLocation(archive: boolean | undefined): RouteLocationRaw {
  return { name: RECRUTEMENTS_TAB_ROUTE_NAMES[archive ? 'archives' : DEFAULT_RECRUTEMENT_TAB] }
}

export const recrutementsRoutes: RouteRecordRaw[] = [
  {
    path: '/mes-recrutements',
    name: RECRUTEMENTS_TAB_ROUTE_NAMES.actifs,
    component: () => import('./views/MesRecrutementsView.vue'),
    meta: { tab: 'actifs' },
  },
  {
    path: '/mes-recrutements/archives',
    name: RECRUTEMENTS_TAB_ROUTE_NAMES.archives,
    component: () => import('./views/MesRecrutementsView.vue'),
    meta: { tab: 'archives' },
  },
]
