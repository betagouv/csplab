// Référentiel des fiches de poste (fictif), conservé pendant la session.
// Les fiches sont créées et maintenues dans l'ATS ; un SIRH pourra en fournir plus tard (non traité).

import type { FichePoste } from './types'
import { reactive } from 'vue'
import { clone } from './scenario'

const CLE = 'csplab-proto-creation-offre-fiches-v6'
const CLE_COLONNES = 'csplab-proto-creation-offre-colonnes-fiches-v6'

function lire<T>(cle: string): T | null {
  try {
    const brut = sessionStorage.getItem(cle)
    return brut ? JSON.parse(brut) as T : null
  }
  catch {
    return null
  }
}
function ecrire(cle: string, valeur: unknown) {
  try {
    sessionStorage.setItem(cle, JSON.stringify(valeur))
  }
  catch {
    // Stockage indisponible : le prototype reste utilisable, sans persistance.
  }
}

const BASE = {
  statut: 'active' as const,
  organisme: 'dreal-occ',
  localisation: 'Toulouse (31)',
  teletravail: '',
  corps: '',
  qualifications: '',
  conditionsParticulieres: '',
  origine: 'ats' as const,
}

function fichesInitiales(): FichePoste[] {
  return [
    {
      ...BASE,
      id: 'FP-SG-2026-007',
      intitule: 'Gestionnaire de paie',
      service: 'Secrétariat général — Bureau des ressources humaines',
      categories: ['B'],
      statuts: ['titulaire', 'contractuel'],
      metier: 'm-grh',
      codePoste: 'SG-PAIE',
      teletravail: '1 jour par semaine',
      missions: 'Au sein du bureau des ressources humaines, assurer la préparation et le contrôle de la paie des agents titulaires et contractuels de la direction (environ 900 agents), en lien avec le centre de services RH et la DRFiP.',
      activites: [
        'Saisir et contrôler les éléments variables de paie',
        'Calculer les indemnités, rappels et précomptes',
        'Répondre aux questions des agents sur leur rémunération',
        'Participer à la fiabilisation des données de paie',
      ],
      competences: ['Réglementation de la rémunération dans la fonction publique', 'Maîtrise d\'un logiciel de paie', 'Rigueur et respect des échéances', 'Discrétion'],
      profil: 'Agent de catégorie B ou contractuel ; une expérience en paie est souhaitée.',
      environnement: 'Bureau des ressources humaines de 12 agents, dont une cellule paie de 5 personnes. Pics d\'activité liés au calendrier de paie.',
      modifieLe: '2 septembre 2026',
      journal: [
        { date: '12 mars 2026', texte: 'Fiche créée par Camille Moreau' },
        { date: '2 septembre 2026', texte: 'Fiche modifiée — compétences, environnement' },
      ],
    },
    {
      ...BASE,
      id: 'FP-SG-2025-019',
      intitule: 'Chargé·e de ressources humaines',
      service: 'Secrétariat général — Bureau des ressources humaines',
      categories: ['A'],
      statuts: ['titulaire', 'contractuel'],
      metier: 'm-grh',
      codePoste: 'SG-RH',
      missions: 'Piloter la gestion administrative et le conseil RH d\'un portefeuille de services (environ 250 agents) : carrières, mobilité, accompagnement des managers.',
      activites: ['Conseiller les managers et les agents', 'Suivre les actes de carrière', 'Accompagner les mobilités'],
      competences: ['Statut de la fonction publique', 'Conseil et accompagnement', 'Conduite d\'entretiens'],
      profil: '',
      environnement: '',
      modifieLe: '18 novembre 2025',
      journal: [{ date: '18 novembre 2025', texte: 'Fiche créée par Nadia Benali' }],
    },
    {
      ...BASE,
      id: 'FP-SG-2024-031',
      intitule: 'Responsable informatique',
      service: 'Secrétariat général — Pôle numérique',
      categories: ['A'],
      statuts: ['titulaire', 'contractuel'],
      metier: 'm-num',
      codePoste: 'SG-NUM-RESP',
      teletravail: '2 jours par semaine',
      missions: 'Encadrer le pôle numérique (6 agents) et garantir le bon fonctionnement du système d\'information de la direction : postes de travail, réseau, applications métier, sécurité.',
      activites: ['Encadrer et organiser le pôle', 'Piloter le budget et les marchés informatiques', 'Conduire les projets de modernisation', 'Assurer la sécurité du système d\'information'],
      competences: ['Management d\'équipe', 'Architecture des systèmes d\'information', 'Sécurité informatique', 'Conduite de projet'],
      profil: 'Ingénieur·e ou attaché·e avec une solide expérience en informatique ; contractuel possible.',
      environnement: 'Pôle numérique de 6 agents, en lien avec le service ministériel du numérique.',
      modifieLe: '3 avril 2026',
      journal: [{ date: '15 février 2024', texte: 'Fiche créée par Camille Moreau' }, { date: '3 avril 2026', texte: 'Fiche modifiée — missions' }],
    },
    {
      ...BASE,
      id: 'FP-SG-2026-003',
      intitule: 'Gestionnaire RH — carrières',
      service: 'Secrétariat général — Bureau des ressources humaines',
      categories: ['B'],
      statuts: ['titulaire', 'contractuel'],
      metier: 'm-grh',
      codePoste: 'SG-RH-CAR',
      missions: 'Gestion administrative des actes de carrière des agents du périmètre (avancements, promotions, mobilités) ; suivi des dossiers individuels ; relation avec le centre de services RH.',
      activites: ['Préparer les actes de carrière', 'Tenir les dossiers individuels'],
      competences: ['Réglementation statutaire', 'SIRH', 'Sens du service'],
      profil: 'Agent de catégorie B ou contractuel.',
      environnement: 'Bureau des ressources humaines de 12 agents.',
      modifieLe: '16 octobre 2026',
      journal: [{ date: '16 octobre 2026', texte: 'Fiche créée par Camille Moreau' }],
    },
    {
      ...BASE,
      id: 'FP-SG-2026-011',
      intitule: 'Assistant·e de direction',
      service: 'Secrétariat général',
      categories: ['C'],
      statuts: ['titulaire', 'contractuel'],
      metier: 'm-assist',
      codePoste: 'SG-ASSIST',
      missions: 'Assurer le secrétariat de la secrétaire générale : agenda, accueil téléphonique, courrier, préparation des réunions.',
      activites: ['Gérer les agendas', 'Préparer les dossiers de réunion'],
      competences: [],
      profil: '',
      environnement: '',
      modifieLe: 'Hier',
      journal: [{ date: 'Hier', texte: 'Fiche créée par Camille Moreau' }],
    },
    {
      ...BASE,
      id: 'FP-SG-2026-014',
      intitule: 'Chargé·e de communication interne',
      service: 'Secrétariat général',
      categories: ['A'],
      statuts: ['contractuel'],
      metier: 'm-com',
      codePoste: 'SG-COM-INT',
      missions: 'Concevoir et animer la communication interne pendant la réorganisation des services : lettre interne, intranet, événements.',
      activites: ['Rédiger la lettre interne mensuelle', 'Animer l\'intranet', 'Organiser les temps d\'échange avec les agents'],
      competences: ['Rédaction', 'Gestion de projet', 'Outils de publication web'],
      profil: '',
      environnement: '',
      modifieLe: '18 octobre 2026',
      journal: [{ date: '18 octobre 2026', texte: 'Fiche créée par Camille Moreau' }],
    },
    {
      ...BASE,
      id: 'FP-SECL-2024-012',
      intitule: 'Chargé·e de mission rénovation énergétique des collectivités',
      service: 'Service Énergie, Climat, Logement — Pôle transition énergétique',
      categories: ['A'],
      statuts: ['titulaire', 'contractuel'],
      metier: 'm-transeco',
      codePoste: 'SECL-PTRE',
      missions: 'Animer le réseau des plateformes de rénovation énergétique et accompagner les intercommunalités dans leurs programmes.',
      activites: ['Animer le réseau régional', 'Accompagner les intercommunalités', 'Instruire les demandes de subvention'],
      competences: ['Politiques de l\'énergie et du logement', 'Conduite de projet partenarial', 'Animation de réseau'],
      profil: 'Formation supérieure (bac+3) ; expérience en collectivité appréciée.',
      environnement: 'Pôle de 7 agents.',
      modifieLe: '14 mai 2024',
      journal: [{ date: '14 mai 2024', texte: 'Fiche créée par Julien Lefèvre' }],
    },
    {
      ...BASE,
      id: 'FP-SECL-2023-004',
      intitule: 'Chargé·e de mission mobilité durable',
      service: 'Service Aménagement — Pôle urbanisme durable',
      categories: ['A'],
      statuts: ['titulaire'],
      metier: 'm-transeco',
      codePoste: 'SA-MOB',
      missions: 'Accompagner les territoires dans leurs politiques de mobilité durable.',
      activites: ['Conseiller les autorités organisatrices de mobilité', 'Suivre les appels à projets'],
      competences: ['Politiques de mobilité', 'Conduite de projet'],
      profil: '',
      environnement: '',
      modifieLe: '9 janvier 2026',
      journal: [{ date: '9 janvier 2026', texte: 'Fiche créée par Julien Lefèvre' }],
    },
    {
      ...BASE,
      id: 'FP-SA-2021-008',
      statut: 'archivee',
      intitule: 'Instructeur·rice des autorisations d\'urbanisme',
      service: 'Service Aménagement — Pôle urbanisme durable',
      categories: ['B'],
      statuts: ['titulaire'],
      metier: 'm-ads',
      codePoste: 'SA-ADS',
      missions: 'Instruire les demandes d\'autorisation d\'urbanisme pour le compte des communes.',
      activites: [],
      competences: [],
      profil: '',
      environnement: '',
      modifieLe: '30 juin 2024',
      journal: [{ date: '2 mars 2021', texte: 'Fiche créée' }, { date: '30 juin 2024', texte: 'Fiche archivée (mission transférée aux collectivités)' }],
    },
  ]
}

export const fiches = reactive<FichePoste[]>(lire<FichePoste[]>(CLE) ?? fichesInitiales())

export function rangerFiche(f: FichePoste) {
  const i = fiches.findIndex(x => x.id === f.id)
  if (i >= 0) {
    fiches.splice(i, 1, clone(f))
  }
  else {
    fiches.unshift(clone(f))
  }
  ecrire(CLE, fiches)
}

export function trouverFiche(id: string): FichePoste | undefined {
  const f = fiches.find(x => x.id === id)
  return f ? clone(f) : undefined
}

export function nouvelleFiche(): FichePoste {
  const n = fiches.length + 20
  return {
    ...BASE,
    id: `FP-SG-2026-0${n}`,
    intitule: '',
    service: '',
    categories: [],
    statuts: [],
    metier: null,
    codePoste: '',
    missions: '',
    activites: [],
    competences: [],
    profil: '',
    environnement: '',
    modifieLe: 'Aujourd\'hui',
    journal: [{ date: 'Aujourd\'hui', texte: 'Fiche créée par Camille Moreau' }],
  }
}

export function reinitialiserFiches() {
  fiches.splice(0, fiches.length, ...fichesInitiales())
  ecrire(CLE, fiches)
}

/** Ce qui manque à une fiche pour servir de base à une DAR ou à une offre (indicatif, non bloquant). */
export function manquesFiche(f: FichePoste): string[] {
  return [
    !f.missions && 'missions',
    !f.competences.length && 'compétences',
    !f.profil && 'profil recherché',
    !f.environnement && 'environnement de travail',
  ].filter(Boolean) as string[]
}

export const COLONNES_FICHES_DEFAUT = ['service', 'categorie', 'code', 'recrutements', 'modifie']
export const colonnesFiches = reactive<{ visibles: string[] }>({ visibles: lire<string[]>(CLE_COLONNES) ?? [...COLONNES_FICHES_DEFAUT] })
export function enregistrerColonnesFiches() {
  ecrire(CLE_COLONNES, colonnesFiches.visibles)
}
