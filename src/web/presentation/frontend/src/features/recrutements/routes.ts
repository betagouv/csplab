import type { RouteLocationRaw, RouteRecordRaw } from 'vue-router'
import type { RecrutementKey } from './types'
import { tabMetaFor } from '@/composables/navigation/tabs'
import { ORGANISME_PATH_PREFIX } from '@/router/params'
import { RECRUTEMENT_TAB_LABELS } from './constants/recrutement'

export const RECRUTEMENTS_TAB_ROUTE_NAMES = {
  actifs: 'recrutements',
  archives: 'recrutements-archives',
} as const satisfies Record<RecrutementKey, string>

export const DEFAULT_RECRUTEMENT_TAB: RecrutementKey = 'actifs'

const tabMeta = tabMetaFor(RECRUTEMENT_TAB_LABELS)

export function recrutementsListLocation(
  organismeUuid: string,
  archive: boolean | undefined,
): RouteLocationRaw {
  return {
    name: RECRUTEMENTS_TAB_ROUTE_NAMES[archive ? 'archives' : DEFAULT_RECRUTEMENT_TAB],
    params: { organismeUuid },
  }
}

export const recrutementsRoutes: RouteRecordRaw[] = [
  {
    path: `${ORGANISME_PATH_PREFIX}/recrutements`,
    name: RECRUTEMENTS_TAB_ROUTE_NAMES.actifs,
    component: () => import('./views/RecrutementsView.vue'),
    meta: tabMeta('actifs'),
  },
  {
    path: `${ORGANISME_PATH_PREFIX}/recrutements/archives`,
    name: RECRUTEMENTS_TAB_ROUTE_NAMES.archives,
    component: () => import('./views/RecrutementsView.vue'),
    meta: tabMeta('archives'),
  },
]
