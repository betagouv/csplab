import type { RouteRecordRaw } from 'vue-router'
import type { CandidaturePanelRouteNames } from './names'
import { tabMetaFor } from '@/composables/navigation/tabs'
import { CANDIDATURE_PANEL_TAB_LABELS, CANDIDATURE_TAB_LABELS } from '@/features/candidatures/constants/candidature'
import { ORGANISME_TAB_LABELS } from '@/features/organismes/constants/organisme'
import { RECRUTEMENT_TAB_LABELS } from '@/features/recrutements/constants/recrutement'
import {
  CANDIDATURE_PANEL_ROUTE_NAMES,
  CANDIDATURES_TAB_ROUTE_NAMES,
  CANDIDATURES_VIEW_ROUTE_NAMES,
  HOME_ROUTE_NAME,
  NOT_FOUND_ROUTE_NAME,
  ORGANISME_SECTION_ROUTE_NAMES,
  ORGANISME_TAB_ROUTE_NAMES,
  ORGANISMES_ROUTE_NAME,
  RECRUTEMENT_ETAPES_ROUTE_NAME,
  RECRUTEMENTS_TAB_ROUTE_NAMES,
} from './names'

const UUID = '([0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12})'

const organismeTabMeta = tabMetaFor(ORGANISME_TAB_LABELS)
const recrutementsTabMeta = tabMetaFor(RECRUTEMENT_TAB_LABELS)
const recrutementTabMeta = tabMetaFor(CANDIDATURE_TAB_LABELS)
const panelTabMeta = tabMetaFor(CANDIDATURE_PANEL_TAB_LABELS)

const OrganismeView = () => import('@/features/organismes/views/OrganismeView.vue')
const RecrutementsView = () => import('@/features/recrutements/views/RecrutementsView.vue')
const CandidaturesView = () => import('@/features/candidatures/views/CandidaturesView.vue')
const CandidaturePanelView = () => import('@/features/candidatures/views/CandidaturePanelView.vue')

const CANDIDATURE_PANEL_PATH = `candidatures/:candidatureUuid${UUID}`

function candidaturePanelRoutes({ tabs, conversations }: CandidaturePanelRouteNames): RouteRecordRaw[] {
  return [
    { path: CANDIDATURE_PANEL_PATH, name: tabs.candidature, component: CandidaturePanelView, meta: panelTabMeta('candidature') },
    { path: `${CANDIDATURE_PANEL_PATH}/historique`, name: tabs.historique, component: CandidaturePanelView, meta: panelTabMeta('historique') },
    { path: `${CANDIDATURE_PANEL_PATH}/documents`, name: tabs.documents, component: CandidaturePanelView, meta: panelTabMeta('documents') },
    { path: `${CANDIDATURE_PANEL_PATH}/notes`, name: tabs.notes, component: CandidaturePanelView, meta: panelTabMeta('notes') },
    { path: `${CANDIDATURE_PANEL_PATH}/messages`, name: tabs.messages, component: CandidaturePanelView, meta: panelTabMeta('messages') },
    { path: `${CANDIDATURE_PANEL_PATH}/messages/nouveau`, name: conversations.create, component: CandidaturePanelView, meta: panelTabMeta('messages') },
    {
      path: `${CANDIDATURE_PANEL_PATH}/messages/:conversationUuid${UUID}`,
      name: conversations.conversation,
      component: CandidaturePanelView,
      meta: panelTabMeta('messages'),
    },
  ]
}

const recrutementRoutes: RouteRecordRaw[] = [
  {
    path: '',
    component: CandidaturesView,
    meta: recrutementTabMeta('candidatures'),
    children: [
      {
        path: '',
        name: CANDIDATURES_VIEW_ROUTE_NAMES.kanban,
        component: () => import('@/features/candidatures/views/CandidaturesKanbanView.vue'),
        meta: { candidaturesView: 'kanban' },
        children: candidaturePanelRoutes(CANDIDATURE_PANEL_ROUTE_NAMES.kanban),
      },
      {
        path: 'liste',
        name: CANDIDATURES_VIEW_ROUTE_NAMES.liste,
        component: () => import('@/features/candidatures/views/CandidaturesListeView.vue'),
        meta: { candidaturesView: 'liste' },
        children: candidaturePanelRoutes(CANDIDATURE_PANEL_ROUTE_NAMES.liste),
      },
    ],
  },
  {
    path: 'activites',
    name: CANDIDATURES_TAB_ROUTE_NAMES['activites-et-taches'],
    component: CandidaturesView,
    meta: recrutementTabMeta('activites-et-taches'),
  },
  {
    path: 'equipe',
    name: CANDIDATURES_TAB_ROUTE_NAMES.equipe,
    component: CandidaturesView,
    meta: recrutementTabMeta('equipe'),
  },
  {
    path: 'etapes-recrutement',
    name: RECRUTEMENT_ETAPES_ROUTE_NAME,
    component: () => import('@/features/etapes-recrutement/views/OffreEtapesRecrutementView.vue'),
  },
]

const organismeRoutes: RouteRecordRaw[] = [
  {
    path: '',
    name: ORGANISME_SECTION_ROUTE_NAMES.parametres,
    children: [
      { path: '', name: ORGANISME_TAB_ROUTE_NAMES.membres, component: OrganismeView, meta: organismeTabMeta('membres') },
      { path: 'etapes', name: ORGANISME_TAB_ROUTE_NAMES.etapes, component: OrganismeView, meta: organismeTabMeta('etapes') },
    ],
  },
  {
    path: 'recrutements',
    name: ORGANISME_SECTION_ROUTE_NAMES.recrutements,
    children: [
      { path: '', name: RECRUTEMENTS_TAB_ROUTE_NAMES.actifs, component: RecrutementsView, meta: recrutementsTabMeta('actifs') },
      { path: 'archives', name: RECRUTEMENTS_TAB_ROUTE_NAMES.archives, component: RecrutementsView, meta: recrutementsTabMeta('archives') },
      { path: `:recrutementUuid${UUID}`, children: recrutementRoutes },
    ],
  },
]

export const routes: RouteRecordRaw[] = [
  {
    path: '/',
    name: HOME_ROUTE_NAME,
    component: () => import('@/views/HomeView.vue'),
  },
  {
    path: '/organismes',
    name: ORGANISMES_ROUTE_NAME,
    component: () => import('@/features/organismes/views/GestionOrganismesView.vue'),
  },
  {
    path: `/organismes/:organismeUuid${UUID}`,
    children: organismeRoutes,
  },
  {
    path: '/:pathMatch(.*)*',
    name: NOT_FOUND_ROUTE_NAME,
    component: () => import('@/views/NotFoundView.vue'),
  },
]
