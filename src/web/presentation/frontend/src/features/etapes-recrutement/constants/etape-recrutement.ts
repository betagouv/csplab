import type { EtapeRecrutement } from '../types'

export type Categorie = EtapeRecrutement['categorie']
export type BadgeType = 'info' | 'success' | 'error'

export interface CategorieConfig {
  label: string
  icon: string
  type?: BadgeType
  cssModifier: string
}

export const CATEGORIE_CONFIG: Record<Categorie, CategorieConfig> = {
  ENTREE: { label: 'À traiter', icon: 'ri:inbox-2-line', cssModifier: 'entree' },
  EN_COURS: { label: 'En cours', icon: 'ri:progress-4-line', type: 'info', cssModifier: 'en-cours' },
  REFUS: { label: 'Refusée', icon: 'ri:close-circle-line', type: 'error', cssModifier: 'refus' },
  ACCEPTE: { label: 'Acceptée', icon: 'ri:checkbox-circle-line', type: 'success', cssModifier: 'accepte' },
}
