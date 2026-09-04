import type { NavItem } from '@/components/layout/CspAppShell/CspAppShell.types'
import { CANDIDATURES_TAB_ROUTE_NAMES } from '@/features/candidatures/routes'
import { RECRUTEMENTS_TAB_ROUTE_NAMES } from '@/features/recrutements/routes'

const ORGANISMES_ITEM: NavItem = {
  icon: 'ri:settings-3-line',
  label: 'Gestion des organismes',
  to: 'organismes',
  match: ['organismes'],
}

function recrutementsItem(organismeUuid: string): NavItem {
  return {
    icon: 'ri:briefcase-line',
    label: 'Recrutements',
    to: RECRUTEMENTS_TAB_ROUTE_NAMES.actifs,
    params: { organismeUuid },
    match: [
      ...Object.values(RECRUTEMENTS_TAB_ROUTE_NAMES),
      ...Object.values(CANDIDATURES_TAB_ROUTE_NAMES),
      'recrutement-candidatures',
      'recrutement-etapes-recrutement',
    ],
  }
}

export function isNavItemActive(item: NavItem, matchedRouteNames: string[]): boolean {
  const names = item.match ?? [item.to]
  return matchedRouteNames.some(name => names.includes(name))
}

export function navigationFor(options: {
  isStaff: boolean
  organismeUuid: string | null
}): NavItem[] {
  const { isStaff, organismeUuid } = options

  const items: NavItem[] = []

  if (isStaff) {
    items.push(ORGANISMES_ITEM)
  }

  if (organismeUuid) {
    items.push(recrutementsItem(organismeUuid))
  }

  return items
}
