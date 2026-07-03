import type { EtapeRecrutement } from '../parametres/api'

type Categorie = EtapeRecrutement['categorie']
type BadgeType = 'info' | 'success' | 'error'

export interface CategorieBadgeConfig {
  label: string
  icon: string
  type?: BadgeType
}

export const CATEGORIE_BADGE: Record<Categorie, CategorieBadgeConfig> = {
  ENTREE: { label: 'À traiter', icon: 'ri:inbox-2-line' },
  EN_COURS: { label: 'En cours', icon: 'ri:progress-4-line', type: 'info' },
  REFUS: { label: 'Refusée', icon: 'ri:close-circle-line', type: 'error' },
  ACCEPTE: { label: 'Acceptée', icon: 'ri:checkbox-circle-line', type: 'success' },
}
