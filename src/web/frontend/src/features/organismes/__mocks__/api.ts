import type * as Api from '@/features/organismes/api'
import type { AgentOrganisme, OrganismeDetail } from '@/features/organismes/types'
import { DEMO_ORGANISME, DEMO_UTILISATEUR, demoDate } from '@/api/__mocks__/demo'

const DEMO_ORGANISME_DETAIL: OrganismeDetail = {
  ...DEMO_ORGANISME,
  versant: 'FPE',
  superviseurs: `${DEMO_UTILISATEUR.prenom} ${DEMO_UTILISATEUR.nom}`,
  gestion_ats: true,
  date_derniere_activite: demoDate(1),
  date_creation: demoDate(320),
}

const AGENTS: [prenom: string, nom: string, poste: string, role: AgentOrganisme['role'], activite: number | null][] = [
  [DEMO_UTILISATEUR.prenom, DEMO_UTILISATEUR.nom, 'Cheffe du bureau du recrutement', 'superviseur', 0],
  ['Julien', 'Moreau', 'Chargé de recrutement', 'agent', 2],
  ['Inès', 'Lambert', 'Gestionnaire des ressources humaines', 'agent', 5],
  ['Thomas', 'Girard', 'Adjoint au chef de service', 'agent', 12],
  ['Sophie', 'Roux', 'Chargée de mission handicap', 'agent', null],
  ['Karim', 'Benali', 'Responsable de la formation', 'agent', 31],
]

const DEMO_AGENTS: AgentOrganisme[] = AGENTS.map(([prenom, nom, poste, role, activite], index) => ({
  uuid: `e0000000-0000-4000-8000-00000000000${index + 1}`,
  organisme_id: DEMO_ORGANISME.uuid,
  prenom,
  nom,
  email: `${prenom.toLowerCase()}.${nom.toLowerCase()}@example.gouv.fr`.normalize('NFD').replace(/\p{Diacritic}/gu, ''),
  poste,
  role,
  date_derniere_activite: activite === null ? null : demoDate(activite),
  date_creation_compte: demoDate(200 - index * 20),
}))

export const getOrganismesList: typeof Api.getOrganismesList = async () => [{
  ...DEMO_ORGANISME_DETAIL,
  nombre_agents: DEMO_AGENTS.length,
  nombre_offres_publiees: 1,
}]

export const getOrganismeDetail: typeof Api.getOrganismeDetail = async () => DEMO_ORGANISME_DETAIL

export const createOrganisme: typeof Api.createOrganisme = async () => DEMO_ORGANISME_DETAIL

export const updateOrganisme: typeof Api.updateOrganisme = async () => DEMO_ORGANISME_DETAIL

export const getOrganismeAgents: typeof Api.getOrganismeAgents = async () => DEMO_AGENTS

export const setAgentRole: typeof Api.setAgentRole = async () => DEMO_AGENTS[0]!

export const updateAgentRole: typeof Api.updateAgentRole = async () => DEMO_AGENTS[0]!
