import type { NavGroup } from '@/components/layout/CspAppShell/CspAppShell.types'

const AGENT_NAVIGATION: NavGroup[] = [
  {
    label: 'Pilotage',
    items: [
      { icon: 'ri:briefcase-line', label: 'Mes recrutements', to: 'mes-recrutements' },
    ],
  },
  {
    label: 'Paramètres',
    items: [
      { icon: 'ri:settings-3-line', label: 'Gestion des organismes', to: 'organismes' },
    ],
  },
]

const STAFF_NAVIGATION: NavGroup[] = [
  {
    label: 'Paramètres',
    items: [
      { icon: 'ri:settings-3-line', label: 'Gestion des organismes', to: 'organismes' },
    ],
  },
]

export function navigationFor(isStaff: boolean): NavGroup[] {
  return isStaff ? STAFF_NAVIGATION : AGENT_NAVIGATION
}
