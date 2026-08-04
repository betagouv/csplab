import type { RouteLocationRaw, RouteRecordRaw } from 'vue-router'
import type { RecrutementKey } from './types'

export const RECRUTEMENTS_TAB_ROUTE_NAMES = {
  actifs: 'mes-recrutements',
  archives: 'mes-recrutements-archives',
} as const satisfies Record<RecrutementKey, string>

export const DEFAULT_RECRUTEMENT_TAB: RecrutementKey = 'actifs'

const ORIGIN_TAB_STATE = 'recrutementsTab'

function isRecrutementKey(value: unknown): value is RecrutementKey {
  return typeof value === 'string' && Object.hasOwn(RECRUTEMENTS_TAB_ROUTE_NAMES, value)
}

export function recrutementsOriginState(tab: RecrutementKey) {
  return { [ORIGIN_TAB_STATE]: tab }
}

export function recrutementsListLocation(historyState: unknown): RouteLocationRaw {
  const tab = (historyState as Record<string, unknown> | null | undefined)?.[ORIGIN_TAB_STATE]
  return { name: RECRUTEMENTS_TAB_ROUTE_NAMES[isRecrutementKey(tab) ? tab : DEFAULT_RECRUTEMENT_TAB] }
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
