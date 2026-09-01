import type { RouteRecordRaw } from 'vue-router'

export const ORGANISME_TAB_ROUTE_NAMES = {
  membres: 'organisme',
  etapes: 'organisme-etapes',
} as const

export const MON_ORGANISME_TAB_ROUTE_NAMES = {
  membres: 'mon-organisme',
  etapes: 'mon-organisme-etapes',
} as const

export const organismesRoutes: RouteRecordRaw[] = [
  {
    path: '/organismes',
    name: 'organismes',
    component: () => import('./views/GestionOrganismesView.vue'),
  },
  {
    path: '/organismes/:organismeUuid',
    name: ORGANISME_TAB_ROUTE_NAMES.membres,
    component: () => import('./views/OrganismeView.vue'),
    meta: { tab: 'membres' },
  },
  {
    path: '/organismes/:organismeUuid/etapes',
    name: ORGANISME_TAB_ROUTE_NAMES.etapes,
    component: () => import('./views/OrganismeView.vue'),
    meta: { tab: 'etapes' },
  },
  {
    path: '/mon-organisme',
    name: MON_ORGANISME_TAB_ROUTE_NAMES.membres,
    component: () => import('./views/OrganismeView.vue'),
    meta: { requiresCurrentOrganisme: true, tab: 'membres' },
  },
  {
    path: '/mon-organisme/etapes',
    name: MON_ORGANISME_TAB_ROUTE_NAMES.etapes,
    component: () => import('./views/OrganismeView.vue'),
    meta: { requiresCurrentOrganisme: true, tab: 'etapes' },
  },
]
