import type { RouteRecordRaw } from 'vue-router'
import type { CandidatureTabKey } from './constants/candidature'
import { tabMetaFor } from '@/composables/navigation/tabs'
import { ORGANISME_PATH_PREFIX, UUID_ROUTE_PARAM } from '@/router/params'
import { CANDIDATURE_TAB_LABELS } from './constants/candidature'

export const CANDIDATURES_TAB_ROUTE_NAMES = {
  'candidatures': 'recrutement-candidatures-kanban',
  'activites-et-taches': 'recrutement-activites',
} as const satisfies Record<CandidatureTabKey, string>

const tabMeta = tabMetaFor(CANDIDATURE_TAB_LABELS)

const RECRUTEMENT_PATH = `${ORGANISME_PATH_PREFIX}/recrutements/:recrutementUuid${UUID_ROUTE_PARAM}`

export const candidaturesRoutes: RouteRecordRaw[] = [
  {
    path: `${RECRUTEMENT_PATH}/activites`,
    name: CANDIDATURES_TAB_ROUTE_NAMES['activites-et-taches'],
    component: () => import('./views/CandidaturesView.vue'),
    meta: tabMeta('activites-et-taches'),
  },
  {
    path: RECRUTEMENT_PATH,
    component: () => import('./views/CandidaturesView.vue'),
    meta: tabMeta('candidatures'),
    children: [
      {
        path: '',
        name: 'recrutement-candidatures-kanban',
        component: () => import('./views/CandidaturesKanbanView.vue'),
      },
      {
        path: 'liste',
        name: 'recrutement-candidatures',
        component: () => import('./views/CandidaturesListeView.vue'),
      },
    ],
  },
]
