import type { RouteLocationRaw } from 'vue-router'

export const HOME_ROUTE_NAME = 'home'
export const NOT_FOUND_ROUTE_NAME = 'not-found'
export const ORGANISMES_ROUTE_NAME = 'organismes'

export const ORGANISME_SECTION_ROUTE_NAMES = {
  parametres: 'organisme-parametres',
  recrutements: 'organisme-recrutements',
} as const

export const ORGANISME_TAB_ROUTE_NAMES = {
  membres: 'organisme',
  etapes: 'organisme-etapes',
} as const

export const RECRUTEMENTS_TAB_ROUTE_NAMES = {
  actifs: 'recrutements',
  archives: 'recrutements-archives',
} as const

export const RECRUTEMENT_ETAPES_ROUTE_NAME = 'recrutement-etapes-recrutement'

export const CANDIDATURES_VIEW_ROUTE_NAMES = {
  kanban: 'recrutement-candidatures-kanban',
  liste: 'recrutement-candidatures',
} as const

export type CandidaturesViewName = keyof typeof CANDIDATURES_VIEW_ROUTE_NAMES

export const CANDIDATURES_TAB_ROUTE_NAMES = {
  'candidatures': CANDIDATURES_VIEW_ROUTE_NAMES.kanban,
  'activites-et-taches': 'recrutement-activites',
  'equipe': 'recrutement-equipe',
} as const

function panelRouteNames(prefix: string) {
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
  }
}

export type CandidaturePanelRouteNames = ReturnType<typeof panelRouteNames>

export const CANDIDATURE_PANEL_ROUTE_NAMES = {
  kanban: panelRouteNames('recrutement-candidature'),
  liste: panelRouteNames('recrutement-liste-candidature'),
} as const satisfies Record<CandidaturesViewName, CandidaturePanelRouteNames>

export function recrutementsListLocation(
  organismeUuid: string,
  archive: boolean | undefined,
): RouteLocationRaw {
  return {
    name: RECRUTEMENTS_TAB_ROUTE_NAMES[archive ? 'archives' : 'actifs'],
    params: { organismeUuid },
  }
}

declare module 'vue-router' {
  interface RouteMeta {
    candidaturesView?: CandidaturesViewName
  }
}
