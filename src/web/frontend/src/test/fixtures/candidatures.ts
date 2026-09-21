import type { Candidat, RecrutementDetailKanban } from '@/features/candidatures/types'
import type { RecrutementDetail } from '@/features/recrutements/types'

export const ORGANISME_UUID = '00000000-0000-0000-0000-000000000000'
export const RECRUTEMENT_UUID = 'aaaaaaaa-0001-0001-0001-000000000001'
export const KANBAN_PATH = `/organismes/${ORGANISME_UUID}/recrutements/${RECRUTEMENT_UUID}`

export const ETAPE_RECEPTION = 'cccccccc-0001-0001-0001-000000000001'
export const ETAPE_ENTRETIEN = 'cccccccc-0001-0001-0001-000000000002'
export const ETAPE_REFUS = 'cccccccc-0001-0001-0001-000000000003'

export const CANDIDATURE_ALICE = 'dddddddd-0001-0001-0001-000000000001'
export const CANDIDATURE_BRUNO = 'dddddddd-0001-0001-0001-000000000002'

export const CANDIDAT_ALICE: Candidat = { uuid: 'eeeeeeee-0001-0001-0001-000000000001', nom: 'Dupont', prenom: 'Alice' }
export const CANDIDAT_BRUNO: Candidat = { uuid: 'eeeeeeee-0001-0001-0001-000000000002', nom: 'Martin', prenom: 'Bruno' }

export const KANBAN: RecrutementDetailKanban = {
  offer_id: RECRUTEMENT_UUID,
  etapes: [
    {
      etape_uuid: ETAPE_RECEPTION,
      nom: 'Réception des candidatures',
      categorie: 'ENTREE',
      candidatures: [
        {
          uuid: CANDIDATURE_ALICE,
          date_soumission: '2025-06-10T09:15:00Z',
          date_derniere_activite: '2025-06-11T10:00:00Z',
          candidat: CANDIDAT_ALICE,
        },
        {
          uuid: CANDIDATURE_BRUNO,
          date_soumission: '2025-06-12T09:15:00Z',
          date_derniere_activite: '2025-06-12T10:00:00Z',
          candidat: CANDIDAT_BRUNO,
        },
      ],
    },
    { etape_uuid: ETAPE_ENTRETIEN, nom: 'Entretien', categorie: 'EN_COURS', candidatures: [] },
    { etape_uuid: ETAPE_REFUS, nom: 'Refus', categorie: 'REFUS', candidatures: [] },
  ],
}

export const RECRUTEMENT_DETAIL = {
  intitule: 'Chargé de mission',
  date_publication: '2025-06-01T09:00:00Z',
  localisation: { localisation_label: 'Paris' },
  organisme_recruteur: { nom: 'Ministère de la Transition Écologique' },
  categorie_offre: 'A',
  etapes: KANBAN.etapes.map(({ etape_uuid, nom, categorie }) => ({ etape_uuid, nom, categorie })),
} as unknown as RecrutementDetail
