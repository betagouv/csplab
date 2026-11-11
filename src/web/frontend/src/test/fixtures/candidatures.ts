import type { CandidatureParams } from '@/api/params'
import type { OrganismeRole } from '@/api/utilisateur'
import type { Activite, Candidat, CandidatureDetail, CandidatureListe, DocumentListe, KanbanColumn, MotifRefus, MotifRefusOption, Note, RecrutementListe } from '@/features/candidatures/types'
import type { RecrutementDetail } from '@/features/recrutements/types'
import type { components } from '@/types/api'

export const ORGANISME_UUID = '00000000-0000-0000-0000-000000000000'
export const RECRUTEMENT_UUID = 'aaaaaaaa-0001-0001-0001-000000000001'
export const KANBAN_PATH = `/organismes/${ORGANISME_UUID}/recrutements/${RECRUTEMENT_UUID}`

export const ETAPE_RECEPTION = 'cccccccc-0001-0001-0001-000000000001'
export const ETAPE_ENTRETIEN = 'cccccccc-0001-0001-0001-000000000002'
export const ETAPE_REFUS = 'cccccccc-0001-0001-0001-000000000003'

export function roleOnOrganisme(role: OrganismeRole['role']): OrganismeRole {
  return { organisme_uuid: ORGANISME_UUID, nom: 'Ministère de la Transition Écologique', role }
}

export const CANDIDATURE_ALICE = 'dddddddd-0001-0001-0001-000000000001'
export const CANDIDATURE_BRUNO = 'dddddddd-0001-0001-0001-000000000002'

export const CANDIDATURE_PARAMS: CandidatureParams = {
  organismeUuid: ORGANISME_UUID,
  recrutementUuid: RECRUTEMENT_UUID,
  candidatureUuid: CANDIDATURE_ALICE,
}

export const CANDIDAT_ALICE: Candidat = { uuid: 'eeeeeeee-0001-0001-0001-000000000001', nom: 'Dupont', prenom: 'Alice' }
export const CANDIDAT_BRUNO: Candidat = { uuid: 'eeeeeeee-0001-0001-0001-000000000002', nom: 'Martin', prenom: 'Bruno' }

export const KANBAN_COLUMNS: KanbanColumn[] = [
  {
    uuid: ETAPE_RECEPTION,
    nom: 'Réception des candidatures',
    categorie: 'ENTREE',
    candidatures: [
      {
        uuid: CANDIDATURE_ALICE,
        date_soumission: '2025-06-10T09:15:00Z',
        date_derniere_activite: '2025-06-11T10:00:00Z',
        unread_conversations: 0,
        candidat: CANDIDAT_ALICE,
      },
      {
        uuid: CANDIDATURE_BRUNO,
        date_soumission: '2025-06-12T09:15:00Z',
        date_derniere_activite: '2025-06-12T10:00:00Z',
        unread_conversations: 0,
        candidat: CANDIDAT_BRUNO,
      },
    ],
  },
  { uuid: ETAPE_ENTRETIEN, nom: 'Entretien', categorie: 'EN_COURS', candidatures: [] },
  { uuid: ETAPE_REFUS, nom: 'Refus', categorie: 'REFUS', candidatures: [] },
]

export function makeCandidatureRow(index: number): CandidatureListe {
  return {
    uuid: `dddddddd-0002-0002-0002-${String(index + 1).padStart(12, '0')}`,
    date_soumission: '2025-06-10T09:15:00Z',
    date_derniere_activite: new Date(Date.UTC(2025, 5, 19, 10) - index * 3_600_000).toISOString(),
    unread_conversations: 0,
    candidat: { ...CANDIDAT_ALICE, prenom: `Candidat ${index + 1}` },
    etape: { uuid: ETAPE_RECEPTION, nom: 'Réception des candidatures', categorie: 'ENTREE' },
  }
}

export const CANDIDATURE_LISTE: RecrutementListe = {
  count: 2,
  next: null,
  previous: null,
  results: KANBAN_COLUMNS.flatMap(({ uuid, nom, categorie, candidatures }) =>
    candidatures.map(candidature => ({ ...candidature, etape: { uuid, nom, categorie } }))),
  etapes: KANBAN_COLUMNS.map(({ uuid, nom, categorie }) => ({ uuid, nom, categorie })),
}

export function candidatureDetail(candidatureUuid: string): CandidatureDetail {
  const etape = KANBAN_COLUMNS.find(({ candidatures }) => candidatures.some(({ uuid }) => uuid === candidatureUuid))!
  const candidature = etape.candidatures.find(({ uuid }) => uuid === candidatureUuid)!
  return {
    uuid: candidatureUuid,
    candidat: { ...candidature.candidat, email: 'candidat@example.fr' },
    recrutement_intitule: 'Chargé de mission',
    etapes: KANBAN_COLUMNS.map(({ uuid, nom }) => ({ uuid, nom })),
    etape_actuelle: { uuid: etape.uuid, nom: etape.nom },
    motif_refus: null,
    date_candidature: candidature.date_soumission,
    date_derniere_maj_candidat: null,
    date_derniere_maj_recruteur: null,
    document_uuid: null,
    navigation_candidature_uuids: etape.candidatures.map(({ uuid }) => uuid),
    authorized_actions: ['change_etape_candidatures'],
  }
}

export const RECRUTEMENT_DETAIL: RecrutementDetail = {
  uuid: RECRUTEMENT_UUID,
  intitule: 'Chargé de mission',
  archive: false,
  date_publication: '2025-06-01T09:00:00Z',
  localisations: [{
    zone_geographique: 'France',
    pays: 'France',
    region: 'Île-de-France',
    departement: 'Paris',
    localisation_label: 'Paris',
    latitude: null,
    longitude: null,
  }],
  organisme_recruteur: { nom: 'Ministère de la Transition Écologique', siret: '11000201100044' },
  categorie_offre: 'A',
  etapes: KANBAN_COLUMNS.map(({ uuid, nom, categorie }) => ({ uuid, nom, categorie })),
  recrutement_role: null,
  authorized_actions: ['change_etape_candidatures'],
}

export const MOTIFS_REFUS: MotifRefusOption[] = [
  { value: 'experience_insuffisante', label: 'Expérience insuffisante' },
  { value: 'disponibilite', label: 'Disponibilité' },
  { value: 'autre', label: 'Autre' },
]

export const CV_DOCUMENT: DocumentListe = {
  uuid: 'ffffffff-0001-0001-0001-000000000001',
  type: 'cv',
  nom_original: 'CV Alice Dupont.pdf',
  content_type: 'application/pdf',
  taille: 73_400,
  depose_par_uuid: CANDIDAT_ALICE.uuid,
  depose_par: 'Alice Dupont',
  depose_le: '2025-06-10T09:15:00Z',
}

export const LETTRE_DOCUMENT: DocumentListe = {
  ...CV_DOCUMENT,
  uuid: 'ffffffff-0001-0001-0001-000000000002',
  type: 'lettre_motivation',
  nom_original: 'Lettre.png',
  content_type: 'image/png',
  taille: 12_000,
}

export const NOTE: Note = {
  uuid: 'ffffffff-0002-0002-0002-000000000001',
  candidature_id: CANDIDATURE_ALICE,
  message: 'Profil solide',
  publie_par_id: 'eeeeeeee-0002-0002-0002-000000000001',
  publie_par_prenom: 'Marie',
  publie_par_nom: 'Dupont',
  publie_le: '2025-06-10T09:15:00',
  est_privee: false,
  authorized_actions: ['update_note', 'delete_note'],
}

export const SECONDE_NOTE: Note = {
  ...NOTE,
  uuid: 'ffffffff-0002-0002-0002-000000000002',
  message: 'À recontacter',
  publie_par_id: 'eeeeeeee-0002-0002-0002-000000000002',
  publie_par_prenom: 'Paul',
  publie_par_nom: 'Bernard',
}

export const ACTIVITE: Activite = {
  utilisateur_id: NOTE.publie_par_id,
  utilisateur_prenom: NOTE.publie_par_prenom,
  utilisateur_nom: NOTE.publie_par_nom,
  occurred_at: '2026-09-29T10:00:00',
  event_name: 'NoteAjoutee',
}

export function etapeChangeBody(etapeCibleUuid: string, candidatureUuids: string[], motifRefus?: MotifRefus): components['schemas']['PatchedChangerEtapeCandidatures'] {
  return {
    etape_cible_uuid: etapeCibleUuid,
    candidatures: candidatureUuids.map(candidature_uuid => ({ candidature_uuid })),
    motif_refus: motifRefus,
  }
}
