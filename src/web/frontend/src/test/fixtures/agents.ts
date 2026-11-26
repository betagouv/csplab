import type { Agent, AgentRecherche } from '@/features/agents/types'

export const AGENT_UUID = 'bbbbbbbb-0001-0001-0001-000000000001'

export const AGENT_RECHERCHE: AgentRecherche = {
  uuid: AGENT_UUID,
  email: 'jeanne.dupont@example.gouv.fr',
  prenom: 'Jeanne',
  nom: 'Dupont',
  intitule_poste: 'Responsable recrutement',
}

export const NOUVEL_AGENT: AgentRecherche = {
  uuid: 'bbbbbbbb-0002-0002-0002-000000000002',
  email: 'paul.bernard@example.gouv.fr',
  prenom: 'Paul',
  nom: 'Bernard',
  intitule_poste: 'Responsable recrutement',
}

export const CREATED_AGENT: Agent = {
  uuid: 'bbbbbbbb-0003-0003-0003-000000000003',
  email: 'nouvelle.agente@example.gouv.fr',
  prenom: '',
  nom: '',
  intitule_poste: '',
}
