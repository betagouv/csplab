export interface NavItem {
  icon: string
  label: string
  /** Nom de route vue-router cible. */
  to: string
}

export interface NavGroup {
  label: string
  items: NavItem[]
}

export const ATS_NAVIGATION: NavGroup[] = [
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
