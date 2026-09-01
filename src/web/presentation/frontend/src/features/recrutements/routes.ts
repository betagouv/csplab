import type { RouteLocationRaw, RouteRecordRaw } from 'vue-router'
import type { RecrutementKey } from './types'
import { tabMetaFor } from '@/composables/navigation/tabs'
import { RECRUTEMENT_TAB_LABELS } from './constants/recrutement'

export const RECRUTEMENTS_TAB_ROUTE_NAMES = {
  actifs: 'mes-recrutements',
  archives: 'mes-recrutements-archives',
} as const satisfies Record<RecrutementKey, string>

export const DEFAULT_RECRUTEMENT_TAB: RecrutementKey = 'actifs'

const tabMeta = tabMetaFor(RECRUTEMENT_TAB_LABELS)

export function recrutementsListLocation(archive: boolean | undefined): RouteLocationRaw {
  return { name: RECRUTEMENTS_TAB_ROUTE_NAMES[archive ? 'archives' : DEFAULT_RECRUTEMENT_TAB] }
}

export const recrutementsRoutes: RouteRecordRaw[] = [
  {
    path: '/mes-recrutements',
    name: RECRUTEMENTS_TAB_ROUTE_NAMES.actifs,
    component: () => import('./views/MesRecrutementsView.vue'),
    meta: tabMeta('actifs'),
  },
  {
    path: '/mes-recrutements/archives',
    name: RECRUTEMENTS_TAB_ROUTE_NAMES.archives,
    component: () => import('./views/MesRecrutementsView.vue'),
    meta: tabMeta('archives'),
  },
]
