import type { RouteRecordRaw } from 'vue-router'
import type { CandidaturePanelTabKey, CandidatureTabKey } from './constants/candidature'
import { tabMetaFor } from '@/composables/navigation/tabs'
import { ORGANISME_PATH_PREFIX, UUID_ROUTE_PARAM } from '@/router/params'
import { CANDIDATURE_PANEL_TAB_LABELS, CANDIDATURE_TAB_LABELS } from './constants/candidature'

export const CANDIDATURE_ROUTE_NAME = 'recrutement-candidature'

export const CANDIDATURE_PANEL_TAB_ROUTE_NAMES = {
  candidature: CANDIDATURE_ROUTE_NAME,
  documents: 'recrutement-candidature-documents',
  notes: 'recrutement-candidature-notes',
  messages: 'recrutement-candidature-messages',
} as const satisfies Record<CandidaturePanelTabKey, string>

export const CANDIDATURE_CONVERSATION_ROUTE_NAME = 'recrutement-candidature-conversation'

export const CANDIDATURES_TAB_ROUTE_NAMES = {
  'candidatures': 'recrutement-candidatures-kanban',
  'activites-et-taches': 'recrutement-activites',
  'equipe': 'recrutement-equipe',
} as const satisfies Record<CandidatureTabKey, string>

const tabMeta = tabMetaFor(CANDIDATURE_TAB_LABELS)
const panelTabMeta = tabMetaFor(CANDIDATURE_PANEL_TAB_LABELS)

const RECRUTEMENT_PATH = `${ORGANISME_PATH_PREFIX}/recrutements/:recrutementUuid${UUID_ROUTE_PARAM}`
const CANDIDATURE_PANEL_PATH = `candidatures/:candidatureUuid${UUID_ROUTE_PARAM}`

export const candidaturesRoutes: RouteRecordRaw[] = [
  {
    path: `${RECRUTEMENT_PATH}/activites`,
    name: CANDIDATURES_TAB_ROUTE_NAMES['activites-et-taches'],
    component: () => import('./views/CandidaturesView.vue'),
    meta: tabMeta('activites-et-taches'),
  },
  {
    path: `${RECRUTEMENT_PATH}/equipe`,
    name: CANDIDATURES_TAB_ROUTE_NAMES.equipe,
    component: () => import('./views/CandidaturesView.vue'),
    meta: tabMeta('equipe'),
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
        children: [
          {
            path: CANDIDATURE_PANEL_PATH,
            name: CANDIDATURE_PANEL_TAB_ROUTE_NAMES.candidature,
            component: () => import('./views/CandidaturePanelView.vue'),
            meta: panelTabMeta('candidature'),
          },
          {
            path: `${CANDIDATURE_PANEL_PATH}/documents`,
            name: CANDIDATURE_PANEL_TAB_ROUTE_NAMES.documents,
            component: () => import('./views/CandidaturePanelView.vue'),
            meta: panelTabMeta('documents'),
          },
          {
            path: `${CANDIDATURE_PANEL_PATH}/notes`,
            name: CANDIDATURE_PANEL_TAB_ROUTE_NAMES.notes,
            component: () => import('./views/CandidaturePanelView.vue'),
            meta: panelTabMeta('notes'),
          },
          {
            path: `${CANDIDATURE_PANEL_PATH}/messages`,
            name: CANDIDATURE_PANEL_TAB_ROUTE_NAMES.messages,
            component: () => import('./views/CandidaturePanelView.vue'),
            meta: panelTabMeta('messages'),
          },
          {
            path: `${CANDIDATURE_PANEL_PATH}/messages/:conversationUuid${UUID_ROUTE_PARAM}`,
            name: CANDIDATURE_CONVERSATION_ROUTE_NAME,
            component: () => import('./views/CandidaturePanelView.vue'),
            meta: panelTabMeta('messages'),
          },
        ],
      },
      {
        path: 'liste',
        name: 'recrutement-candidatures',
        component: () => import('./views/CandidaturesListeView.vue'),
      },
    ],
  },
]
