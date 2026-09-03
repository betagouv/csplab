import type { NavItem } from '@/components/layout/CspAppShell/CspAppShell.types'

const AGENT_NAVIGATION: NavItem[] = [
  { icon: 'ri:briefcase-line', label: 'Mes recrutements', to: 'mes-recrutements' },
  { icon: 'ri:settings-3-line', label: 'Gestion des organismes', to: 'organismes' },
]

const STAFF_NAVIGATION: NavItem[] = [
  { icon: 'ri:settings-3-line', label: 'Gestion des organismes', to: 'organismes' },
]

export function navigationFor(isStaff: boolean): NavItem[] {
  return isStaff ? STAFF_NAVIGATION : AGENT_NAVIGATION
}
