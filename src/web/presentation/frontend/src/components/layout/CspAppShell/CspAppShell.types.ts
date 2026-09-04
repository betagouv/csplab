export interface NavItem {
  icon: string
  label: string
  /** Nom de route vue-router cible. */
  to: string
  params?: Record<string, string>
  /** Noms de routes qui rendent l'entrée active. Par défaut, `to` seul. */
  match?: string[]
}
