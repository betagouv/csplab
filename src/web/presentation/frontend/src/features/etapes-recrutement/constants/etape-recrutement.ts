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

export interface EtapesListeTexts {
  title: string
  calloutTitle: string
  calloutDescription: string
  resetDescription: string
}

export const ETAPES_TEXTS_ORGANISME: EtapesListeTexts = {
  title: 'Étapes de recrutement',
  calloutTitle: 'Modification des étapes de recrutement',
  calloutDescription: 'Ce modèle d\'étapes sera appliqué par défaut à tous les nouveaux recrutements. Les modifications apportées à ce modèle ne s\'appliqueront qu\'aux nouvelles offres.',
  resetDescription: 'Voulez-vous vraiment réinitialiser les étapes de recrutement ? Toutes vos personnalisations seront perdues et remplacées par la configuration par défaut.',
}

export const ETAPES_TEXTS_OFFRE: EtapesListeTexts = {
  title: 'Étapes de recrutement',
  calloutTitle: 'Modification des étapes de recrutement',
  calloutDescription: 'Ces étapes ne s\'appliquent qu\'à cette offre et remplacent le modèle défini dans les paramètres de l\'organisme. Une étape ne doit pas contenir de candidature pour pouvoir être supprimée.',
  resetDescription: 'Voulez-vous vraiment réinitialiser les étapes de cette offre ? Vos personnalisations seront perdues et remplacées par le modèle de l\'organisme.',
}
