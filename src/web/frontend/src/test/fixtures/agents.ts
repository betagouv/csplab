import type { Agent, AgentRecherche } from '@/features/agents/types'
import { AGENT_UUID } from './organismes'

export const AGENT_RECHERCHE: AgentRecherche = {
  uuid: AGENT_UUID,
  email: 'jeanne.dupont@example.gouv.fr',
  prenom: 'Jeanne',
  nom: 'Dupont',
  intitule_poste: 'Responsable recrutement',
}

export const CREATED_AGENT: Agent = {
  uuid: 'bbbbbbbb-0003-0003-0003-000000000003',
  email: 'nouvelle.agente@example.gouv.fr',
  prenom: '',
  nom: '',
  intitule_poste: '',
}
