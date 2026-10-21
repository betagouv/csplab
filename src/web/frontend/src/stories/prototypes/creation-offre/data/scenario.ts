// Scénario fictif : la DREAL Occitanie remplace une chargée de mission partie en mobilité.
// Camille Moreau (RH de proximité) crée l'offre ; Julien Lefèvre (manager) contribue ;
// la DAR a été validée avant la création de l'offre.

import type { Besoin, Conditions, ContenuDar, EtapeCircuit, Evaluation, OffreState, Origine, Poste, SectionOffre, SectionOffreId } from './types'
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

/** Fiche de poste volontairement incomplète : compétences, profil et environnement manquent. */
export const FICHE_PAIE: SourceFiche = {
  id: 'FP-SG-2026-007',
  libelle: 'Fiche de poste — Gestionnaire de paie',
  detail: 'Mise à jour en septembre 2026 · import SIRH fictif · incomplète',
  besoin: {
    intitule: 'Gestionnaire de paie',
    organisme: 'dreal-occ',
    service: 'Secrétariat général — Bureau des ressources humaines',
    localisation: 'Toulouse (31)',
    categories: ['B'],
    metier: 'm-grh',
    ficheRef: 'FP-SG-2026-007',
  },
  poste: {
    missions: 'Assurer la préparation et le contrôle de la paie des agents titulaires et contractuels de la direction (environ 900 agents), en lien avec le centre de services RH et la DRFiP.',
    activites: [
      'Saisir et contrôler les éléments variables de paie',
      'Calculer les indemnités et les rappels',
      'Répondre aux questions des agents sur leur rémunération',
    ],
  },
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
  FICHE_PAIE,
]

export interface SourceOffre {
  id: string
  libelle: string
  detail: string
}

export const OFFRES_PRECEDENTES: SourceOffre[] = [
  { id: 'OFF-2025-0102', libelle: 'Gestionnaire de paie', detail: 'Publiée en juin 2025 · 18 candidatures · 2 postes pourvus' },
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
    codesPostes: [],
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
  if (organisation === 'sans_validation' || organisation === 'dar_csp') {
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
    darContenu: null,
    notifications: 'chaque',
    modifieLe: 'Aujourd\'hui',
    derniereEtape: '',
    titreAnnonce: '',
    offreDemarree: true,
    contactCandidats: '',
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

export type Preset = 'nouveau' | 'incomplet' | 'a_valider' | 'a_corriger' | 'pret' | 'sans_dar' | 'sans_validation' | 'paie' | 'dar_paie'

export function etatPreset(preset: Preset): OffreState {
  if (preset === 'nouveau') {
    return etatInitial()
  }
  if (preset === 'paie') {
    return etatPaie()
  }
  if (preset === 'dar_paie') {
    const s = etatDarPaie()
    s.offreDemarree = true
    return s
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

/**
 * Scénario principal de l'itération 3 : 3 postes de gestionnaire de paie. La fiche de poste a été
 * reprise hier, puis Camille a été interrompue (appel) : le brouillon a été enregistré automatiquement.
 * La DAR est préparée dans ce même dossier et n'est pas encore soumise.
 */
export function etatPaie(): OffreState {
  const s = etatInitial()
  s.reference = 'OFF-2026-0150'
  depuisFiche(s, FICHE_PAIE)
  s.journal = [
    { date: 'Hier, 15:58', texte: 'Dossier créé par Camille Moreau' },
    { date: 'Hier, 15:58', texte: 'Fiche de poste FP-SG-2026-007 reprise (6 informations)' },
    { date: 'Hier, 16:12', texte: 'Modifications enregistrées automatiquement — Poste', type: 'modification' },
  ]
  s.besoin.nbPostes = '3'
  s.besoin.codesPostes = ['SG-PAIE-012', 'SG-PAIE-015']
  s.besoin.statuts = ['titulaire', 'contractuel']
  s.besoin.darApplicable = 'oui'
  s.besoin.darRef = 'DAR-2026-0331'
  s.besoin.darStatut = 'a_demander'
  s.modifieLe = 'Hier, 16:12'
  s.derniereEtape = 'poste'
  s.circuit[0]!.personneId = 'isabelle'
  s.equipe[1] = { personneId: 'isabelle', acces: 'evaluation' }
  return s
}

/** Ce que la cheffe de bureau RH apporte quand on lui demande de compléter la fiche paie (simulation). */
export const COMPLEMENT_PAIE: Partial<Poste> = {
  competences: ['Réglementation de la rémunération dans la fonction publique', 'Maîtrise d\'un logiciel de paie', 'Rigueur et respect des échéances', 'Sens du service aux agents'],
  profil: 'Première expérience en paie ou en gestion administrative du personnel appréciée. Débutant·e accepté·e avec formation.',
  environnement: 'Bureau des ressources humaines de 12 agents, dont une cellule paie de 5 personnes. Pics d\'activité mensuels liés au calendrier de paie.',
}

// --- Itération 4 : la DAR validée est la source de l'offre ---

/** Texte de la DAR tel que validé : fidèle à la fiche de poste, mais brut pour un candidat (sigles, « ; », abréviations). */
export const DAR_PAIE: ContenuDar = {
  statut: 'validee',
  date: '15 octobre 2026',
  reference: 'DAR-2026-0331',
  validePar: 'helene',
  intitule: 'Gestionnaire de paie',
  service: 'Secrétariat général — Bureau des ressources humaines',
  localisation: 'Toulouse (31)',
  nbPostes: '3',
  codesPostes: ['SG-PAIE-012', 'SG-PAIE-015', 'SG-PAIE-019'],
  categories: ['B'],
  statuts: ['titulaire', 'contractuel'],
  missions: 'Au sein du BRH/SG, le titulaire du poste assure la pré-liquidation de la paie des agents (tit. et contr.) relevant du périmètre de gestion (env. 900 ag.) en lien avec le CSRH et la DRFiP ;\nsaisie et contrôle des EVS dans le SIRH ;\ncalcul des IJ, rappels et précomptes ;\nréponse aux sollicitations des agents ;\nparticipation aux travaux de fiabilisation des données de paie.',
  activites: [],
  competences: ['Connaissance de la réglementation statutaire et indemnitaire (RIFSEEP)', 'Maîtrise des outils bureautiques et du SIRH', 'Rigueur', 'Discrétion'],
  profil: 'Agent de cat. B ou contractuel ; expérience paie souhaitée.',
  environnement: 'BRH : 12 ETP dont cellule paie 5 ETP. Pics d\'activité liés au calendrier de paie (clôture à J-10).',
  conditions: 'Cat. B ; ouvert aux titulaires et aux contractuels (CDD 3 ans).',
}

/** Reformulations proposées pour le scénario paie (fictives, sans IA). */
export const SUGGESTIONS_PAIE: Partial<Record<SectionOffreId, string>> = {
  poste: 'Rejoignez la cellule paie du bureau des ressources humaines : une équipe de 5 personnes qui garantit chaque mois la rémunération des 900 agents de la DREAL Occitanie.',
  missions: 'Vous veillez à ce que chaque agent soit payé juste et à temps :\n- vous préparez et contrôlez les éléments de paie (primes, heures supplémentaires, absences)\n- vous calculez les indemnités et les régularisations\n- vous répondez aux questions des agents sur leur rémunération\n- vous participez à l\'amélioration de la qualité des données de paie',
  profil: 'Vous connaissez les règles de rémunération de la fonction publique, ou vous avez envie de les apprendre. Vous êtes rigoureux·se, discret·e et à l\'aise avec les outils informatiques. Une première expérience en paie est un plus.',
  conditions: 'Poste de catégorie B ouvert aux fonctionnaires et aux contractuels (contrat de 3 ans).',
}

export function suggestionsPour(s: OffreState): Partial<Record<SectionOffreId, string>> {
  return s.besoin.darRef === 'DAR-2026-0331' ? SUGGESTIONS_PAIE : SUGGESTIONS
}

/** Offre préremplie depuis une DAR validée : informations communes et textes bruts repris tels quels. */
function offreDepuisDar(s: OffreState, d: ContenuDar) {
  s.besoin.intitule = d.intitule
  s.besoin.service = d.service
  s.besoin.localisation = d.localisation
  s.besoin.categories = [...(d.categories ?? [])]
  s.besoin.statuts = [...(d.statuts ?? [])]
  s.besoin.typeContrat = d.statuts?.includes('contractuel') ? 'cdd' : ''
  s.besoin.dureeContrat = d.statuts?.includes('contractuel') ? '3 ans' : ''
  s.besoin.nbPostes = d.nbPostes
  s.besoin.codesPostes = [...d.codesPostes]
  s.besoin.darApplicable = 'oui'
  s.besoin.darRef = d.reference ?? ''
  s.besoin.darStatut = d.statut === 'validee' ? 'validee' : 'en_cours'
  s.poste.missions = d.missions
  s.poste.activites = [...d.activites]
  s.poste.competences = [...d.competences]
  s.poste.profil = d.profil ?? ''
  s.poste.environnement = d.environnement ?? ''
  s.darContenu = clone(d)
  s.titreAnnonce = d.intitule
  const reprise = (texte: string): SectionOffre => ({ texte, etat: texte ? 'reprise' : 'vide' })
  s.offre.organisme = reprise(OFFRE_REDIGEE.organisme)
  s.offre.poste = reprise(d.environnement ?? '')
  s.offre.missions = reprise(d.missions)
  s.offre.profil = reprise([d.competences.join(' ; '), d.profil].filter(Boolean).join('\n'))
  s.offre.conditions = reprise(d.conditions ?? '')
  s.offre.pratique = reprise(`Localisation : ${d.localisation}.`)
  // Hypothèse : l'organisation dispose d'un modèle pour les modalités de candidature (absent de la DAR).
  s.offre.candidature = reprise('Candidature (CV et lettre de motivation) à déposer via Choisir le Service Public avant la date limite.')
  s.canaux.forEach((c) => {
    c.selectionne = c.id === 'csp'
  })
  s.startMode = 'besoin'
  s.sourceLibelle = `${d.reference} — ${d.intitule}`
}

export function etatDarPaie(): OffreState {
  const s = etatInitial('dar_csp')
  s.reference = 'OFF-2026-0151'
  offreDepuisDar(s, DAR_PAIE)
  s.offreDemarree = false
  s.besoin.ficheRef = 'FP-SG-2026-007'
  s.equipe[1] = { personneId: 'isabelle', acces: 'evaluation' }
  s.modifieLe = '15 octobre 2026'
  s.journal = [
    { date: '8 octobre 2026, 10:14', texte: 'DAR créée à partir de la fiche de poste FP-SG-2026-007' },
    { date: '9 octobre 2026, 16:40', texte: 'Modifications enregistrées — DAR', type: 'modification' },
    { date: '10 octobre 2026, 09:02', texte: 'DAR DAR-2026-0331 soumise à validation' },
    { date: '15 octobre 2026, 11:30', texte: 'DAR validée par Hélène Robert, telle que soumise' },
  ]
  return s
}

/** DAR soumise, pas encore validée : l'offre peut être préparée, pas créée. */
export function etatDarRh(): OffreState {
  const s = etatInitial('dar_csp')
  s.reference = 'OFF-2026-0152'
  offreDepuisDar(s, {
    ...DAR_PAIE,
    statut: 'soumise',
    date: '17 octobre 2026',
    reference: 'DAR-2026-0322',
    validePar: undefined,
    intitule: 'Gestionnaire RH — carrières',
    nbPostes: '1',
    codesPostes: ['SG-RH-004'],
    missions: 'Gestion administrative des actes de carrière des agents du périmètre (avancements, promotions, mobilités) ; suivi des dossiers individuels ; relation avec le CSRH.',
    competences: ['Réglementation statutaire', 'SIRH', 'Sens du service'],
    profil: 'Agent de cat. B ou contractuel.',
    environnement: 'BRH : 12 ETP.',
  })
  s.offreDemarree = false
  s.modifieLe = '17 octobre 2026'
  s.journal = [
    { date: '16 octobre 2026, 14:05', texte: 'DAR créée à partir de la fiche de poste FP-SG-2026-003' },
    { date: '17 octobre 2026, 10:20', texte: 'DAR DAR-2026-0322 soumise à validation' },
  ]
  return s
}

/** DAR encore en brouillon, préparée depuis une fiche de poste incomplète (itération 3). */
export function etatDarBrouillon(): OffreState {
  const s = etatPaie()
  s.organisation = 'dar_csp'
  s.circuit = []
  s.reference = 'OFF-2026-0153'
  s.besoin.intitule = 'Assistant·e de direction'
  s.besoin.service = 'Secrétariat général — Bureau des ressources humaines'
  s.besoin.darRef = 'DAR-2026-0335'
  s.besoin.metier = 'm-assist'
  s.besoin.nbPostes = '1'
  s.besoin.codesPostes = []
  s.besoin.categories = ['C']
  s.poste.missions = 'Assurer le secrétariat de la secrétaire générale : agenda, accueil téléphonique, courrier, préparation des réunions.'
  s.poste.activites = ['Gérer les agendas', 'Préparer les dossiers de réunion']
  s.offreDemarree = false
  s.journal = [
    { date: 'Hier, 15:58', texte: 'DAR créée à partir de la fiche de poste FP-SG-2026-011' },
    { date: 'Hier, 16:12', texte: 'Modifications enregistrées automatiquement — Poste', type: 'modification' },
  ]
  return s
}

/** Besoin validé sans DAR (renfort contractuel) : l'offre est déjà en rédaction. */
export function etatSansDar(): OffreState {
  const s = etatInitial('dar_csp')
  s.reference = 'OFF-2026-0154'
  s.besoin.intitule = 'Chargé·e de communication interne'
  s.besoin.service = 'Secrétariat général — Bureau des ressources humaines'
  s.besoin.localisation = 'Toulouse (31)'
  s.besoin.categories = ['A']
  s.besoin.statuts = ['contractuel']
  s.besoin.typeContrat = 'cdd'
  s.besoin.dureeContrat = '1 an'
  s.besoin.motif = 'renfort'
  s.besoin.metier = 'm-com'
  s.besoin.darApplicable = 'non'
  s.poste.missions = 'Concevoir et animer la communication interne pendant la réorganisation des services : lettre interne, intranet, événements.'
  s.poste.activites = ['Rédiger la lettre interne mensuelle', 'Animer l\'intranet', 'Organiser les temps d\'échange avec les agents']
  s.poste.competences = ['Rédaction', 'Gestion de projet', 'Outils de publication web']
  s.titreAnnonce = 'Chargé·e de communication interne (CDD 1 an)'
  s.offre.organisme = { texte: OFFRE_REDIGEE.organisme, etat: 'redige' }
  s.offre.poste = { texte: 'Vous accompagnez les 900 agents de la DREAL pendant une année de transformation : il s\'agit de garder chacun informé et impliqué.', etat: 'redige' }
  s.offreDemarree = true
  s.derniereEtape = 'offre'
  s.canaux.forEach((c) => {
    c.selectionne = c.id === 'csp'
  })
  s.modifieLe = 'Hier, 18:05'
  s.journal = [
    { date: '18 octobre 2026, 09:30', texte: 'Besoin déclaré par Camille Moreau (fiche de poste)' },
    { date: '18 octobre 2026, 09:31', texte: 'Validation : sans DAR (renfort temporaire)' },
    { date: 'Hier, 17:40', texte: 'Offre démarrée à partir du besoin' },
    { date: 'Hier, 18:05', texte: 'Modifications enregistrées automatiquement — Offre', type: 'modification' },
  ]
  return s
}
