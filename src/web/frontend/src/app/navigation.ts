import type { NavItem } from '@/components/layout/CspAppShell/CspAppShell.types'
import {
  ORGANISME_SECTION_ROUTE_NAMES,
  ORGANISME_TAB_ROUTE_NAMES,
  ORGANISMES_ROUTE_NAME,
  RECRUTEMENTS_TAB_ROUTE_NAMES,
} from '@/router/names'

const ORGANISMES_ITEM: NavItem = {
  icon: 'ri:government-line',
  label: 'Gestion des organismes',
  to: ORGANISMES_ROUTE_NAME,
}

function recrutementsItem(organismeUuid: string, label: string): NavItem {
  return {
    icon: 'ri:briefcase-line',
    label,
    to: RECRUTEMENTS_TAB_ROUTE_NAMES.actifs,
    params: { organismeUuid },
    match: [ORGANISME_SECTION_ROUTE_NAMES.recrutements],
  }
}

function parametresItem(organismeUuid: string): NavItem {
  return {
    icon: 'ri:settings-3-line',
    label: 'Paramètres de l\'organisme',
    to: ORGANISME_TAB_ROUTE_NAMES.membres,
    params: { organismeUuid },
    match: [ORGANISME_SECTION_ROUTE_NAMES.parametres],
  }
}

export function isNavItemActive(item: NavItem, matchedRouteNames: string[]): boolean {
  const names = item.match ?? [item.to]
  return matchedRouteNames.some(name => names.includes(name))
}

export function navigationFor(options: {
  isStaff: boolean
  organismeUuid: string | null
  canManageOrganisme: boolean
}): NavItem[] {
  const { isStaff, organismeUuid, canManageOrganisme } = options

  if (!organismeUuid) {
    return isStaff ? [ORGANISMES_ITEM] : []
  }

  if (!canManageOrganisme) {
    return [recrutementsItem(organismeUuid, 'Mes recrutements')]
  }

  return [recrutementsItem(organismeUuid, 'Recrutements'), parametresItem(organismeUuid)]
}
