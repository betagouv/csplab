import type { NavGroup } from '@/components/layout/CspAppShell/CspAppShell.types'

export const APP_NAVIGATION: NavGroup[] = [
  {
    items: [
      { icon: 'ri:briefcase-line', label: 'Mes recrutements', to: 'mes-recrutements' },
      { icon: 'ri:settings-3-line', label: 'Paramètres', to: 'parametres' },
    ],
  },
]
