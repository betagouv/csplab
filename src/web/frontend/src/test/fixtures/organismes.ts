import type { AgentOrganisme, AgentRecherche, OrganismeDetail, OrganismesList } from '@/features/organismes/types'

export const AGENT_UUID = 'bbbbbbbb-0001-0001-0001-000000000001'

export const AGENT_ORGANISME: AgentOrganisme = {
  uuid: AGENT_UUID,
  organisme_id: '11111111-1111-1111-1111-111111111111',
  nom: 'Dupont',
  prenom: 'Jeanne',
  email: 'jeanne.dupont@example.gouv.fr',
  poste: 'Chargée de recrutement',
  role: 'agent',
  date_derniere_activite: null,
  date_creation_compte: '2026-01-01T00:00:00Z',
}

export const AGENT_RECHERCHE: AgentRecherche = {
  uuid: AGENT_UUID,
  email: 'jeanne.dupont@example.gouv.fr',
  prenom: 'Jeanne',
  nom: 'Dupont',
  intitule_poste: 'Responsable recrutement',
}

export const ORGANISME: OrganismesList = {
  uuid: '11111111-1111-1111-1111-111111111111',
  nom: 'Organisme 1',
  siret: '11004601800021',
  versant: 'FPT',
  gestionnaire: null,
  gestion_ats: false,
  date_derniere_activite: '2026-08-01T00:00:00Z',
  date_creation: '2026-01-01T00:00:00Z',
  nombre_agents: 10,
  nombre_offres_publiees: 5,
}

export const ORGANISME_DETAIL: OrganismeDetail = {
  uuid: '11111111-1111-1111-1111-111111111111',
  nom: 'Commune de Briançon',
  versant: 'FPT',
  siret: '21050023700354',
  gestionnaire: null,
  gestion_ats: true,
  date_creation: '2026-01-01',
  date_derniere_activite: '2026-01-15',
}
