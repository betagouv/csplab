// Scénario fictif : la DREAL Occitanie remplace une chargée de mission partie en mobilité.
// Camille Moreau (RH de proximité) crée l'offre ; Julien Lefèvre (manager) contribue ;
// la DAR a été validée avant la création de l'offre.

import type { Besoin, Conditions, EtapeCircuit, Evaluation, OffreState, Origine, Poste, SectionOffre, SectionOffreId } from './types'
import { CANAUX } from './referentiels'

/** Copie profonde tolérante aux objets réactifs Vue (structuredClone refuse les proxys). */
export function clone<T>(v: T): T {
  return v === undefined ? v : JSON.parse(JSON.stringify(v))
}

// --- Sources existantes, hors de l'outil ou dans l'outil ---

export interface SourceBesoin {
  id: string
  libelle: string
  detail: string
  statut: string
  besoin: Partial<Besoin>
}

export const BESOINS: SourceBesoin[] = [
  {
    id: 'DAR-2026-0318',
    libelle: 'Chargé·e de mission rénovation énergétique des collectivités',
    detail: 'Pôle transition énergétique · Vacance suite à mobilité · 1 poste',
    statut: 'DAR validée le 2 octobre 2026',
    besoin: {
      intitule: 'Chargé·e de mission rénovation énergétique des collectivités',
      organisme: 'dreal-occ',
      service: 'Service Énergie, Climat, Logement — Pôle transition énergétique',
      motif: 'vacance',
      posteRemplace: 'Poste n° 31-SECL-0412',
      categories: ['A'],
      quotite: '100 %',
      nbPostes: '1',
      datePriseDePoste: '2027-01-05',
      darApplicable: 'oui',
      darRef: 'DAR-2026-0318',
      darStatut: 'validee',
    },
  },
  {
    id: 'DAR-2026-0322',
    libelle: 'Gestionnaire RH — paie et carrières',
    detail: 'Bureau des ressources humaines · Création de poste',
    statut: 'DAR en cours de validation',
    besoin: {
      intitule: 'Gestionnaire RH — paie et carrières',
      organisme: 'dreal-occ',
      service: 'Secrétariat général — Bureau des ressources humaines',
      motif: 'creation',
      categories: ['B'],
      darApplicable: 'oui',
      darRef: 'DAR-2026-0322',
      darStatut: 'en_cours',
    },
  },
]

export interface SourceFiche {
  id: string
  libelle: string
  detail: string
  besoin: Partial<Besoin>
  poste: Partial<Poste>
}

const FICHE_POSTE: Partial<Poste> = {
  missions: 'Au sein du pôle transition énergétique du SECL, le ou la titulaire du poste anime le réseau des PTRE et accompagne les EPCI dans la définition et la mise en œuvre de leurs programmes de rénovation énergétique du bâti public et privé. Il ou elle assure le suivi des crédits du BOP 135 délégués aux territoires.',
  activites: [
    'Animer le réseau régional des plateformes territoriales de rénovation énergétique (PTRE)',
    'Accompagner les EPCI dans l\'élaboration de leurs programmes de rénovation',
    'Instruire les demandes de subvention et suivre les crédits délégués',
    'Produire des bilans et indicateurs pour la direction',
    'Représenter la DREAL dans les instances partenariales',
  ],
  environnement: 'Pôle de 7 agents (4 A, 2 B, 1 C) rattaché au chef de pôle. Relations fréquentes avec les collectivités, l\'ADEME, la Région et les DDT(M).',
  competences: [
    'Connaissance des politiques publiques de l\'énergie et du logement',
    'Conduite de projet partenarial',
    'Animation de réseau',
    'Capacités rédactionnelles et de synthèse',
  ],
  qualifications: 'Formation supérieure (bac+3 minimum) dans le domaine de l\'énergie, du bâtiment, de l\'aménagement ou des politiques publiques.',
  profil: 'Agent de catégorie A, expérience souhaitée en collectivité ou en bureau d\'études.',
  aDesConditions: true,
  conditionsParticulieres: 'Déplacements réguliers en région (permis B requis, véhicule de service).',
}

export const FICHES: SourceFiche[] = [
  {
    id: 'FP-SECL-2024-012',
    libelle: 'Fiche de poste — Chargé·e de mission PTRE',
    detail: 'Mise à jour en mai 2024 · Format Word, importée depuis le SIRH',
    besoin: {
      intitule: 'Chargé·e de mission rénovation énergétique',
      organisme: 'dreal-occ',
      service: 'Service Énergie, Climat, Logement — Pôle transition énergétique',
      metier: 'm-transeco',
      categories: ['A'],
      corps: 'Ingénieur·e des travaux publics de l\'État / Attaché·e d\'administration',
      localisation: 'Toulouse (31)',
      ficheRef: 'FP-SECL-2024-012',
    },
    poste: FICHE_POSTE,
  },
]

export interface SourceOffre {
  id: string
  libelle: string
  detail: string
}

export const OFFRES_PRECEDENTES: SourceOffre[] = [
  { id: 'OFF-2025-0087', libelle: 'Chargé·e de mission rénovation énergétique', detail: 'Publiée en mars 2025 · 34 candidatures · pourvue' },
  { id: 'OFF-2026-0012', libelle: 'Chargé·e d\'études mobilité durable', detail: 'Publiée en février 2026 · 21 candidatures · pourvue' },
]

export const BROUILLONS = [
  { id: 'OFF-2026-0141', preset: 'incomplet', libelle: 'Chargé·e de mission rénovation énergétique des collectivités', detail: 'Brouillon · modifié il y a 3 jours par vous', statut: 'brouillon' },
  { id: 'OFF-2026-0139', preset: 'a_corriger', libelle: 'Chargé·e de mission rénovation énergétique des collectivités', detail: 'À corriger · remarque de Julien Lefèvre hier', statut: 'a_corriger' },
] as const

// --- Textes d'offre (destinés aux candidats) ---

export const OFFRE_REDIGEE: Record<SectionOffreId, string> = {
  organisme: 'La Direction régionale de l\'environnement, de l\'aménagement et du logement (DREAL) Occitanie met en œuvre les politiques de l\'État en matière de transition écologique, d\'énergie et de logement. Ses 900 agents travaillent au plus près des territoires, de Toulouse à Montpellier.',
  poste: 'Vous rejoignez une équipe de 7 personnes engagée dans la rénovation énergétique des bâtiments. Votre rôle : aider les intercommunalités à concevoir et réussir leurs programmes de rénovation, en lien avec les acteurs locaux.',
  missions: '- Animer le réseau régional des plateformes d\'accompagnement à la rénovation énergétique\n- Conseiller les intercommunalités dans la construction de leurs programmes\n- Instruire les demandes de subvention et suivre les financements accordés\n- Produire des bilans pour la direction et les partenaires',
  profil: 'Vous avez une formation supérieure (bac+3 minimum) dans l\'énergie, le bâtiment, l\'aménagement ou les politiques publiques. Vous aimez travailler en réseau et savez faire avancer des projets à plusieurs. Une expérience en collectivité ou en bureau d\'études est un plus.',
  conditions: 'Poste ouvert aux fonctionnaires de catégorie A et aux contractuels (CDD de 3 ans renouvelable). Rémunération selon expérience et grille indiciaire.',
  pratique: 'Poste basé à Toulouse, accessible en métro. Télétravail possible jusqu\'à 2 jours par semaine. Déplacements réguliers en Occitanie avec véhicule de service.',
  candidature: 'Envoyez votre CV et une lettre de motivation avant la date limite. Les entretiens auront lieu courant décembre. Contact : Julien Lefèvre, chef de pôle.',
}

/** Suggestions de reformulation fictives (pas de vraie IA) : affichées à côté, jamais appliquées seules. */
export const SUGGESTIONS: Partial<Record<SectionOffreId, string>> = {
  poste: 'Vous aimez les projets concrets et le travail avec les territoires ? Rejoignez une équipe de 7 personnes qui accompagne les intercommunalités d\'Occitanie dans la rénovation énergétique de leurs bâtiments.',
  missions: '- Animer et faire vivre le réseau des plateformes de rénovation énergétique de la région\n- Accompagner les intercommunalités, de l\'idée au programme financé\n- Instruire les demandes de subvention et suivre leur utilisation\n- Rendre compte des résultats à la direction et aux partenaires',
  profil: 'Vous êtes diplômé·e d\'un bac+3 ou plus (énergie, bâtiment, aménagement, politiques publiques). Vous savez fédérer des partenaires autour d\'un projet et vous exprimer clairement à l\'écrit comme à l\'oral. Une première expérience en collectivité ou en bureau d\'études serait appréciée.',
  organisme: 'La DREAL Occitanie porte les politiques de l\'État pour la transition écologique, l\'énergie et le logement dans les 13 départements de la région. Rejoindre la DREAL, c\'est agir concrètement pour le climat au service des territoires.',
}

// --- Fabriques d'état ---

function sectionsVides(): Record<SectionOffreId, SectionOffre> {
  return {
    organisme: { texte: '', etat: 'vide' },
    poste: { texte: '', etat: 'vide' },
    missions: { texte: '', etat: 'vide' },
    profil: { texte: '', etat: 'vide' },
    conditions: { texte: '', etat: 'vide' },
    pratique: { texte: '', etat: 'vide' },
    candidature: { texte: '', etat: 'vide' },
  }
}

function besoinVide(): Besoin {
  return {
    intitule: '',
    organisme: 'dreal-occ',
    service: '',
    motif: '',
    motifPrecision: '',
    posteRemplace: '',
    localisation: '',
    teletravail: '',
    metier: null,
    metierHorsReferentiel: '',
    metiersAssocies: [],
    categories: [],
    statuts: [],
    typeContrat: '',
    dureeContrat: '',
    corps: '',
    quotite: '100 %',
    datePriseDePoste: '',
    nbPostes: '1',
    ficheRef: '',
    darApplicable: 'nsp',
    darRef: '',
    darStatut: '',
  }
}

function posteVide(): Poste {
  return {
    missions: '',
    activites: [],
    environnement: '',
    competences: [],
    qualifications: '',
    profil: '',
    aDesConditions: false,
    conditionsParticulieres: '',
  }
}

function conditionsVides(): Conditions {
  return { profils: [], indispensables: [], souhaites: [], questions: [] }
}

function evaluationVide(): Evaluation {
  return { active: false, criteres: [], premierTri: [], tours: '1', format: 'presentiel', jury: [] }
}

export function circuitPour(organisation: OffreState['organisation']): EtapeCircuit[] {
  const manager: EtapeCircuit = { id: 'manager', libelle: 'Validation du contenu par le manager', personneId: 'julien', obligatoire: true, statut: 'a_venir', date: null }
  if (organisation === 'sans_validation') {
    return []
  }
  if (organisation === 'sans_dar') {
    return [manager]
  }
  return [
    manager,
    { id: 'recrutement', libelle: 'Vérification par la responsable recrutement', personneId: 'nadia', obligatoire: true, statut: 'a_venir', date: null },
  ]
}

export function etatInitial(organisation: OffreState['organisation'] = 'avec_dar'): OffreState {
  return {
    reference: 'OFF-2026-0144',
    startMode: null,
    sourceLibelle: '',
    besoin: besoinVide(),
    poste: posteVide(),
    offre: sectionsVides(),
    conditions: conditionsVides(),
    evaluation: evaluationVide(),
    circuit: circuitPour(organisation),
    remarques: [],
    contributions: [],
    canaux: CANAUX.map(c => ({ id: c.id, selectionne: c.selectionne, fait: [] })),
    dateDebutDiffusion: '',
    dateLimite: '',
    statut: 'brouillon',
    origines: {},
    journal: [{ date: 'Aujourd\'hui', texte: 'Offre créée par Camille Moreau' }],
    organisation,
    equipe: [
      { personneId: 'camille', acces: 'gestion' },
      { personneId: 'julien', acces: 'evaluation' },
      { personneId: 'nadia', acces: 'gestion' },
    ],
  }
}

// --- Préremplissage depuis une source ---

/** Applique des valeurs sur une section de l'état en mémorisant leur origine. */
function reprendre<T extends object>(cible: T, valeurs: Partial<T>, prefixe: string, origine: Origine, s: OffreState) {
  for (const [cle, valeur] of Object.entries(valeurs)) {
    if (valeur === undefined) {
      continue
    }
    ;(cible as Record<string, unknown>)[cle] = clone(valeur)
    s.origines[`${prefixe}.${cle}`] = { origine, valeur: clone(valeur) }
  }
}

export function depuisBesoin(s: OffreState, source: SourceBesoin) {
  s.startMode = 'besoin'
  s.sourceLibelle = `${source.id} — ${source.libelle}`
  reprendre(s.besoin, source.besoin, 'besoin', 'dar', s)
  s.journal.push({ date: 'Aujourd\'hui', texte: `Informations reprises de la ${source.id}` })
}

export function depuisFiche(s: OffreState, source: SourceFiche) {
  s.startMode = 'fiche'
  s.sourceLibelle = `${source.id} — ${source.libelle}`
  reprendre(s.besoin, source.besoin, 'besoin', 'fiche', s)
  reprendre(s.poste, source.poste, 'poste', 'fiche', s)
  s.journal.push({ date: 'Aujourd\'hui', texte: `Fiche de poste ${source.id} importée` })
}

export function depuisOffre(s: OffreState, source: SourceOffre) {
  s.startMode = 'duplication'
  s.sourceLibelle = `${source.id} — ${source.libelle}`
  const fiche = FICHES[0]!
  reprendre(s.besoin, { ...fiche.besoin, statuts: ['titulaire', 'contractuel'], typeContrat: 'cdd', dureeContrat: '3 ans', motif: 'vacance', teletravail: '2 jours par semaine' }, 'besoin', 'offre', s)
  reprendre(s.poste, fiche.poste, 'poste', 'offre', s)
  for (const id of Object.keys(OFFRE_REDIGEE) as SectionOffreId[]) {
    s.offre[id] = { texte: OFFRE_REDIGEE[id], etat: 'reprise' }
    s.origines[`offre.${id}`] = { origine: 'offre', valeur: OFFRE_REDIGEE[id] }
  }
  s.conditions = conditionsExemple()
  s.origines['conditions.profils'] = { origine: 'offre', valeur: s.conditions.profils }
  s.canaux.forEach((c) => {
    c.selectionne = ['csp', 'intranet', 'linkedin'].includes(c.id)
  })
  s.journal.push({ date: 'Aujourd\'hui', texte: `Offre dupliquée depuis ${source.id}` })
}

export function conditionsExemple(): Conditions {
  return {
    profils: ['fonct-meme-versant', 'fonct-autres-versants', 'contractuels'],
    indispensables: [
      { id: 'c1', libelle: 'Diplôme de niveau bac+3 minimum', type: 'diplome' },
      { id: 'c2', libelle: 'Permis B (déplacements réguliers)', type: 'permis' },
    ],
    souhaites: [
      { id: 'c3', libelle: 'Expérience en collectivité ou bureau d\'études', type: 'experience' },
      { id: 'c4', libelle: 'Connaissance des dispositifs de rénovation énergétique', type: 'competence' },
    ],
    questions: [
      { id: 'q1', libelle: 'Êtes-vous titulaire du permis B ?', format: 'oui_non', choix: [], bloquante: true, critereId: 'c2' },
    ],
  }
}

// --- États prêts à l'emploi pour les stories ---

function remplirComplet(s: OffreState) {
  depuisBesoin(s, BESOINS[0]!)
  depuisFiche(s, FICHES[0]!)
  s.startMode = 'besoin'
  s.sourceLibelle = 'DAR-2026-0318 — Chargé·e de mission rénovation énergétique des collectivités'
  s.besoin.intitule = 'Chargé·e de mission rénovation énergétique des collectivités'
  s.besoin.statuts = ['titulaire', 'contractuel']
  s.besoin.typeContrat = 'cdd'
  s.besoin.dureeContrat = '3 ans'
  s.besoin.teletravail = '2 jours par semaine'
  for (const id of Object.keys(OFFRE_REDIGEE) as SectionOffreId[]) {
    s.offre[id] = { texte: OFFRE_REDIGEE[id], etat: 'redige' }
  }
  s.conditions = conditionsExemple()
  s.canaux.forEach((c) => {
    c.selectionne = ['csp', 'intranet', 'linkedin'].includes(c.id)
  })
  s.dateDebutDiffusion = '2026-11-02'
  s.dateLimite = '2026-11-30'
}

export type Preset = 'nouveau' | 'incomplet' | 'a_valider' | 'a_corriger' | 'pret' | 'sans_dar' | 'sans_validation'

export function etatPreset(preset: Preset): OffreState {
  if (preset === 'nouveau') {
    return etatInitial()
  }
  if (preset === 'sans_validation') {
    const s = etatInitial('sans_validation')
    s.besoin.organisme = 'commune-aurin'
    s.besoin.darApplicable = 'non'
    return s
  }
  if (preset === 'sans_dar') {
    const s = etatInitial('sans_dar')
    s.besoin.organisme = 'metro-garonne'
    s.besoin.darApplicable = 'non'
    return s
  }
  const s = etatInitial()
  s.reference = 'OFF-2026-0141'
  if (preset === 'incomplet') {
    depuisBesoin(s, BESOINS[0]!)
    s.besoin.localisation = 'Toulouse (31)'
    s.besoin.statuts = ['titulaire', 'contractuel']
    s.poste.missions = FICHE_POSTE.missions!
    s.poste.activites = [...FICHE_POSTE.activites!]
    s.origines['poste.missions'] = { origine: 'fiche', valeur: FICHE_POSTE.missions }
    s.offre.organisme = { texte: OFFRE_REDIGEE.organisme, etat: 'redige' }
    s.offre.missions = { texte: FICHE_POSTE.missions!, etat: 'reprise' }
    s.contributions.push({ id: 'k1', personneId: 'julien', stepId: 'poste', demande: 'Compléter les compétences attendues et le profil recherché', statut: 'en_attente' })
    s.journal.push({ date: 'Il y a 3 jours', texte: 'Contribution demandée à Julien Lefèvre (fiche de poste)' })
    return s
  }
  remplirComplet(s)
  s.reference = preset === 'a_corriger' ? 'OFF-2026-0139' : 'OFF-2026-0141'
  s.evaluation = {
    active: true,
    criteres: [
      { id: 'e1', libelle: 'Expérience de conduite de projet avec des collectivités', importance: 'essentiel', depuisCritereId: 'c3' },
      { id: 'e2', libelle: 'Maîtrise des dispositifs de rénovation énergétique', importance: 'important', depuisCritereId: 'c4' },
      { id: 'e3', libelle: 'Aisance rédactionnelle', importance: 'complementaire', depuisCritereId: null },
    ],
    premierTri: [{ id: 't1', libelle: 'CV et lettre de motivation présents' }, { id: 't2', libelle: 'Diplôme bac+3 ou équivalent' }],
    tours: '1',
    format: 'presentiel',
    jury: ['julien', 'nadia'],
  }
  if (preset === 'a_valider') {
    s.statut = 'a_valider'
    s.circuit[0]!.statut = 'en_attente'
    s.journal.push({ date: 'Hier', texte: 'Soumise à validation par Camille Moreau' })
  }
  if (preset === 'a_corriger') {
    s.statut = 'a_corriger'
    s.circuit[0]!.statut = 'corrections'
    s.circuit[0]!.date = 'Hier'
    s.offre.conditions = { texte: 'Poste ouvert aux fonctionnaires de catégorie A et aux contractuels. Rémunération : RIFSEEP groupe 3, IFSE selon cotation.', etat: 'redige' }
    s.remarques.push(
      { id: 'r1', auteurId: 'julien', date: 'Hier, 17:42', texte: 'Les conditions de recrutement parlent de « RIFSEEP groupe 3 » : incompréhensible pour un candidat externe. Pouvez-vous reformuler ?', stepId: 'offre', resolue: false },
      { id: 'r2', auteurId: 'julien', date: 'Hier, 17:44', texte: 'Ajouter la maîtrise d\'un tableur dans les critères souhaités.', stepId: 'conditions', resolue: false },
    )
    s.journal.push({ date: 'Avant-hier', texte: 'Soumise à validation par Camille Moreau' }, { date: 'Hier', texte: 'Corrections demandées par Julien Lefèvre' })
  }
  if (preset === 'pret') {
    s.statut = 'validee'
    s.circuit.forEach((e) => {
      e.statut = 'approuve'
      e.date = 'Hier'
    })
    s.journal.push({ date: 'Avant-hier', texte: 'Soumise à validation' }, { date: 'Hier', texte: 'Validée par Julien Lefèvre puis Nadia Benali' })
  }
  return s
}
