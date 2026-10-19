import type { Etiquette, WithEtiquettes } from '@/features/candidatures/etiquettes'
import type {
  Activite,
  Candidature,
  CandidatureDetail,
  CandidatureListe,
  DocumentListe,
  MotifRefusOption,
  Note,
  RecrutementDetailKanban,
} from '@/features/candidatures/types'
import { DEMO_CANDIDATURE, DEMO_RECRUTEMENT_INTITULE, DEMO_RECRUTEMENT_UUID, DEMO_UTILISATEUR, demoDate } from '@/api/__mocks__/demo'
import { DEMO_ETAPES } from '@/features/recrutements/__mocks__/demo'

export const ETIQUETTES_CANDIDATURE = {
  titulaire: { libelle: 'Titulaire', couleur: 'blue' },
  contractuel: { libelle: 'Contractuel', couleur: 'yellow' },
  mobilite: { libelle: 'Mobilité interne', couleur: 'teal' },
  rappeler: { libelle: 'À rappeler', couleur: 'orange' },
  vivier: { libelle: 'Vivier', couleur: 'green' },
  senior: { libelle: 'Profil senior', couleur: 'purple' },
  apprentissage: { libelle: 'Apprentissage', couleur: 'pink' },
  prioritaire: { libelle: 'Prioritaire', couleur: 'red' },
  teletravail: { libelle: 'Télétravail souhaité', couleur: 'brown' },
  delai: { libelle: 'Hors délai', couleur: 'grey' },
  laureate: { libelle: 'Lauréate concours externe', couleur: 'purple' },
  encadrement: { libelle: 'Expérience en encadrement', couleur: 'orange' },
} satisfies Record<string, Etiquette>

export const ETIQUETTES_NOTE = {
  compteRendu: { libelle: 'Compte rendu d\'entretien', couleur: 'blue' },
  validation: { libelle: 'Validation', couleur: 'green' },
  vigilance: { libelle: 'Point de vigilance', couleur: 'orange' },
  information: { libelle: 'Information', couleur: 'grey' },
  avis: { libelle: 'Avis du service', couleur: 'purple' },
} satisfies Record<string, Etiquette>

export const ETIQUETTES_EQUIPE = {
  gestionnaire: { libelle: 'Gestionnaire RH', couleur: 'teal' },
  manager: { libelle: 'Manager', couleur: 'purple' },
  expert: { libelle: 'Expert métier', couleur: 'yellow' },
  assistant: { libelle: 'Assistant RH', couleur: 'pink' },
  jury: { libelle: 'Membre du jury', couleur: 'brown' },
} satisfies Record<string, Etiquette>

interface DemoCandidat {
  prenom: string
  nom: string
  etape: number
  jours: number
  etiquettes: Etiquette[]
}

const E = ETIQUETTES_CANDIDATURE

const CANDIDATS: DemoCandidat[] = [
  { prenom: 'Inès', nom: 'Moreau', etape: 0, jours: 1, etiquettes: [E.mobilite, E.titulaire] },
  { prenom: 'Thomas', nom: 'Leroy', etape: 0, jours: 1, etiquettes: [E.contractuel] },
  { prenom: DEMO_CANDIDATURE.prenom, nom: DEMO_CANDIDATURE.nom, etape: 0, jours: 2, etiquettes: [E.prioritaire, E.laureate, E.titulaire, E.teletravail, E.rappeler] },
  { prenom: 'Mehdi', nom: 'Benali', etape: 0, jours: 2, etiquettes: [] },
  { prenom: 'Sophie', nom: 'Garnier', etape: 0, jours: 3, etiquettes: [E.encadrement, E.vivier] },
  { prenom: 'Lucas', nom: 'Petit', etape: 0, jours: 3, etiquettes: [] },
  { prenom: 'Aïcha', nom: 'Diallo', etape: 0, jours: 4, etiquettes: [E.laureate] },
  { prenom: 'Antoine', nom: 'Mercier', etape: 0, jours: 4, etiquettes: [E.delai] },
  { prenom: 'Julie', nom: 'Robin', etape: 0, jours: 5, etiquettes: [E.teletravail, E.rappeler] },
  { prenom: 'Nicolas', nom: 'Faure', etape: 0, jours: 5, etiquettes: [E.contractuel, E.vivier] },
  { prenom: 'Manon', nom: 'Rousseau', etape: 0, jours: 6, etiquettes: [] },
  { prenom: 'Karim', nom: 'Saïdi', etape: 0, jours: 6, etiquettes: [E.titulaire, E.mobilite, E.senior] },
  { prenom: 'Léa', nom: 'Chevalier', etape: 0, jours: 7, etiquettes: [E.apprentissage] },
  { prenom: 'Hugo', nom: 'Lambert', etape: 0, jours: 8, etiquettes: [] },
  { prenom: 'Chloé', nom: 'Bonnet', etape: 0, jours: 8, etiquettes: [E.prioritaire, E.laureate] },
  { prenom: 'Romain', nom: 'Gauthier', etape: 0, jours: 9, etiquettes: [E.delai, E.contractuel] },
  { prenom: 'Sarah', nom: 'Benhamou', etape: 0, jours: 10, etiquettes: [E.encadrement] },
  { prenom: 'Maxime', nom: 'Perrin', etape: 0, jours: 11, etiquettes: [] },
  { prenom: 'Élodie', nom: 'Marchand', etape: 0, jours: 12, etiquettes: [E.vivier, E.teletravail] },
  { prenom: 'Paul', nom: 'Dumas', etape: 0, jours: 13, etiquettes: [E.titulaire] },
  { prenom: 'Lucie', nom: 'Morel', etape: 1, jours: 14, etiquettes: [E.titulaire, E.senior] },
  { prenom: 'Nadia', nom: 'Haddad', etape: 1, jours: 15, etiquettes: [E.mobilite, E.prioritaire, E.teletravail] },
  { prenom: 'Julien', nom: 'Roux', etape: 1, jours: 15, etiquettes: [E.contractuel, E.rappeler] },
  { prenom: 'Emma', nom: 'Girard', etape: 1, jours: 16, etiquettes: [E.apprentissage, E.delai, E.vivier] },
  { prenom: 'Camille', nom: 'Martin', etape: 2, jours: 17, etiquettes: [E.laureate, E.titulaire] },
  { prenom: 'Yanis', nom: 'Boucher', etape: 2, jours: 18, etiquettes: [] },
  { prenom: 'Pauline', nom: 'Lemoine', etape: 2, jours: 18, etiquettes: [E.mobilite] },
  { prenom: 'Olivier', nom: 'Fabre', etape: 3, jours: 19, etiquettes: [E.senior, E.vivier] },
  { prenom: 'Fatou', nom: 'Ndiaye', etape: 3, jours: 20, etiquettes: [E.encadrement, E.prioritaire] },
  { prenom: 'Marion', nom: 'Leclerc', etape: 4, jours: 21, etiquettes: [E.titulaire] },
  { prenom: 'Damien', nom: 'Caron', etape: 5, jours: 21, etiquettes: [E.delai] },
  { prenom: 'Laura', nom: 'Vidal', etape: 5, jours: 22, etiquettes: [] },
]

function demoUuid(prefix: string, index: number): string {
  return `${prefix}0000000-0000-4000-8000-${String(index + 1).padStart(12, '0')}`
}

function emailOf({ prenom, nom }: DemoCandidat): string {
  return `${prenom}.${nom}@example.fr`.normalize('NFD').replace(/\p{Diacritic}/gu, '').toLowerCase()
}

const CANDIDATURES: (Candidature & WithEtiquettes)[] = CANDIDATS.map((candidat, index) => ({
  uuid: demoUuid('d', index),
  date_soumission: demoDate(candidat.jours, 8 + (index % 9), (index * 7) % 60),
  date_derniere_activite: demoDate(Math.max(1, candidat.jours - 1), 15, 30),
  candidat: { uuid: demoUuid('e', index), prenom: candidat.prenom, nom: candidat.nom },
  etiquettes: candidat.etiquettes,
  unread_conversations: 0,
}))

const etapeOfCandidature = new Map(CANDIDATURES.map((candidature, index) => [candidature.uuid, DEMO_ETAPES[CANDIDATS[index]!.etape]!]))

export function moveDemoCandidatures(candidatureUuids: string[], etapeUuid: string): void {
  const etape = DEMO_ETAPES.find(({ uuid }) => uuid === etapeUuid)
  if (etape) {
    candidatureUuids.forEach(uuid => etapeOfCandidature.set(uuid, etape))
  }
}

export function demoKanban(): RecrutementDetailKanban {
  return {
    uuid: DEMO_RECRUTEMENT_UUID,
    etapes: DEMO_ETAPES.map(etape => ({
      ...etape,
      candidatures: CANDIDATURES.filter(({ uuid }) => etapeOfCandidature.get(uuid) === etape),
    })),
  }
}

export function demoListe(): (CandidatureListe & WithEtiquettes)[] {
  return CANDIDATURES.map(candidature => ({ ...candidature, etape: etapeOfCandidature.get(candidature.uuid)! }))
}

export function demoCandidatureDetail(candidatureUuid: string): (CandidatureDetail & WithEtiquettes) | null {
  const index = CANDIDATURES.findIndex(({ uuid }) => uuid === candidatureUuid)
  const candidature = CANDIDATURES[index]
  if (!candidature) {
    return null
  }
  const etape = etapeOfCandidature.get(candidatureUuid)!
  return {
    uuid: candidature.uuid,
    candidat: { ...candidature.candidat, email: emailOf(CANDIDATS[index]!) },
    recrutement_intitule: DEMO_RECRUTEMENT_INTITULE,
    etapes: DEMO_ETAPES.map(({ uuid, nom }) => ({ uuid, nom })),
    etape_actuelle: { uuid: etape.uuid, nom: etape.nom },
    date_candidature: candidature.date_soumission,
    date_derniere_maj_candidat: null,
    date_derniere_maj_recruteur: candidature.date_derniere_activite,
    document_uuid: demoUuid('9', index * 3),
    navigation_candidature_uuids: CANDIDATURES.filter(({ uuid }) => etapeOfCandidature.get(uuid) === etape).map(({ uuid }) => uuid),
    etiquettes: candidature.etiquettes,
  }
}

export function demoDocuments(candidatureUuid: string): DocumentListe[] {
  const index = CANDIDATURES.findIndex(({ uuid }) => uuid === candidatureUuid)
  const candidature = CANDIDATURES[index]
  if (!candidature) {
    return []
  }
  const { candidat, date_soumission } = candidature
  const depot = { depose_par_uuid: candidat.uuid, depose_par: `${candidat.prenom} ${candidat.nom}`, depose_le: date_soumission, content_type: 'application/pdf' }
  return [
    { ...depot, uuid: demoUuid('9', index * 3), type: 'cv', nom_original: `CV_${candidat.prenom}_${candidat.nom}.pdf`, taille: 184_320 },
    { ...depot, uuid: demoUuid('9', index * 3 + 1), type: 'lettre_motivation', nom_original: 'Lettre_de_motivation.pdf', taille: 96_256 },
    { ...depot, uuid: demoUuid('9', index * 3 + 2), type: 'piece_justificative', nom_original: 'Arrete_de_nomination.pdf', taille: 152_064 },
  ]
}

const N = ETIQUETTES_NOTE

const AUTEURS = {
  utilisateur: { publie_par_id: 'f1000000-0000-4000-8000-000000000001', publie_par_prenom: DEMO_UTILISATEUR.prenom, publie_par_nom: DEMO_UTILISATEUR.nom },
  julien: { publie_par_id: 'f1000000-0000-4000-8000-000000000002', publie_par_prenom: 'Julien', publie_par_nom: 'Moreau' },
  sophie: { publie_par_id: 'f1000000-0000-4000-8000-000000000003', publie_par_prenom: 'Sophie', publie_par_nom: 'Lefèvre' },
}

const notesByCandidature = new Map<string, (Note & WithEtiquettes)[]>([[DEMO_CANDIDATURE.uuid, [
  {
    ...AUTEURS.utilisateur,
    uuid: 'f0000000-0000-4000-8000-000000000001',
    candidature_id: DEMO_CANDIDATURE.uuid,
    publie_le: demoDate(1, 16, 40),
    message: 'Échange téléphonique de vingt minutes. Bonne connaissance des procédures de recrutement et du statut de la fonction publique d\'État. Disponible en janvier si son employeur actuel accepte la date de départ.',
    etiquettes: [N.compteRendu, N.vigilance],
  },
  {
    ...AUTEURS.julien,
    uuid: 'f0000000-0000-4000-8000-000000000002',
    candidature_id: DEMO_CANDIDATURE.uuid,
    publie_le: demoDate(1, 10, 5),
    message: 'Profil validé par le service. Proposer un entretien avec la cheffe du bureau de la gestion administrative la semaine prochaine.',
    etiquettes: [N.validation],
  },
  {
    ...AUTEURS.sophie,
    uuid: 'f0000000-0000-4000-8000-000000000003',
    candidature_id: DEMO_CANDIDATURE.uuid,
    publie_le: demoDate(2, 11, 40),
    message: 'Candidature transmise par la conseillère mobilité carrière de la plateforme régionale. Les pièces du dossier sont complètes.',
    etiquettes: [N.information],
  },
  {
    ...AUTEURS.julien,
    uuid: 'f0000000-0000-4000-8000-000000000004',
    candidature_id: DEMO_CANDIDATURE.uuid,
    publie_le: demoDate(2, 15, 30),
    message: 'Premier tri : deux ans d\'expérience en gestion de la paie dans une collectivité territoriale.',
    etiquettes: [],
  },
]]])

export function demoNotes(candidatureUuid: string): (Note & WithEtiquettes)[] {
  return [...notesByCandidature.get(candidatureUuid) ?? []].sort((a, b) => b.publie_le.localeCompare(a.publie_le))
}

export function addDemoNote(candidatureUuid: string, message: string): void {
  notesByCandidature.set(candidatureUuid, [{
    ...AUTEURS.utilisateur,
    uuid: crypto.randomUUID(),
    candidature_id: candidatureUuid,
    publie_le: new Date().toISOString(),
    message,
    etiquettes: [],
  }, ...demoNotes(candidatureUuid)])
}

export function demoActivites(candidatureUuid: string): Activite[] {
  const candidature = CANDIDATURES.find(({ uuid }) => uuid === candidatureUuid)
  if (!candidature) {
    return []
  }
  const recue: Activite = { utilisateur_id: candidature.candidat.uuid, utilisateur_prenom: '', utilisateur_nom: '', occurred_at: candidature.date_soumission, event_name: 'CandidatureRecue' }
  return [
    ...demoNotes(candidatureUuid).map(note => ({
      utilisateur_id: note.publie_par_id,
      utilisateur_prenom: note.publie_par_prenom,
      utilisateur_nom: note.publie_par_nom,
      occurred_at: note.publie_le,
      event_name: 'NoteAjoutee',
    })),
    ...(etapeOfCandidature.get(candidatureUuid) === DEMO_ETAPES[0]
      ? []
      : [{ utilisateur_id: AUTEURS.julien.publie_par_id, utilisateur_prenom: 'Julien', utilisateur_nom: 'Moreau', occurred_at: candidature.date_derniere_activite, event_name: 'CandidatureEtapeModifiee' }]),
    recue,
  ].sort((a, b) => b.occurred_at.localeCompare(a.occurred_at))
}

export const DEMO_MOTIFS_REFUS: MotifRefusOption[] = [
  { value: 'experience_insuffisante', label: 'Expérience insuffisante' },
  { value: 'competences_techniques_insuffisantes', label: 'Compétences techniques insuffisantes' },
  { value: 'condition_mobilite_non_remplie', label: 'Condition de mobilité non remplie' },
  { value: 'disponibilite', label: 'Disponibilité' },
  { value: 'autre', label: 'Autre' },
]
