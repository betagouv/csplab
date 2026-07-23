import type { NavGroup } from '@/components/layout/CspAppShell/CspAppShell.types'

export const APP_NAVIGATION: NavGroup[] = [
  {
    label: 'Pilotage',
    items: [
      { icon: 'ri:briefcase-line', label: 'Mes recrutements', to: 'mes-recrutements' },
    ],
  },
  {
    label: 'Paramètres',
    items: [
      { icon: 'ri:settings-3-line', label: 'Paramètres', to: 'parametres' },
    ],
  },
]
