import type { RecrutementsActifs, RecrutementsArchives } from './types'

function daysAgo(days: number): string {
  const date = new Date()
  date.setHours(12, 0, 0, 0)
  date.setDate(date.getDate() - days)
  return date.toISOString()
}

export const RECRUTEMENTS_ACTIFS: RecrutementsActifs[] = [
  {
    offer_id: 'rec-1',
    intitule: 'Chargé·e de mission numérique',
    reference_csp: 'REF-001',
    responsables: [{ nom: 'Camille Durand' }],
    type_contrat: 'TITULAIRE_CONTRACTUEL',
    date_publication: daysAgo(1),
    derniere_activite: daysAgo(0),
    candidatures: { total: 24, a_traiter: 12, en_cours: 2 },
  },
  {
    offer_id: 'rec-2',
    intitule: 'Gestionnaire de paie',
    reference_csp: 'REF-002',
    responsables: [{ nom: 'Léa Martin' }],
    type_contrat: 'TITULAIRE_CONTRACTUEL',
    date_publication: daysAgo(1),
    derniere_activite: daysAgo(0),
    candidatures: { total: 24, a_traiter: 12, en_cours: 2 },
  },
  {
    offer_id: 'rec-3',
    intitule: 'Développeur·se back-end',
    reference_csp: 'REF-003',
    responsables: [{ nom: 'Hugo Bernard' }],
    type_contrat: 'CONTRACTUELS',
    date_publication: daysAgo(2),
    derniere_activite: daysAgo(2),
    candidatures: { total: 24, a_traiter: 12, en_cours: 2 },
  },
  {
    offer_id: 'rec-4',
    intitule: 'Apprenti·e communication',
    reference_csp: 'REF-004',
    responsables: [{ nom: 'Sofia Petit' }],
    type_contrat: 'CONTRACTUELS',
    date_publication: daysAgo(2),
    derniere_activite: daysAgo(2),
    candidatures: { total: 24, a_traiter: 12, en_cours: 2 },
  },
  {
    offer_id: 'rec-5',
    intitule: 'Assistant·e administratif·ve',
    reference_csp: 'REF-005',
    responsables: [{ nom: 'Camille Durand' }, { nom: 'Léa Martin' }],
    type_contrat: 'TITULAIRE_CONTRACTUEL',
    date_publication: daysAgo(2),
    derniere_activite: daysAgo(2),
    candidatures: { total: 24, a_traiter: 12, en_cours: 2 },
  },
  {
    offer_id: 'rec-6',
    intitule: 'Agent·e d’accueil',
    reference_csp: 'REF-006',
    responsables: [{ nom: 'Léa Martin' }],
    type_contrat: 'TERRITORIAL',
    date_publication: daysAgo(22),
    derniere_activite: daysAgo(3),
    candidatures: { total: null, a_traiter: null, en_cours: null },
  },
]

export const RECRUTEMENTS_ARCHIVES: RecrutementsArchives[] = [
  {
    offer_id: 'arch-1',
    intitule: 'Chef·fe de projet SI',
    reference_csp: 'REF-101',
    responsables: [{ nom: 'Hugo Bernard' }],
    type_contrat: 'TITULAIRE_CONTRACTUEL',
    date_archivage: daysAgo(120),
    finalise: true,
    recrute: 'Nadia Lefèvre',
  },
  {
    offer_id: 'arch-2',
    intitule: 'Juriste droit public',
    reference_csp: 'REF-102',
    responsables: [{ nom: 'Sofia Petit' }],
    type_contrat: 'TITULAIRE_CONTRACTUEL',
    date_archivage: daysAgo(110),
    finalise: false,
    recrute: null,
  },
  {
    offer_id: 'arch-3',
    intitule: 'Technicien·ne support',
    reference_csp: 'REF-103',
    responsables: [{ nom: 'Camille Durand' }],
    type_contrat: 'TITULAIRE_CONTRACTUEL',
    date_archivage: daysAgo(100),
    finalise: true,
    recrute: 'Yanis Moreau',
  },
]
