import type { RouteRecordRaw } from 'vue-router'
import type { CandidaturePanelTabKey, CandidatureTabKey } from './constants/candidature'
import type { NoteRouteNames } from './types'
import type { ConversationRouteNames } from '@/features/messages/types'
import { tabMetaFor } from '@/composables/navigation/tabs'
import { ORGANISME_PATH_PREFIX, UUID_ROUTE_PARAM } from '@/router/params'
import { CANDIDATURE_PANEL_TAB_LABELS, CANDIDATURE_TAB_LABELS } from './constants/candidature'

export type CandidaturesViewName = 'kanban' | 'liste'

declare module 'vue-router' {
  interface RouteMeta {
    candidaturesView?: CandidaturesViewName
  }
}

export const CANDIDATURES_VIEW_ROUTE_NAMES = {
  kanban: 'recrutement-candidatures-kanban',
  liste: 'recrutement-candidatures',
} as const satisfies Record<CandidaturesViewName, string>

export interface CandidaturePanelRouteNames {
  tabs: Record<CandidaturePanelTabKey, string>
  conversations: ConversationRouteNames
  notes: NoteRouteNames
}

function panelRouteNames(prefix: string): CandidaturePanelRouteNames {
  const tabs = {
    candidature: prefix,
    historique: `${prefix}-historique`,
    documents: `${prefix}-documents`,
    notes: `${prefix}-notes`,
    messages: `${prefix}-messages`,
  }
  return {
    tabs,
    conversations: {
      conversations: tabs.messages,
      create: `${prefix}-nouvelle-conversation`,
      conversation: `${prefix}-conversation`,
    },
    notes: {
      notes: tabs.notes,
      create: `${prefix}-nouvelle-note`,
    },
  }
}

export const CANDIDATURE_PANEL_ROUTE_NAMES = {
  kanban: panelRouteNames('recrutement-candidature'),
  liste: panelRouteNames('recrutement-liste-candidature'),
} as const satisfies Record<CandidaturesViewName, CandidaturePanelRouteNames>

export const CANDIDATURES_TAB_ROUTE_NAMES = {
  'candidatures': CANDIDATURES_VIEW_ROUTE_NAMES.kanban,
  'activites-et-taches': 'recrutement-activites',
  'equipe': 'recrutement-equipe',
} as const satisfies Record<CandidatureTabKey, string>

const tabMeta = tabMetaFor(CANDIDATURE_TAB_LABELS)
const panelTabMeta = tabMetaFor(CANDIDATURE_PANEL_TAB_LABELS)

const RECRUTEMENT_PATH = `${ORGANISME_PATH_PREFIX}/recrutements/:recrutementUuid${UUID_ROUTE_PARAM}`
const CANDIDATURE_PANEL_PATH = `candidatures/:candidatureUuid${UUID_ROUTE_PARAM}`

function panelRoutes({ tabs, conversations, notes }: CandidaturePanelRouteNames): RouteRecordRaw[] {
  const panel = () => import('./views/CandidaturePanelView.vue')
  return [
    { path: CANDIDATURE_PANEL_PATH, name: tabs.candidature, component: panel, meta: panelTabMeta('candidature') },
    { path: `${CANDIDATURE_PANEL_PATH}/historique`, name: tabs.historique, component: panel, meta: panelTabMeta('historique') },
    { path: `${CANDIDATURE_PANEL_PATH}/documents`, name: tabs.documents, component: panel, meta: panelTabMeta('documents') },
    { path: `${CANDIDATURE_PANEL_PATH}/notes`, name: tabs.notes, component: panel, meta: panelTabMeta('notes') },
    { path: `${CANDIDATURE_PANEL_PATH}/notes/nouvelle`, name: notes.create, component: panel, meta: panelTabMeta('notes') },
    { path: `${CANDIDATURE_PANEL_PATH}/messages`, name: tabs.messages, component: panel, meta: panelTabMeta('messages') },
    { path: `${CANDIDATURE_PANEL_PATH}/messages/nouveau`, name: conversations.create, component: panel, meta: panelTabMeta('messages') },
    {
      path: `${CANDIDATURE_PANEL_PATH}/messages/:conversationUuid${UUID_ROUTE_PARAM}`,
      name: conversations.conversation,
      component: panel,
      meta: panelTabMeta('messages'),
    },
  ]
}

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
        name: CANDIDATURES_VIEW_ROUTE_NAMES.kanban,
        component: () => import('./views/CandidaturesKanbanView.vue'),
        meta: { candidaturesView: 'kanban' },
        children: panelRoutes(CANDIDATURE_PANEL_ROUTE_NAMES.kanban),
      },
      {
        path: 'liste',
        name: CANDIDATURES_VIEW_ROUTE_NAMES.liste,
        component: () => import('./views/CandidaturesListeView.vue'),
        meta: { candidaturesView: 'liste' },
        children: panelRoutes(CANDIDATURE_PANEL_ROUTE_NAMES.liste),
      },
    ],
  },
]
