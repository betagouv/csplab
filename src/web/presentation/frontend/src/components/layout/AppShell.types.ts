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
