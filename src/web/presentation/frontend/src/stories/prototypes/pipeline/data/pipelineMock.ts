export type CategorieEtape = 'INITIALE' | 'EN_COURS' | 'TERMINALE'

// Ce que le candidat voit en face d'une étape de son côté.
export type StatutCandidat = 'RECUE' | 'EN_COURS' | 'REFUSEE' | 'ACCEPTEE'

export interface EtapePrototype {
  identifiant: string
  categorie: CategorieEtape
  nom: string
  statutCandidat: StatutCandidat
}

export const statutCandidatLabels: Record<StatutCandidat, string> = {
  RECUE: 'À traiter',
  EN_COURS: 'En cours',
  REFUSEE: 'Refusée',
  ACCEPTEE: 'Acceptée',
}

// Sémantique d'état alignée sur la doctrine des badges (CspBadge type).
// Pas de côté assumé : on garde les couleurs/sémantiques de la doctrine, mais on
// choisit une icône propre à chaque statut candidat (plus parlante que l'icône
// générique du badge). RECUE et EN_COURS n'ont pas de couleur d'alerte : neutres.
export type StatutTon = 'neutre' | 'info' | 'error' | 'success'

export interface StatutVisuel {
  ton: StatutTon
  icon: string
}

export const statutCandidatVisuel: Record<StatutCandidat, StatutVisuel> = {
  RECUE: { ton: 'neutre', icon: 'ri:inbox-2-line' },
  EN_COURS: { ton: 'info', icon: 'ri:progress-4-line' },
  REFUSEE: { ton: 'error', icon: 'ri:close-circle-line' },
  ACCEPTEE: { ton: 'success', icon: 'ri:checkbox-circle-line' },
}

// Les étapes INITIALE et TERMINALE sont obligatoires : elles ouvrent et ferment
// le recrutement. Elles ne sont pas déplaçables dans le pipeline, mais restent
// des étapes pleines et actives (≠ désactivées).
export function isObligatoire(etape: EtapePrototype): boolean {
  return etape.categorie === 'INITIALE' || etape.categorie === 'TERMINALE'
}

export function createPipeline(): EtapePrototype[] {
  return [
    { identifiant: 'e-1', categorie: 'INITIALE', nom: 'Candidature à traiter', statutCandidat: 'RECUE' },
    { identifiant: 'e-2', categorie: 'EN_COURS', nom: 'Pré-qualification', statutCandidat: 'EN_COURS' },
    { identifiant: 'e-3', categorie: 'EN_COURS', nom: 'Entretien', statutCandidat: 'EN_COURS' },
    { identifiant: 'e-4', categorie: 'EN_COURS', nom: 'Proposition', statutCandidat: 'EN_COURS' },
    { identifiant: 'e-5', categorie: 'TERMINALE', nom: 'Candidature refusée', statutCandidat: 'REFUSEE' },
    { identifiant: 'e-6', categorie: 'TERMINALE', nom: 'Candidature acceptée', statutCandidat: 'ACCEPTEE' },
  ]
}
