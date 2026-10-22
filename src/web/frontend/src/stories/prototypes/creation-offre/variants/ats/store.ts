// Modèle et données de la variante « ATS — fiches et offres ».
// Deux objets distincts et reliés : la fiche de poste (référentiel durable) et l'offre d'emploi
// (opération de recrutement + annonce). Une offre est toujours rattachée à une fiche.
// Tout est local et fictif ; conservé pendant la session (sessionStorage).

import { reactive } from 'vue'

export type OrigineFiche = 'ats' | 'sirh' | 'document'
export type EtatOffre = 'redaction' | 'validation' | 'a_publier' | 'publiee' | 'archivee'
export type OrigineContenu = 'fiche' | 'fichier' | 'manuel' | 'duplication'

export interface Evenement {
  date: string
  texte: string
}

export interface Fiche {
  id: string
  intitule: string
  service: string
  localisation: string
  categories: string[]
  statuts: string[]
  codePoste: string
  missions: string
  activites: string[]
  competences: string[]
  profil: string
  environnement: string
  teletravail: string
  conditions: string
  origine: OrigineFiche
  /** Fiche récupérée d'un SIRH (simulation) : référence et dernière synchronisation. */
  sirh?: { reference: string, synchroLe: string }
  /** Fiche issue d'un document ajouté (simulation). */
  document?: { nom: string, ajouteLe: string }
  statut: 'active' | 'archivee'
  modifieLe: string
  historique: Evenement[]
}

/** Formulaire de DAR, prérempli à partir de la fiche de poste. Figé à la soumission. */
export interface FormulaireDar {
  entite: string
  type: string
  employeur: string
  descriptifEmployeur: string
  descriptifService: string
  intitule: string
  categorie: string
  nbPostes: string
  description: string
  motif: string
  piecesJointes: string[]
}

export interface Offre {
  id: string
  ficheId: string
  etat: EtatOffre
  origineContenu: OrigineContenu
  sourceOffreId?: string
  nbPostes: string
  /** Fixé par les paramètres de l'organisme, jamais choisi à la création de l'offre. */
  dar: 'requise' | 'non_requise'
  darStatut?: 'brouillon' | 'soumise' | 'validee' | 'refusee'
  darRef?: string
  darSoumiseLe?: string
  darValideeLe?: string
  darForm?: FormulaireDar
  remarqueDar?: string
  /** Publication par support : état et dates (simulées). */
  publications: Record<string, { etat: 'publiee' | 'arretee', debut: string, fin: string }>
  // Contenu éditorial de l'annonce
  titre: string
  presentation: string
  missions: string
  profil: string
  indispensables: string[]
  souhaitables: string[]
  modalites: string
  lieu: string
  teletravail: string
  conditions: string
  remuneration: string
  dateLimite: string
  contact: string
  canaux: string[]
  notifications: 'chaque' | 'cinq' | 'quotidien' | 'aucune'
  creeLe: string
  modifieLe: string
  publieeLe?: string
  historique: Evenement[]
}

export const LIBELLES_ETAT: Record<EtatOffre, string> = {
  redaction: 'En cours de rédaction',
  validation: 'En cours de validation (DAR)',
  a_publier: 'À publier',
  publiee: 'Publiée',
  archivee: 'Archivée',
}

export const LIBELLES_ORIGINE: Record<OrigineFiche, string> = {
  ats: 'Créée dans l\'ATS',
  sirh: 'Récupérée du SIRH',
  document: 'Issue d\'un document',
}

export const LIBELLES_CONTENU: Record<OrigineContenu, string> = {
  fiche: 'Depuis la fiche de poste',
  fichier: 'Depuis un fichier',
  manuel: 'Saisie manuelle',
  duplication: 'Duplication d\'une offre',
}

export const CANAUX_DIFFUSION = [
  { id: 'csp', groupe: 'Sites web', nom: 'Choisir le Service Public', detail: 'Support de publication maître', maitre: true },
  { id: 'intranet', groupe: 'Sites web', nom: 'Intranet ministériel', detail: 'Visible des agents', maitre: false },
  { id: 'jobboard', groupe: 'Jobboards', nom: 'Jobboard emploi public (fictif)', detail: 'Diffusion ciblée', maitre: false },
  { id: 'multi', groupe: 'Multi-diffuseurs', nom: 'Multi-diffuseur (fictif)', detail: 'Relais vers plusieurs sites d\'emploi', maitre: false },
]

/** Paramètres de l'organisme (simulés). La nécessité d'une DAR y est définie une fois pour toutes. */
export interface Organisme {
  nom: string
  darObligatoire: boolean
  entite: string
  typeDar: string
  valideur: string
}

export const ENTITES = [
  'Premier ministre › Secrétariat général pour l\'investissement (SGPI)',
  'Premier ministre › Direction des services administratifs et financiers (DSAF)',
  'Premier ministre › Direction interministérielle du numérique (DINUM)',
  'Transition écologique › DREAL Occitanie',
]
export const TYPES_DAR = ['Formulaire DAR', 'Formulaire de demande d\'autorisation']

// --- Données fictives ---

function fichesInitiales(): Fiche[] {
  const base = { statut: 'active' as const, teletravail: '', conditions: '', environnement: '', codePoste: '' }
  return [
    {
      ...base,
      id: 'FP-SG-2026-007',
      intitule: 'Gestionnaire de paie',
      service: 'Secrétariat général — Bureau des ressources humaines',
      localisation: 'Toulouse (31)',
      categories: ['B'],
      statuts: ['titulaire', 'contractuel'],
      codePoste: 'SG-PAIE',
      missions: 'Au sein du BRH, le titulaire assure la pré-liquidation de la paie des agents (tit. et contr.) relevant du périmètre de gestion (env. 900 ag.) en lien avec le CSRH et la DRFiP.',
      activites: ['Saisie et contrôle des EVS dans le SIRH', 'Calcul des IJ, rappels et précomptes', 'Réponse aux sollicitations des agents', 'Participation à la fiabilisation des données de paie'],
      competences: ['Réglementation statutaire et indemnitaire (RIFSEEP)', 'Maîtrise d\'un logiciel de paie', 'Rigueur', 'Discrétion'],
      profil: 'Agent de cat. B ou contractuel ; expérience paie souhaitée.',
      environnement: 'BRH : 12 ETP dont cellule paie 5 ETP. Pics d\'activité liés au calendrier de paie.',
      teletravail: '1 jour par semaine',
      origine: 'ats',
      modifieLe: '2 septembre 2026',
      historique: [{ date: '12 mars 2026', texte: 'Fiche créée dans l\'ATS par Camille Moreau' }, { date: '2 septembre 2026', texte: 'Fiche modifiée — compétences' }],
    },
    {
      ...base,
      id: 'FP-SIRH-48213',
      intitule: 'Chargé·e de recrutement',
      service: 'Secrétariat général — Bureau des ressources humaines',
      localisation: 'Toulouse (31)',
      categories: ['A'],
      statuts: ['titulaire', 'contractuel'],
      codePoste: 'RH-RECR-02',
      missions: 'Piloter les recrutements de la direction : définition des besoins avec les managers, rédaction et diffusion des offres, présélection, organisation des jurys.',
      activites: ['Accompagner les managers dans la définition du besoin', 'Diffuser les offres', 'Présélectionner les candidatures', 'Organiser les entretiens et jurys'],
      competences: ['Techniques de recrutement', 'Statut de la fonction publique', 'Conduite d\'entretien'],
      profil: 'Expérience en recrutement public ou privé.',
      environnement: 'Cellule recrutement de 3 personnes.',
      origine: 'sirh',
      sirh: { reference: 'SIRH-RH-48213', synchroLe: '20 octobre 2026' },
      modifieLe: '20 octobre 2026',
      historique: [{ date: '4 février 2025', texte: 'Fiche récupérée du SIRH ministériel (simulation)' }, { date: '20 octobre 2026', texte: 'Synchronisation SIRH — aucun changement' }],
    },
    {
      ...base,
      id: 'FP-DOC-2026-002',
      intitule: 'Chef·fe de projet numérique',
      service: 'Secrétariat général — Pôle numérique',
      localisation: 'Montpellier (34)',
      categories: ['A'],
      statuts: ['titulaire', 'contractuel'],
      codePoste: 'NUM-CPN',
      missions: 'Conduire les projets de dématérialisation des démarches de la direction, de l\'expression du besoin à la mise en service, en lien avec les métiers et les prestataires.',
      activites: ['Recueillir les besoins des services', 'Piloter les prestataires', 'Accompagner les utilisateurs'],
      competences: ['Gestion de projet agile', 'Connaissance des démarches en ligne', 'Animation de réunions'],
      profil: '',
      teletravail: '2 jours par semaine',
      origine: 'document',
      document: { nom: 'fiche_poste_CPN_v3.docx', ajouteLe: '14 octobre 2026' },
      modifieLe: '14 octobre 2026',
      historique: [{ date: '14 octobre 2026', texte: 'Fiche constituée à partir du document fiche_poste_CPN_v3.docx (extraction simulée)' }],
    },
    {
      ...base,
      id: 'FP-SG-2025-031',
      intitule: 'Assistant·e administratif·ve',
      service: 'Service Aménagement',
      localisation: 'Toulouse (31)',
      categories: ['C'],
      statuts: ['titulaire', 'contractuel'],
      codePoste: 'SA-ASSIST',
      missions: 'Assurer l\'accueil et le secrétariat du service : courrier, agendas, préparation des dossiers et des réunions.',
      activites: ['Gérer le courrier et les agendas', 'Préparer les réunions', 'Accueillir le public'],
      competences: ['Outils bureautiques', 'Organisation', 'Sens de l\'accueil'],
      profil: 'Expérience en secrétariat appréciée.',
      origine: 'ats',
      modifieLe: '3 juin 2025',
      historique: [{ date: '3 juin 2025', texte: 'Fiche créée dans l\'ATS par Nadia Benali' }],
    },
    {
      ...base,
      id: 'FP-SG-2024-031',
      intitule: 'Responsable informatique',
      service: 'Secrétariat général — Pôle numérique',
      localisation: 'Toulouse (31)',
      categories: ['A'],
      statuts: ['titulaire', 'contractuel'],
      codePoste: 'NUM-RESP',
      missions: 'Encadrer le pôle numérique (6 agents) et garantir le bon fonctionnement du système d\'information de la direction.',
      activites: ['Encadrer le pôle', 'Piloter le budget informatique', 'Assurer la sécurité du système d\'information'],
      competences: ['Management', 'Architecture des systèmes d\'information', 'Sécurité informatique'],
      profil: '',
      origine: 'sirh',
      sirh: { reference: 'SIRH-NUM-30117', synchroLe: '20 octobre 2026' },
      modifieLe: '3 avril 2026',
      historique: [{ date: '3 avril 2026', texte: 'Fiche récupérée du SIRH ministériel (simulation)' }],
    },
    {
      ...base,
      id: 'FP-SG-2023-010',
      intitule: 'Chargé·e d\'accueil',
      service: 'Secrétariat général',
      localisation: 'Toulouse (31)',
      categories: ['C'],
      statuts: ['titulaire'],
      codePoste: 'SG-ACC',
      missions: 'Accueillir et orienter les visiteurs et les appels.',
      activites: [],
      competences: ['Sens de l\'accueil'],
      profil: '',
      origine: 'ats',
      statut: 'archivee',
      modifieLe: '10 janvier 2026',
      historique: [{ date: '2 mai 2023', texte: 'Fiche créée dans l\'ATS' }, { date: '10 janvier 2026', texte: 'Fiche archivée (accueil mutualisé)' }],
    },
  ]
}

const VIDE = {
  presentation: '',
  missions: '',
  profil: '',
  indispensables: [] as string[],
  souhaitables: [] as string[],
  modalites: '',
  lieu: '',
  teletravail: '',
  conditions: '',
  remuneration: '',
  dateLimite: '',
  contact: '',
  canaux: ['csp'],
  notifications: 'chaque' as const,
  publications: {} as Offre['publications'],
}

function offresInitiales(f: Fiche[]): Offre[] {
  const fiche = (id: string) => f.find(x => x.id === id)!
  const paie = { ...contenuDepuisFiche(fiche('FP-SG-2026-007')), titre: 'Gestionnaire de paie' }
  return [
    {
      ...VIDE,
      ...paie,
      id: 'OFF-2026-0151',
      ficheId: 'FP-SG-2026-007',
      etat: 'redaction',
      origineContenu: 'fiche',
      nbPostes: '3',
      dar: 'requise',
      creeLe: 'Hier',
      modifieLe: 'Hier, 16:12',
      historique: [{ date: 'Hier, 15:58', texte: 'Offre créée depuis la fiche FP-SG-2026-007 (3 postes)' }, { date: 'Hier, 16:12', texte: 'Brouillon enregistré' }],
    },
    {
      ...VIDE,
      ...contenuDepuisFiche(fiche('FP-SIRH-48213')),
      titre: 'Chargé·e de recrutement',
      presentation: 'Vous rejoignez la cellule recrutement de la DREAL Occitanie et accompagnez les managers pour attirer les bons profils.',
      id: 'OFF-2026-0148',
      ficheId: 'FP-SIRH-48213',
      etat: 'validation',
      origineContenu: 'fiche',
      nbPostes: '1',
      dar: 'requise',
      darRef: 'DAR-2026-0330',
      darStatut: 'soumise',
      darSoumiseLe: '17 octobre 2026',
      darForm: formulaireDarDepuis(fiche('FP-SIRH-48213'), '1'),
      remuneration: 'Selon expérience et grille indiciaire',
      creeLe: '15 octobre 2026',
      modifieLe: '17 octobre 2026',
      historique: [
        { date: '15 octobre 2026', texte: 'Offre créée depuis la fiche FP-SIRH-48213' },
        { date: '17 octobre 2026', texte: 'DAR DAR-2026-0330 soumise — état : En cours de validation (DAR)' },
      ],
    },
    {
      ...VIDE,
      ...contenuDepuisFiche(fiche('FP-DOC-2026-002')),
      titre: 'Chef·fe de projet numérique — démarches en ligne',
      presentation: 'Vous faites entrer les démarches de la DREAL dans l\'ère du numérique : vos projets simplifient la vie des usagers et des agents.',
      profil: 'Vous avez conduit des projets numériques et savez faire travailler ensemble métiers et prestataires.',
      id: 'OFF-2026-0145',
      ficheId: 'FP-DOC-2026-002',
      etat: 'a_publier',
      origineContenu: 'fiche',
      nbPostes: '1',
      dar: 'requise',
      darStatut: 'validee',
      darRef: 'DAR-2026-0311',
      darSoumiseLe: '9 octobre 2026',
      darValideeLe: '15 octobre 2026',
      darForm: formulaireDarDepuis(fiche('FP-DOC-2026-002'), '1'),
      remuneration: 'Selon expérience, de 2 600 à 3 400 € brut mensuel',
      dateLimite: '2026-11-20',
      contact: 'Pôle numérique — recrutement.num@exemple.gouv.fr',
      creeLe: '14 octobre 2026',
      modifieLe: '16 octobre 2026',
      historique: [
        { date: '8 octobre 2026', texte: 'Offre créée depuis la fiche FP-DOC-2026-002' },
        { date: '9 octobre 2026', texte: 'DAR DAR-2026-0311 soumise — état : En cours de validation (DAR)' },
        { date: '15 octobre 2026', texte: 'DAR validée par Hélène Robert — état : À publier' },
      ],
    },
    {
      ...VIDE,
      ...contenuDepuisFiche(fiche('FP-SG-2025-031')),
      titre: 'Assistant·e administratif·ve au service Aménagement',
      presentation: 'Au cœur d\'un service de 25 personnes, vous êtes le premier contact des usagers et le point d\'appui de l\'équipe.',
      id: 'OFF-2026-0118',
      ficheId: 'FP-SG-2025-031',
      etat: 'publiee',
      origineContenu: 'fiche',
      nbPostes: '1',
      dar: 'requise',
      darRef: 'DAR-2026-0274',
      darSoumiseLe: '22 septembre 2026',
      darValideeLe: '29 septembre 2026',
      darStatut: 'validee',
      darForm: formulaireDarDepuis(fiche('FP-SG-2025-031'), '1'),
      publications: {
        csp: { etat: 'publiee', debut: '12 octobre 2026', fin: '2026-11-15' },
        intranet: { etat: 'publiee', debut: '12 octobre 2026', fin: '2026-11-15' },
      },
      remuneration: 'Grille indiciaire de catégorie C',
      dateLimite: '2026-11-15',
      contact: 'Nadia Benali, responsable recrutement',
      canaux: ['csp', 'intranet'],
      creeLe: '18 septembre 2026',
      modifieLe: '12 octobre 2026',
      publieeLe: '12 octobre 2026',
      historique: [
        { date: '18 septembre 2026', texte: 'Offre créée depuis la fiche FP-SG-2025-031' },
        { date: '22 septembre 2026', texte: 'DAR DAR-2026-0274 soumise — état : En cours de validation (DAR)' },
        { date: '29 septembre 2026', texte: 'DAR validée — état : À publier' },
        { date: '12 octobre 2026', texte: 'Offre publiée sur Choisir le Service Public et l\'intranet' },
      ],
    },
    {
      ...VIDE,
      ...contenuDepuisFiche(fiche('FP-SG-2023-010')),
      titre: 'Chargé·e d\'accueil',
      id: 'OFF-2025-0087',
      ficheId: 'FP-SG-2023-010',
      etat: 'archivee',
      origineContenu: 'manuel',
      nbPostes: '2',
      dar: 'requise',
      darStatut: 'validee',
      darRef: 'DAR-2025-0102',
      publications: { csp: { etat: 'arretee', debut: '20 mai 2025', fin: '2025-06-30' } },
      dateLimite: '2025-06-30',
      creeLe: '2 mai 2025',
      modifieLe: '15 juillet 2025',
      publieeLe: '20 mai 2025',
      historique: [
        { date: '2 mai 2025', texte: 'Offre créée par saisie manuelle (fiche FP-SG-2023-010 constituée)' },
        { date: '20 mai 2025', texte: 'Offre publiée' },
        { date: '15 juillet 2025', texte: 'Offre archivée (2 postes pourvus)' },
      ],
    },
  ]
}

/** Contenu de l'annonce proposé à partir d'une fiche : repris tel quel, à adapter pour les candidats. */
export function contenuDepuisFiche(f: Fiche): Pick<Offre, 'titre' | 'presentation' | 'missions' | 'profil' | 'indispensables' | 'souhaitables' | 'modalites' | 'lieu' | 'teletravail' | 'conditions'> {
  return {
    titre: f.intitule,
    presentation: f.environnement,
    missions: [f.missions, ...f.activites.map(a => `- ${a}`)].filter(Boolean).join('\n'),
    profil: f.profil,
    indispensables: [...f.competences],
    souhaitables: [],
    modalites: modalitesDepuisFiche(f),
    lieu: f.localisation,
    teletravail: f.teletravail,
    conditions: f.conditions,
  }
}

export function formulaireDarDepuis(f: Fiche, nbPostes: string): FormulaireDar {
  return {
    entite: 'Transition écologique › DREAL Occitanie',
    type: 'Formulaire DAR',
    employeur: 'DREAL Occitanie',
    descriptifEmployeur: 'La DREAL Occitanie met en œuvre les politiques de l\'État en matière de transition écologique, d\'énergie et de logement.',
    descriptifService: f.service,
    intitule: f.intitule,
    categorie: f.categories.length ? `Catégorie ${f.categories.join(' ou ')}` : '',
    nbPostes,
    description: [f.missions, ...f.activites.map(a => `- ${a}`)].filter(Boolean).join('\n'),
    motif: '',
    piecesJointes: [],
  }
}

export function modalitesDepuisFiche(f: Fiche): string {
  if (!f.statuts.length) {
    return ''
  }
  const qui = f.statuts.length === 2 ? 'aux fonctionnaires et aux contractuels' : f.statuts[0] === 'titulaire' ? 'aux fonctionnaires' : 'aux contractuels'
  return `Poste de catégorie ${f.categories.join(' ou ') || '—'} ouvert ${qui}.`
}

// --- Stockage de session ---

const CLE = 'csplab-proto-ats-v8'

function lire(): { fiches: Fiche[], offres: Offre[], organisme: Organisme } | null {
  try {
    const brut = sessionStorage.getItem(CLE)
    return brut ? JSON.parse(brut) : null
  }
  catch {
    return null
  }
}

function organismeInitial(): Organisme {
  return { nom: 'DREAL Occitanie', darObligatoire: true, entite: ENTITES[3]!, typeDar: TYPES_DAR[0]!, valideur: 'Hélène Robert, secrétaire générale' }
}

function initial() {
  const fiches = fichesInitiales()
  return { fiches, offres: offresInitiales(fiches), organisme: organismeInitial() }
}

export const db = reactive(lire() ?? initial())

export function sauvegarder() {
  try {
    sessionStorage.setItem(CLE, JSON.stringify(db))
  }
  catch {
    // Stockage indisponible : le prototype reste utilisable, sans persistance.
  }
}

export function reinitialiser() {
  const neuf = initial()
  db.fiches.splice(0, db.fiches.length, ...neuf.fiches)
  db.offres.splice(0, db.offres.length, ...neuf.offres)
  Object.assign(db.organisme, neuf.organisme)
  sauvegarder()
}

/**
 * Applique le paramètre DAR de l'organisme aux offres en rédaction dont la DAR n'est pas engagée.
 * Hypothèse : les offres déjà soumises ou au-delà gardent leur parcours.
 */
export function appliquerParametreDar() {
  for (const o of db.offres) {
    if (o.etat === 'redaction' && (!o.darStatut || o.darStatut === 'brouillon')) {
      o.dar = db.organisme.darObligatoire ? 'requise' : 'non_requise'
    }
  }
  sauvegarder()
}

export function heure(): string {
  return new Date().toLocaleTimeString('fr-FR', { hour: '2-digit', minute: '2-digit' })
}

/** « le 12 octobre 2026 » ou « aujourd'hui, 14:25 ». */
export function le(date: string | undefined): string {
  if (!date) {
    return ''
  }
  return /^(?:Aujourd'hui|Hier)/.test(date) ? date.charAt(0).toLowerCase() + date.slice(1) : `le ${date}`
}

export function maintenant(): string {
  return `Aujourd'hui, ${heure()}`
}

export const fiche = (id: string) => db.fiches.find(f => f.id === id)
export const offre = (id: string) => db.offres.find(o => o.id === id)
export const offresDe = (ficheId: string) => db.offres.filter(o => o.ficheId === ficheId)

function prochainNumero(prefixe: string, liste: { id: string }[], min = 150) {
  const max = Math.max(min, ...liste.map(x => Number(x.id.slice(-3)) || 0))
  return `${prefixe}${String(max + 1).padStart(3, '0')}`
}

export function nouvelleFiche(partiel: Partial<Fiche>, origine: OrigineFiche, evenement: string): Fiche {
  const f: Fiche = {
    id: prochainNumero('FP-SG-2026-', db.fiches.filter(x => x.id.startsWith('FP-SG-2026-')), 0),
    intitule: '',
    service: '',
    localisation: '',
    categories: [],
    statuts: [],
    codePoste: '',
    missions: '',
    activites: [],
    competences: [],
    profil: '',
    environnement: '',
    teletravail: '',
    conditions: '',
    origine,
    statut: 'active',
    modifieLe: maintenant(),
    historique: [{ date: maintenant(), texte: evenement }],
    ...partiel,
  }
  if (origine === 'document') {
    f.id = prochainNumero('FP-DOC-2026-', db.fiches.filter(x => x.id.startsWith('FP-DOC-2026-')), 0)
  }
  db.fiches.unshift(f)
  sauvegarder()
  return f
}

export function nouvelleOffre(f: Fiche, origineContenu: OrigineContenu, depuis?: Offre): Offre {
  const contenu = depuis
    ? {
        titre: depuis.titre,
        presentation: depuis.presentation,
        missions: depuis.missions,
        profil: depuis.profil,
        indispensables: [...depuis.indispensables],
        souhaitables: [...depuis.souhaitables],
        modalites: depuis.modalites,
        lieu: depuis.lieu,
        teletravail: depuis.teletravail,
        conditions: depuis.conditions,
        remuneration: depuis.remuneration,
        contact: depuis.contact,
        canaux: [...depuis.canaux],
        nbPostes: depuis.nbPostes,
      }
    : contenuDepuisFiche(f)
  const texte = {
    fiche: `Offre créée depuis la fiche ${f.id}`,
    fichier: `Offre créée depuis un fichier (fiche ${f.id})`,
    manuel: `Offre créée par saisie manuelle (fiche ${f.id})`,
    duplication: `Offre créée par duplication de ${depuis?.id} (fiche ${f.id})`,
  }[origineContenu]
  const o: Offre = {
    ...VIDE,
    ...contenu,
    id: `OFF-2026-0${prochainNumero('', db.offres.filter(x => x.id.startsWith('OFF-2026-')))}`,
    ficheId: f.id,
    etat: 'redaction',
    origineContenu,
    sourceOffreId: depuis?.id,
    nbPostes: depuis?.nbPostes ?? '1',
    dar: db.organisme.darObligatoire ? 'requise' : 'non_requise',
    publications: {},
    dateLimite: '',
    creeLe: maintenant(),
    modifieLe: maintenant(),
    historique: [{ date: maintenant(), texte }],
  }
  db.offres.unshift(o)
  f.historique.push({ date: maintenant(), texte: `Offre ${o.id} rattachée` })
  sauvegarder()
  return o
}

export function changerEtat(o: Offre, etat: EtatOffre, texte: string) {
  o.etat = etat
  o.modifieLe = maintenant()
  o.historique.push({ date: maintenant(), texte: `${texte} — état : ${LIBELLES_ETAT[etat]}` })
  sauvegarder()
}
