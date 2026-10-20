// Référentiels fictifs. Les libellés sont plausibles mais ne reprennent pas de référentiel officiel :
// le vrai répertoire des métiers, les motifs et les profils dépendent du versant et de la réglementation.

import type { Canal, Personne } from './types'

export const ORGANISMES = [
  { value: 'dreal-occ', label: 'DREAL Occitanie', versant: 'Fonction publique d\'État' },
  { value: 'pref-31', label: 'Préfecture de la Haute-Garonne', versant: 'Fonction publique d\'État' },
  { value: 'metro-garonne', label: 'Métropole de Garonne (fictive)', versant: 'Fonction publique territoriale' },
  { value: 'commune-aurin', label: 'Commune de Saint-Aurin (fictive)', versant: 'Fonction publique territoriale' },
  { value: 'ch-montauban', label: 'Centre hospitalier de Montauban (fictif)', versant: 'Fonction publique hospitalière' },
]

export const SERVICES: Record<string, string[]> = {
  'dreal-occ': [
    'Service Énergie, Climat, Logement — Pôle transition énergétique',
    'Service Aménagement — Pôle urbanisme durable',
    'Secrétariat général — Bureau des ressources humaines',
  ],
  'pref-31': ['Direction des sécurités', 'Direction de la citoyenneté et de la légalité'],
  'metro-garonne': ['Direction de la transition écologique', 'Direction des ressources humaines'],
  'commune-aurin': ['Services techniques', 'Direction générale des services'],
  'ch-montauban': ['Direction des soins', 'Direction des ressources humaines'],
}

export function versantDe(organisme: string): string {
  return ORGANISMES.find(o => o.value === organisme)?.versant ?? ''
}

export const MOTIFS = [
  { value: 'vacance', label: 'Vacance de poste (départ, mobilité, retraite)' },
  { value: 'remplacement', label: 'Remplacement temporaire (congé, absence)' },
  { value: 'creation', label: 'Création de poste' },
  { value: 'campagne', label: 'Campagne de mobilité' },
  { value: 'renfort', label: 'Renfort ponctuel' },
]

export const METIERS = [
  { value: 'm-transeco', label: 'Chargé·e de mission transition écologique', description: 'Développement durable' },
  { value: 'm-accterr', label: 'Chargé·e d\'accompagnement des territoires', description: 'Aménagement et territoires' },
  { value: 'm-energie', label: 'Chargé·e d\'études énergie-climat', description: 'Développement durable' },
  { value: 'm-grh', label: 'Gestionnaire des ressources humaines', description: 'Ressources humaines' },
  { value: 'm-immo', label: 'Responsable de projet immobilier', description: 'Patrimoine et logistique' },
  { value: 'm-ads', label: 'Instructeur·rice des autorisations d\'urbanisme', description: 'Aménagement et territoires' },
  { value: 'm-com', label: 'Chargé·e de communication', description: 'Communication' },
  { value: 'm-juriste', label: 'Juriste', description: 'Affaires juridiques' },
  { value: 'm-cdg', label: 'Contrôleur·se de gestion', description: 'Finances et budget' },
  { value: 'm-num', label: 'Chef·fe de projet numérique', description: 'Numérique' },
  { value: 'm-assist', label: 'Assistant·e de direction', description: 'Fonctions support' },
]

export function libelleMetier(value: string | null): string {
  return METIERS.find(m => m.value === value)?.label ?? ''
}

export const CATEGORIES = [
  { value: 'A', label: 'Catégorie A' },
  { value: 'B', label: 'Catégorie B' },
  { value: 'C', label: 'Catégorie C' },
]

export const STATUTS = [
  { value: 'titulaire', label: 'Fonctionnaire (titulaire)' },
  { value: 'contractuel', label: 'Contractuel·le' },
]

export const PROFILS = [
  { value: 'fonct-meme-versant', label: 'Fonctionnaires du même versant (mutation, mobilité)' },
  { value: 'fonct-autres-versants', label: 'Fonctionnaires des autres versants (détachement)' },
  { value: 'contractuels', label: 'Candidats contractuels' },
  { value: 'handicap', label: 'Bénéficiaires de l\'obligation d\'emploi — voie contractuelle spécifique (à confirmer)' },
]

export const TYPES_CRITERE = [
  { value: 'diplome', label: 'Diplôme ou niveau' },
  { value: 'experience', label: 'Expérience' },
  { value: 'competence', label: 'Compétence' },
  { value: 'permis', label: 'Permis, habilitation' },
  { value: 'autre', label: 'Autre' },
]

export const PERSONNES: Personne[] = [
  { id: 'camille', nom: 'Camille Moreau', role: 'RH de proximité', service: 'Bureau des ressources humaines' },
  { id: 'julien', nom: 'Julien Lefèvre', role: 'Manager — chef du pôle', service: 'Pôle transition énergétique' },
  { id: 'isabelle', nom: 'Isabelle Fournier', role: 'Manager — cheffe du bureau RH', service: 'Bureau des ressources humaines' },
  { id: 'nadia', nom: 'Nadia Benali', role: 'Responsable recrutement et mobilité', service: 'Plateforme RH régionale' },
  { id: 'helene', nom: 'Hélène Robert', role: 'Secrétaire générale — autorité de validation', service: 'Secrétariat général' },
  { id: 'thomas', nom: 'Thomas Garnier', role: 'Contrôle de gestion — budget', service: 'Secrétariat général' },
  { id: 'sophie', nom: 'Sophie Martin', role: 'Chargée de communication', service: 'Cabinet' },
]

/** La personne qui utilise le prototype. */
export const MOI = 'camille'

export function personne(id: string): Personne {
  return PERSONNES.find(p => p.id === id) ?? PERSONNES[0]!
}

export const CANAUX: Canal[] = [
  {
    id: 'csp',
    nom: 'Choisir le Service Public',
    description: 'Site de référence des offres de la fonction publique. Hypothèse : transmission par un connecteur (non simulé ici).',
    mode: 'connecteur',
    selectionne: true,
    attendus: [
      { libelle: 'Métier du répertoire renseigné', ok: s => Boolean(s.besoin.metier), stepId: 'besoin' },
      { libelle: 'Catégorie renseignée', ok: s => s.besoin.categories.length > 0, stepId: 'besoin' },
      { libelle: 'Date limite de candidature', ok: s => Boolean(s.dateLimite), stepId: 'diffusion' },
    ],
    actionsManuelles: [],
  },
  {
    id: 'site',
    nom: 'Site internet de l\'organisme',
    description: 'Page « Nous rejoindre ». Mise en ligne par l\'équipe web.',
    mode: 'manuel',
    selectionne: false,
    attendus: [],
    actionsManuelles: ['Transmettre le texte de l\'offre à l\'équipe web'],
  },
  {
    id: 'intranet',
    nom: 'Intranet ministériel',
    description: 'Visible des agents uniquement. Utile pour la mobilité interne.',
    mode: 'manuel',
    selectionne: false,
    attendus: [],
    actionsManuelles: ['Publier l\'annonce dans la rubrique mobilité'],
  },
  {
    id: 'linkedin',
    nom: 'LinkedIn — page de l\'organisme',
    description: 'Publication par la communication, avec le lien de candidature.',
    mode: 'manuel',
    selectionne: false,
    attendus: [
      { libelle: 'Présentation du poste rédigée (sert de texte court)', ok: s => s.offre.poste.texte.trim().length > 0, stepId: 'offre' },
    ],
    actionsManuelles: ['Copier le texte court et le lien de candidature', 'Demander la publication à la communication'],
  },
  {
    id: 'specialise',
    nom: 'Plateforme spécialisée (réseau métier énergie)',
    description: 'Exemple de site métier ciblé, propre à certains recrutements.',
    mode: 'manuel',
    selectionne: false,
    attendus: [],
    actionsManuelles: ['Déposer l\'annonce sur la plateforme'],
  },
]

export const SECTIONS_OFFRE = [
  { id: 'organisme', libelle: 'Présentation de l\'organisme', requise: false },
  { id: 'poste', libelle: 'Présentation du poste', requise: true },
  { id: 'missions', libelle: 'Missions', requise: true },
  { id: 'profil', libelle: 'Profil recherché', requise: true },
  { id: 'conditions', libelle: 'Conditions de recrutement', requise: false },
  { id: 'pratique', libelle: 'Informations pratiques', requise: false },
  { id: 'candidature', libelle: 'Modalités de candidature', requise: true },
] as const

/** Acronymes fréquents dans les fiches de poste, peu compréhensibles pour un candidat externe. */
export const ACRONYMES = ['DREAL', 'SECL', 'RIFSEEP', 'IFSE', 'CRE', 'BOP', 'PTRE', 'EPCI', 'ETP', 'DAR', 'SG']
