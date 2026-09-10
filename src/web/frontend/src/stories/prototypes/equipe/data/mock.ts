export type RoleOrganisme = 'gestionnaire' | 'agent'
export type RoleOffre = 'responsable' | 'recruteur' | 'contributeur'
export type StatutCompte = 'actif' | 'en_attente'

export interface ProtoAgent {
  uuid: string
  prenom: string
  nom: string
  email: string
  poste: string
  roleOrganisme: RoleOrganisme
  statut: StatutCompte
  dateCreation: string
  dateDerniereActivite: string | null
}

export interface ProtoMembre {
  agentUuid: string
  roleOffre: RoleOffre
  fonction: string | null
}

export interface ProtoRecrutement {
  uuid: string
  intitule: string
  reference: string
  datePublication: string
  derniereActivite: string
  archive: boolean
  candidatures: { total: number, aTraiter: number, enCours: number }
  membres: ProtoMembre[]
}

export interface ProtoEvenement {
  uuid: string
  date: string
  auteur: string
  libelle: string
  recrutementUuid?: string
}

export type Persona = 'gestionnaire' | 'responsable' | 'recruteur' | 'sans-offre' | 'admin'

export interface PersonaDefinition {
  label: string
  agentUuid: string | null
  nom: string
  role: string
  description: string
}

export const ORGANISME = 'Ministère de la Transition écologique'

export const FONCTIONS = ['BRH', 'CBCM', 'N+1', 'Gestionnaire RH', 'Chef de service', 'Expert métier']

export const ROLE_ORGANISME_LABELS: Record<RoleOrganisme, string> = {
  gestionnaire: 'Gestionnaire',
  agent: 'Agent',
}

export const ROLE_OFFRE_LABELS: Record<RoleOffre, string> = {
  responsable: 'Responsable',
  recruteur: 'Recruteur',
  contributeur: 'Contributeur',
}

export const ROLE_OFFRE_DESCRIPTIONS: Record<RoleOffre, string> = {
  responsable: 'Constitue l\'équipe et pilote le recrutement.',
  recruteur: 'Traite les candidatures et fait avancer les étapes.',
  contributeur: 'Consulte les candidatures et laisse des notes.',
}

let counter = 0

export function nextUuid(prefix = 'proto'): string {
  counter += 1
  return `${prefix}-${String(counter).padStart(4, '0')}`
}

export function daysAgo(days: number, hour = 10): string {
  const date = new Date()
  date.setDate(date.getDate() - days)
  date.setHours(hour, 0, 0, 0)
  return date.toISOString()
}

export function minutesAgo(minutes: number): string {
  return new Date(Date.now() - minutes * 60_000).toISOString()
}

const AGENTS = {
  jules: 'agent-jules',
  marc: 'agent-marc',
  camille: 'agent-camille',
  samir: 'agent-samir',
  sophie: 'agent-sophie',
  claire: 'agent-claire',
  nadia: 'agent-nadia',
  theo: 'agent-theo',
  ines: 'agent-ines',
} as const

export const PERSONAS: Record<Persona, PersonaDefinition> = {
  'gestionnaire': {
    label: 'Gestionnaire',
    agentUuid: AGENTS.jules,
    nom: 'Jules Pommier',
    role: 'Gestionnaire',
    description: 'Administre l\'organisme, attribue les responsables, gère les membres.',
  },
  'responsable': {
    label: 'Responsable',
    agentUuid: AGENTS.camille,
    nom: 'Camille Farce',
    role: 'Agent',
    description: 'Responsable d\'une offre, recruteuse sur une autre.',
  },
  'recruteur': {
    label: 'Recruteur',
    agentUuid: AGENTS.sophie,
    nom: 'Sophie Lambert',
    role: 'Agent',
    description: 'Recruteuse et contributrice, sans responsabilité d\'offre.',
  },
  'sans-offre': {
    label: 'Agent sans offre',
    agentUuid: AGENTS.nadia,
    nom: 'Nadia Roux',
    role: 'Agent',
    description: 'Compte actif, rattaché à aucun recrutement.',
  },
  'admin': {
    label: 'Admin',
    agentUuid: null,
    nom: 'Alix Moreau',
    role: 'Administration CSP',
    description: 'Équipe de la plateforme, tous droits sur l\'organisme.',
  },
}

export interface ProtoScenario {
  agents: ProtoAgent[]
  recrutements: ProtoRecrutement[]
  activitesOffres: ProtoEvenement[]
  journalOrganisme: ProtoEvenement[]
}

export function createScenario(): ProtoScenario {
  const agents: ProtoAgent[] = [
    { uuid: AGENTS.jules, prenom: 'Jules', nom: 'Pommier', email: 'jules.pommier@developpement-durable.gouv.fr', poste: 'Responsable RH', roleOrganisme: 'gestionnaire', statut: 'actif', dateCreation: daysAgo(210), dateDerniereActivite: minutesAgo(12) },
    { uuid: AGENTS.marc, prenom: 'Marc', nom: 'Petit', email: 'marc.petit@developpement-durable.gouv.fr', poste: 'DRH adjoint', roleOrganisme: 'gestionnaire', statut: 'actif', dateCreation: daysAgo(210), dateDerniereActivite: daysAgo(3) },
    { uuid: AGENTS.camille, prenom: 'Camille', nom: 'Farce', email: 'camille.farce@developpement-durable.gouv.fr', poste: 'Cheffe de bureau', roleOrganisme: 'agent', statut: 'actif', dateCreation: daysAgo(180), dateDerniereActivite: daysAgo(0) },
    { uuid: AGENTS.samir, prenom: 'Samir', nom: 'Marlot', email: 'samir.marlot@developpement-durable.gouv.fr', poste: 'Chargé de recrutement', roleOrganisme: 'agent', statut: 'actif', dateCreation: daysAgo(150), dateDerniereActivite: daysAgo(1) },
    { uuid: AGENTS.sophie, prenom: 'Sophie', nom: 'Lambert', email: 'sophie.lambert@developpement-durable.gouv.fr', poste: 'Adjointe au chef de service', roleOrganisme: 'agent', statut: 'actif', dateCreation: daysAgo(120), dateDerniereActivite: daysAgo(2) },
    { uuid: AGENTS.claire, prenom: 'Claire', nom: 'Morel', email: 'claire.morel@developpement-durable.gouv.fr', poste: 'Cheffe de service', roleOrganisme: 'agent', statut: 'actif', dateCreation: daysAgo(120), dateDerniereActivite: daysAgo(6) },
    { uuid: AGENTS.nadia, prenom: 'Nadia', nom: 'Roux', email: 'nadia.roux@developpement-durable.gouv.fr', poste: 'Gestionnaire RH', roleOrganisme: 'agent', statut: 'actif', dateCreation: daysAgo(14), dateDerniereActivite: daysAgo(0) },
    { uuid: AGENTS.theo, prenom: 'Théo', nom: 'Garnier', email: 'theo.garnier@developpement-durable.gouv.fr', poste: 'Chargé de mission', roleOrganisme: 'agent', statut: 'en_attente', dateCreation: daysAgo(5), dateDerniereActivite: null },
    { uuid: AGENTS.ines, prenom: 'Inès', nom: 'Dubois', email: 'ines.dubois@developpement-durable.gouv.fr', poste: 'Juriste', roleOrganisme: 'agent', statut: 'actif', dateCreation: daysAgo(90), dateDerniereActivite: daysAgo(40) },
  ]

  const recrutements: ProtoRecrutement[] = [
    {
      uuid: 'rec-01',
      intitule: 'Chargé·e de mission transition écologique et territoires',
      reference: '2026-MTE-0412',
      datePublication: daysAgo(0),
      derniereActivite: daysAgo(0),
      archive: false,
      candidatures: { total: 19, aTraiter: 12, enCours: 7 },
      membres: [],
    },
    {
      uuid: 'rec-02',
      intitule: 'Chef·fe de projet mobilité durable',
      reference: '2026-MTE-0398',
      datePublication: daysAgo(1),
      derniereActivite: daysAgo(0),
      archive: false,
      candidatures: { total: 24, aTraiter: 6, enCours: 11 },
      membres: [
        { agentUuid: AGENTS.camille, roleOffre: 'responsable', fonction: 'BRH' },
        { agentUuid: AGENTS.samir, roleOffre: 'recruteur', fonction: 'CBCM' },
        { agentUuid: AGENTS.theo, roleOffre: 'contributeur', fonction: 'N+1' },
      ],
    },
    {
      uuid: 'rec-03',
      intitule: 'Instructeur·rice des autorisations environnementales',
      reference: '2026-MTE-0371',
      datePublication: daysAgo(2),
      derniereActivite: daysAgo(2),
      archive: false,
      candidatures: { total: 8, aTraiter: 3, enCours: 4 },
      membres: [
        { agentUuid: AGENTS.claire, roleOffre: 'responsable', fonction: 'Chef de service' },
        { agentUuid: AGENTS.ines, roleOffre: 'recruteur', fonction: null },
        { agentUuid: AGENTS.sophie, roleOffre: 'contributeur', fonction: 'Expert métier' },
      ],
    },
    {
      uuid: 'rec-04',
      intitule: 'Responsable d\'unité biodiversité',
      reference: '2026-MTE-0355',
      datePublication: daysAgo(2),
      derniereActivite: daysAgo(2),
      archive: false,
      candidatures: { total: 31, aTraiter: 9, enCours: 15 },
      membres: [
        { agentUuid: AGENTS.claire, roleOffre: 'responsable', fonction: 'Chef de service' },
        { agentUuid: AGENTS.camille, roleOffre: 'recruteur', fonction: 'BRH' },
        { agentUuid: AGENTS.sophie, roleOffre: 'recruteur', fonction: null },
      ],
    },
    {
      uuid: 'rec-05',
      intitule: 'Chargé·e d\'études risques naturels et adaptation au changement climatique',
      reference: '2026-MTE-0340',
      datePublication: daysAgo(2),
      derniereActivite: daysAgo(2),
      archive: false,
      candidatures: { total: 12, aTraiter: 12, enCours: 0 },
      membres: [
        { agentUuid: AGENTS.samir, roleOffre: 'responsable', fonction: 'CBCM' },
        { agentUuid: AGENTS.ines, roleOffre: 'contributeur', fonction: null },
      ],
    },
    {
      uuid: 'rec-06',
      intitule: 'Chef·fe de projet données environnementales',
      reference: '2026-MTE-0322',
      datePublication: daysAgo(22),
      derniereActivite: daysAgo(3),
      archive: false,
      candidatures: { total: 5, aTraiter: 5, enCours: 0 },
      membres: [],
    },
    {
      uuid: 'rec-07',
      intitule: 'Gestionnaire de paie',
      reference: '2025-MTE-0918',
      datePublication: daysAgo(140),
      derniereActivite: daysAgo(35),
      archive: true,
      candidatures: { total: 42, aTraiter: 0, enCours: 0 },
      membres: [
        { agentUuid: AGENTS.jules, roleOffre: 'responsable', fonction: 'Gestionnaire RH' },
      ],
    },
    {
      uuid: 'rec-08',
      intitule: 'Assistant·e de direction',
      reference: '2025-MTE-0871',
      datePublication: daysAgo(190),
      derniereActivite: daysAgo(61),
      archive: true,
      candidatures: { total: 27, aTraiter: 0, enCours: 0 },
      membres: [
        { agentUuid: AGENTS.claire, roleOffre: 'responsable', fonction: null },
      ],
    },
  ]

  const activitesOffres: ProtoEvenement[] = [
    { uuid: nextUuid('evt'), recrutementUuid: 'rec-02', date: daysAgo(1, 9), auteur: 'Jules Pommier', libelle: 'a désigné Camille Farce responsable de l\'offre' },
    { uuid: nextUuid('evt'), recrutementUuid: 'rec-02', date: daysAgo(1, 11), auteur: 'Camille Farce', libelle: 'a ajouté Samir Marlot comme recruteur' },
    { uuid: nextUuid('evt'), recrutementUuid: 'rec-02', date: daysAgo(0, 9), auteur: 'Camille Farce', libelle: 'a invité Théo Garnier comme contributeur' },
    { uuid: nextUuid('evt'), recrutementUuid: 'rec-03', date: daysAgo(2, 9), auteur: 'Marc Petit', libelle: 'a désigné Claire Morel responsable de l\'offre' },
    { uuid: nextUuid('evt'), recrutementUuid: 'rec-03', date: daysAgo(2, 14), auteur: 'Claire Morel', libelle: 'a ajouté Inès Dubois comme recruteuse' },
    { uuid: nextUuid('evt'), recrutementUuid: 'rec-03', date: daysAgo(2, 14), auteur: 'Claire Morel', libelle: 'a ajouté Sophie Lambert comme contributrice' },
    { uuid: nextUuid('evt'), recrutementUuid: 'rec-04', date: daysAgo(2, 10), auteur: 'Jules Pommier', libelle: 'a désigné Claire Morel responsable de l\'offre' },
    { uuid: nextUuid('evt'), recrutementUuid: 'rec-04', date: daysAgo(2, 15), auteur: 'Claire Morel', libelle: 'a ajouté Camille Farce et Sophie Lambert comme recruteuses' },
    { uuid: nextUuid('evt'), recrutementUuid: 'rec-05', date: daysAgo(2, 10), auteur: 'Jules Pommier', libelle: 'a désigné Samir Marlot responsable de l\'offre' },
    { uuid: nextUuid('evt'), recrutementUuid: 'rec-05', date: daysAgo(2, 16), auteur: 'Samir Marlot', libelle: 'a ajouté Inès Dubois comme contributrice' },
  ]

  const journalOrganisme: ProtoEvenement[] = [
    { uuid: nextUuid('log'), date: daysAgo(14, 9), auteur: 'Jules Pommier', libelle: 'a créé le compte de Nadia Roux (agent)' },
    { uuid: nextUuid('log'), date: daysAgo(5, 16), auteur: 'Camille Farce', libelle: 'a créé le compte de Théo Garnier (agent) depuis l\'offre « Chef·fe de projet mobilité durable »' },
    { uuid: nextUuid('log'), date: daysAgo(3, 11), auteur: 'Marc Petit', libelle: 'a consulté la liste des membres' },
  ]

  return { agents, recrutements, activitesOffres, journalOrganisme }
}
