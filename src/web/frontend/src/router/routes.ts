import type { RouteLocationNormalized, RouteRecordRaw } from 'vue-router'
import type { CandidaturePanelRouteNames } from './names'
import { tabMetaFor } from '@/composables/navigation/tabs'
import { CANDIDATURE_PANEL_TAB_LABELS } from '@/features/candidatures/constants/candidature'
import { ORGANISME_TAB_LABELS } from '@/features/organismes/constants/organisme'
import { RECRUTEMENT_DETAIL_TAB_LABELS, RECRUTEMENT_TAB_LABELS } from '@/features/recrutements/constants/recrutement'
import { redirectHome } from './home'
import {
  CANDIDATURE_PANEL_ROUTE_NAMES,
  CANDIDATURES_LAYOUT_ROUTE_NAMES,
  HOME_ROUTE_NAME,
  NOT_FOUND_ROUTE_NAME,
  ORGANISME_HOME_ROUTE_NAME,
  ORGANISME_NAV_ROUTE_NAMES,
  ORGANISME_TAB_ROUTE_NAMES,
  ORGANISMES_ROUTE_NAME,
  RECRUTEMENT_DETAIL_TAB_ROUTE_NAMES,
  RECRUTEMENT_ETAPES_ROUTE_NAME,
  RECRUTEMENTS_TAB_ROUTE_NAMES,
} from './names'

const UUID = '([0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12})'

const organismeTabMeta = tabMetaFor(ORGANISME_TAB_LABELS)
const recrutementsTabMeta = tabMetaFor(RECRUTEMENT_TAB_LABELS)
const recrutementTabMeta = tabMetaFor(RECRUTEMENT_DETAIL_TAB_LABELS)
const panelTabMeta = tabMetaFor(CANDIDATURE_PANEL_TAB_LABELS)

const HomeView = () => import('@/features/home/views/HomeView.vue')
const RecrutementsView = () => import('@/features/recrutements/views/RecrutementsView.vue')
const CandidaturePanelView = () => import('@/features/candidatures/views/CandidaturePanelView.vue')

function paramsAsProps(...names: string[]) {
  return ({ params }: RouteLocationNormalized) => Object.fromEntries(names.map(name => [name, params[name]]))
}

const recrutementProps = paramsAsProps('organismeUuid', 'recrutementUuid')
const candidatureProps = paramsAsProps('organismeUuid', 'recrutementUuid', 'candidatureUuid')

const CANDIDATURE_PANEL_PATH = `candidatures/:candidatureUuid${UUID}`

function candidaturePanelRoutes({ tabs, conversations, notes }: CandidaturePanelRouteNames): RouteRecordRaw[] {
  return [
    { path: CANDIDATURE_PANEL_PATH, name: tabs.candidature, component: CandidaturePanelView, props: candidatureProps, meta: panelTabMeta('candidature') },
    { path: `${CANDIDATURE_PANEL_PATH}/historique`, name: tabs.historique, component: CandidaturePanelView, props: candidatureProps, meta: panelTabMeta('historique') },
    { path: `${CANDIDATURE_PANEL_PATH}/documents`, name: tabs.documents, component: CandidaturePanelView, props: candidatureProps, meta: panelTabMeta('documents') },
    { path: `${CANDIDATURE_PANEL_PATH}/notes`, name: tabs.notes, component: CandidaturePanelView, props: candidatureProps, meta: panelTabMeta('notes') },
    { path: `${CANDIDATURE_PANEL_PATH}/notes/nouvelle`, name: notes.create, component: CandidaturePanelView, props: candidatureProps, meta: panelTabMeta('notes') },
    { path: `${CANDIDATURE_PANEL_PATH}/messages`, name: tabs.messages, component: CandidaturePanelView, props: candidatureProps, meta: panelTabMeta('messages') },
    { path: `${CANDIDATURE_PANEL_PATH}/messages/nouveau`, name: conversations.create, component: CandidaturePanelView, props: candidatureProps, meta: panelTabMeta('messages') },
    {
      path: `${CANDIDATURE_PANEL_PATH}/messages/:conversationUuid${UUID}`,
      name: conversations.conversation,
      component: CandidaturePanelView,
      props: candidatureProps,
      meta: panelTabMeta('messages'),
    },
  ]
}

const recrutementRoutes: RouteRecordRaw[] = [
  {
    path: '',
    component: () => import('@/features/recrutements/views/RecrutementView.vue'),
    props: recrutementProps,
    children: [
      {
        path: '',
        component: () => import('@/features/candidatures/views/CandidaturesTabView.vue'),
        props: recrutementProps,
        meta: recrutementTabMeta('candidatures'),
        children: [
          {
            path: '',
            name: CANDIDATURES_LAYOUT_ROUTE_NAMES.kanban,
            component: () => import('@/features/candidatures/views/CandidaturesKanbanView.vue'),
            props: recrutementProps,
            meta: { candidaturesLayout: 'kanban' },
            children: candidaturePanelRoutes(CANDIDATURE_PANEL_ROUTE_NAMES.kanban),
          },
          {
            path: 'liste',
            name: CANDIDATURES_LAYOUT_ROUTE_NAMES.liste,
            component: () => import('@/features/candidatures/views/CandidaturesListeView.vue'),
            props: candidatureProps,
            meta: { candidaturesLayout: 'liste' },
            children: candidaturePanelRoutes(CANDIDATURE_PANEL_ROUTE_NAMES.liste),
          },
        ],
      },
      {
        path: 'activites',
        name: RECRUTEMENT_DETAIL_TAB_ROUTE_NAMES['activites-et-taches'],
        component: () => import('@/features/recrutements/views/ActivitesTachesView.vue'),
        meta: recrutementTabMeta('activites-et-taches'),
      },
      {
        path: 'equipe',
        name: RECRUTEMENT_DETAIL_TAB_ROUTE_NAMES.equipe,
        component: () => import('@/features/equipe-recrutement/views/EquipeRecrutementView.vue'),
        props: true,
        meta: recrutementTabMeta('equipe'),
      },
    ],
  },
  {
    path: 'etapes-recrutement',
    name: RECRUTEMENT_ETAPES_ROUTE_NAME,
    component: () => import('@/features/etapes-recrutement/views/OffreEtapesRecrutementView.vue'),
    props: true,
  },
]

const organismeRoutes: RouteRecordRaw[] = [
  { path: 'accueil', name: ORGANISME_HOME_ROUTE_NAME, component: HomeView, props: true },
  {
    path: '',
    name: ORGANISME_NAV_ROUTE_NAMES.parametres,
    children: [
      {
        path: '',
        component: () => import('@/features/organismes/views/OrganismeView.vue'),
        props: true,
        children: [
          {
            path: '',
            name: ORGANISME_TAB_ROUTE_NAMES.membres,
            component: () => import('@/features/organismes/views/OrganismeAgentsView.vue'),
            props: true,
            meta: organismeTabMeta('membres'),
          },
          {
            path: 'etapes',
            name: ORGANISME_TAB_ROUTE_NAMES.etapes,
            component: () => import('@/features/etapes-recrutement/views/OrganismeEtapesView.vue'),
            props: true,
            meta: organismeTabMeta('etapes'),
          },
          {
            path: 'etiquettes',
            name: ORGANISME_TAB_ROUTE_NAMES.tags,
            component: () => import('@/features/tags/views/TagsView.vue'),
            props: true,
            meta: organismeTabMeta('tags'),
          },
        ],
      },
    ],
  },
  {
    path: 'recrutements',
    name: ORGANISME_NAV_ROUTE_NAMES.recrutements,
    children: [
      { path: '', name: RECRUTEMENTS_TAB_ROUTE_NAMES.actifs, component: RecrutementsView, props: true, meta: recrutementsTabMeta('actifs') },
      { path: 'archives', name: RECRUTEMENTS_TAB_ROUTE_NAMES.archives, component: RecrutementsView, props: true, meta: recrutementsTabMeta('archives') },
      { path: `:recrutementUuid${UUID}`, children: recrutementRoutes },
    ],
  },
]

export const routes: RouteRecordRaw[] = [
  {
    path: '/',
    name: HOME_ROUTE_NAME,
    component: HomeView,
    beforeEnter: redirectHome,
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
