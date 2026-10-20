// Modèle de données du prototype « création d'offre ».
// Volontairement plat et sérialisable : tout l'état d'une offre tient dans `OffreState`.

/** D'où vient une valeur : sert à distinguer « déjà disponible » de « à compléter ». */
export type Origine = 'dar' | 'fiche' | 'offre' | 'contribution'

export type StartMode = 'besoin' | 'fiche' | 'duplication' | 'vierge'

export type StatutOffre = 'brouillon' | 'a_valider' | 'a_corriger' | 'validee' | 'publiee'

export type StepId
  = | 'besoin'
    | 'poste'
    | 'offre'
    | 'conditions'
    | 'evaluation'
    | 'validation'
    | 'diffusion'
    | 'recap'

export interface Besoin {
  intitule: string
  organisme: string
  service: string
  motif: string
  motifPrecision: string
  posteRemplace: string
  localisation: string
  teletravail: string
  metier: string | null
  metierHorsReferentiel: string
  metiersAssocies: string[]
  categories: string[]
  statuts: string[]
  typeContrat: string
  dureeContrat: string
  corps: string
  quotite: string
  datePriseDePoste: string
  nbPostes: string
  ficheRef: string
  darApplicable: 'oui' | 'non' | 'nsp'
  darRef: string
  darStatut: 'validee' | 'en_cours' | 'a_demander' | ''
}

export interface Poste {
  missions: string
  activites: string[]
  environnement: string
  competences: string[]
  qualifications: string
  profil: string
  aDesConditions: boolean
  conditionsParticulieres: string
}

export type SectionOffreId
  = | 'organisme'
    | 'poste'
    | 'missions'
    | 'profil'
    | 'conditions'
    | 'pratique'
    | 'candidature'

export interface SectionOffre {
  texte: string
  /** `reprise` : texte repris tel quel d'une étape précédente, pas encore retravaillé. */
  etat: 'vide' | 'reprise' | 'redige'
}

export interface Critere {
  id: string
  libelle: string
  type: 'diplome' | 'experience' | 'competence' | 'permis' | 'autre'
}

export interface Question {
  id: string
  libelle: string
  format: 'oui_non' | 'texte' | 'choix'
  choix: string[]
  /** Pour une question oui/non : la réponse « non » écarte la candidature du premier tri. */
  bloquante: boolean
  critereId: string | null
}

export interface CritereEvaluation {
  id: string
  libelle: string
  importance: 'essentiel' | 'important' | 'complementaire'
  depuisCritereId: string | null
}

export interface Conditions {
  profils: string[]
  indispensables: Critere[]
  souhaites: Critere[]
  questions: Question[]
}

export interface Evaluation {
  active: boolean
  criteres: CritereEvaluation[]
  premierTri: { id: string, libelle: string }[]
  tours: string
  format: string
  jury: string[]
}

export interface Personne {
  id: string
  nom: string
  role: string
  service: string
}

export interface EtapeCircuit {
  id: string
  libelle: string
  personneId: string
  obligatoire: boolean
  statut: 'a_venir' | 'en_attente' | 'approuve' | 'corrections'
  date: string | null
  /** Étape déjà franchie hors de l'outil (ex. DAR validée avant la création de l'offre). */
  externe?: boolean
}

export interface Remarque {
  id: string
  auteurId: string
  date: string
  texte: string
  stepId: StepId
  resolue: boolean
}

export interface Contribution {
  id: string
  personneId: string
  stepId: StepId
  demande: string
  statut: 'en_attente' | 'faite'
}

export interface Canal {
  id: string
  nom: string
  description: string
  mode: 'connecteur' | 'manuel'
  selectionne: boolean
  /** Informations que le canal attend en plus de l'offre (hypothèses, non vérifiées). */
  attendus: { libelle: string, ok: (s: OffreState) => boolean, stepId: StepId }[]
  actionsManuelles: string[]
}

export interface Journal {
  date: string
  texte: string
}

export interface OffreState {
  reference: string
  startMode: StartMode | null
  sourceLibelle: string
  besoin: Besoin
  poste: Poste
  offre: Record<SectionOffreId, SectionOffre>
  conditions: Conditions
  evaluation: Evaluation
  circuit: EtapeCircuit[]
  remarques: Remarque[]
  contributions: Contribution[]
  canaux: { id: string, selectionne: boolean, fait: string[] }[]
  dateDebutDiffusion: string
  dateLimite: string
  statut: StatutOffre
  /** Valeurs reprises d'une source, par chemin de champ (`besoin.intitule`). */
  origines: Record<string, { origine: Origine, valeur: unknown }>
  journal: Journal[]
  /** Équipe de recrutement et droits sur les candidatures après publication. */
  equipe: { personneId: string, acces: 'gestion' | 'evaluation' | 'lecture' }[]
  organisation: 'avec_dar' | 'sans_dar'
}
