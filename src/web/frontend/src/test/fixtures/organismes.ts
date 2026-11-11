import type { AgentOrganisme, OrganismeDetail, OrganismeRead, OrganismeRecherche, OrganismesList } from '@/features/organismes/types'
import { AGENT_UUID } from './agents'
import { BRIANCON_UUID, MTE_UUID } from './utilisateur'

export const AGENT_ORGANISME: AgentOrganisme = {
  uuid: AGENT_UUID,
  organisme_id: MTE_UUID,
  nom: 'Dupont',
  prenom: 'Jeanne',
  email: 'jeanne.dupont@example.gouv.fr',
  poste: 'Chargée de recrutement',
  role: 'agent',
  date_derniere_activite: null,
  date_creation_compte: '2026-01-01T00:00:00Z',
}

export const ORGANISME: OrganismesList = {
  uuid: '11111111-1111-1111-1111-111111111111',
  nom: 'Organisme 1',
  siret: '11004601800021',
  versant: 'FPT',
  superviseurs: '',
  gestion_ats: false,
  date_derniere_activite: '2026-08-01T00:00:00Z',
  date_creation: '2026-01-01T00:00:00Z',
  nombre_agents: 10,
  nombre_offres_publiees: 5,
  authorized_actions: [],
}

export const ORGANISMES: OrganismesList[] = [ORGANISME]

export const CREATED_ORGANISME: OrganismeDetail = {
  uuid: '33333333-3333-3333-3333-333333333333',
  nom: 'Commune de Gap',
  siret: '21050061800017',
  versant: 'FPT',
  superviseurs: '',
  gestion_ats: true,
  date_derniere_activite: '2026-08-19T00:00:00Z',
  date_creation: '2026-08-19T00:00:00Z',
}

export const ORGANISME_DETAIL: OrganismeRead = {
  uuid: BRIANCON_UUID,
  nom: 'Commune de Briançon',
  versant: 'FPT',
  siret: '21050023700354',
  superviseurs: '',
  gestion_ats: true,
  date_creation: '2026-01-01',
  date_derniere_activite: '2026-01-15',
  authorized_actions: ['get_organisme'],
}

export const ORGANISME_RECHERCHE: OrganismeRecherche = {
  uuid: ORGANISME_DETAIL.uuid,
  nom: ORGANISME_DETAIL.nom,
  siret: ORGANISME_DETAIL.siret,
}
