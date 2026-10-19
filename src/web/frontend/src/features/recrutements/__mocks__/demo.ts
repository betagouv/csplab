import type { RecrutementDetail, RecrutementsActifs } from '@/features/recrutements/types'
import { DEMO_ORGANISME, DEMO_RECRUTEMENT_INTITULE, DEMO_RECRUTEMENT_UUID, DEMO_UTILISATEUR, demoDate } from '@/api/__mocks__/demo'

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
}

export const DEMO_RECRUTEMENTS_ACTIFS: RecrutementsActifs[] = [{
  uuid: DEMO_RECRUTEMENT_UUID,
  intitule: DEMO_RECRUTEMENT_INTITULE,
  reference_csp: '2026-1043567',
  nature_offre: 'TITULAIRE_CONTRACTUEL',
  responsables: [{ nom: `${DEMO_UTILISATEUR.prenom} ${DEMO_UTILISATEUR.nom}` }],
  date_publication: demoDate(24),
  candidatures: { total: 32, a_traiter: 20, en_cours: 9 },
  derniere_activite: demoDate(1, 16, 40),
}]
