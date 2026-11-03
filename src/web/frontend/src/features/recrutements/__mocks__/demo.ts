import type { RecrutementDetail, RecrutementsActifs } from '@/features/recrutements/types'
import { DEMO_ACTIONS, DEMO_ORGANISME, DEMO_RECRUTEMENT_INTITULE, DEMO_RECRUTEMENT_UUID, DEMO_UTILISATEUR, demoDate } from '@/api/__mocks__/demo'

export const DEMO_ETAPES: RecrutementDetail['etapes'] = [
  { uuid: 'c0000000-0000-4000-8000-000000000001', nom: 'Candidatures reçues', categorie: 'ENTREE' },
  { uuid: 'c0000000-0000-4000-8000-000000000002', nom: 'Présélection', categorie: 'EN_COURS' },
  { uuid: 'c0000000-0000-4000-8000-000000000003', nom: 'Entretien RH', categorie: 'EN_COURS' },
  { uuid: 'c0000000-0000-4000-8000-000000000004', nom: 'Entretien avec le service', categorie: 'EN_COURS' },
  { uuid: 'c0000000-0000-4000-8000-000000000005', nom: 'Proposition d\'embauche', categorie: 'ACCEPTE' },
  { uuid: 'c0000000-0000-4000-8000-000000000006', nom: 'Non retenue', categorie: 'REFUS' },
]

export const DEMO_RECRUTEMENT_DETAIL: RecrutementDetail = {
  uuid: DEMO_RECRUTEMENT_UUID,
  intitule: DEMO_RECRUTEMENT_INTITULE,
  archive: false,
  date_publication: demoDate(24),
  localisation: {
    zone_geographique: 'EU',
    pays: 'France',
    region: '84',
    departement: '69',
    localisation_label: 'Lyon',
    latitude: 45.764,
    longitude: 4.8357,
  },
  organisme_recruteur: { nom: DEMO_ORGANISME.nom, siret: DEMO_ORGANISME.siret },
  categorie_offre: 'B',
  etapes: DEMO_ETAPES,
  recrutement_role: 'responsable',
}

const AUTRES_RECRUTEMENTS: [intitule: string, responsable: string | null, total: number, aTraiter: number, jours: number][] = [
  ['Chargée de mission transition énergétique', 'Julien Moreau', 18, 11, 9],
  ['Gestionnaire de paie', null, 41, 27, 12],
  ['Adjoint administratif du bureau des marchés', 'Inès Lambert', 12, 4, 15],
  ['Chef de projet systèmes d\'information', null, 23, 15, 19],
  ['Assistante de direction', 'Julien Moreau', 9, 2, 26],
  ['Inspecteur des installations classées', null, 7, 5, 30],
  ['Juriste en droit de l\'environnement', 'Thomas Girard', 15, 6, 33],
  ['Technicien supérieur en hydrologie', null, 11, 9, 38],
]

export const DEMO_RECRUTEMENTS_ACTIFS: RecrutementsActifs[] = [{
  uuid: DEMO_RECRUTEMENT_UUID,
  intitule: DEMO_RECRUTEMENT_INTITULE,
  reference_csp: '2026-1043567',
  nature_offre: 'TITULAIRE_CONTRACTUEL',
  responsables: [{ nom: `${DEMO_UTILISATEUR.prenom} ${DEMO_UTILISATEUR.nom}` }],
  authorized_actions: DEMO_ACTIONS,
  date_publication: demoDate(24),
  candidatures: { total: 32, a_traiter: 20, en_cours: 9 },
  derniere_activite: demoDate(1, 16, 40),
  unread_conversations: 0,
}, ...AUTRES_RECRUTEMENTS.map(([intitule, responsable, total, aTraiter, jours], index): RecrutementsActifs => ({
  uuid: `b0000000-0000-4000-8000-00000000001${index}`,
  intitule,
  reference_csp: `2026-10${String(43600 + index * 37)}`,
  nature_offre: index % 3 === 2 ? 'CONTRACTUEL' : 'TITULAIRE_CONTRACTUEL',
  responsables: responsable ? [{ nom: responsable }] : [],
  authorized_actions: DEMO_ACTIONS,
  date_publication: demoDate(jours),
  candidatures: { total, a_traiter: aTraiter, en_cours: total - aTraiter - 1 },
  derniere_activite: demoDate(index + 2, 11, 15),
  unread_conversations: index === 1 ? 2 : 0,
}))]
