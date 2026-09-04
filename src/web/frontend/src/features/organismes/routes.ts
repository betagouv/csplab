import type { RouteRecordRaw } from 'vue-router'
import type { OrganismeTabKey } from './constants/organisme'
import { tabMetaFor } from '@/composables/navigation/tabs'
import { ORGANISME_PATH_PREFIX } from '@/router/params'
import { ORGANISME_TAB_LABELS } from './constants/organisme'

export const ORGANISME_TAB_ROUTE_NAMES = {
  membres: 'organisme',
  etapes: 'organisme-etapes',
} as const satisfies Record<OrganismeTabKey, string>

const tabMeta = tabMetaFor(ORGANISME_TAB_LABELS)

export const organismesRoutes: RouteRecordRaw[] = [
  {
    path: '/organismes',
    name: 'organismes',
    component: () => import('./views/GestionOrganismesView.vue'),
  },
  {
    path: ORGANISME_PATH_PREFIX,
    name: ORGANISME_TAB_ROUTE_NAMES.membres,
    component: () => import('./views/OrganismeView.vue'),
    meta: tabMeta('membres'),
  },
  {
    path: `${ORGANISME_PATH_PREFIX}/etapes`,
    name: ORGANISME_TAB_ROUTE_NAMES.etapes,
    component: () => import('./views/OrganismeView.vue'),
    meta: tabMeta('etapes'),
  },
]
