import type { Utilisateur } from '@/api/utilisateur'
import type { components } from '@/types/api'

export const DEMO_ORGANISME = {
  uuid: 'a0000000-0000-4000-8000-000000000001',
  nom: 'Ministère de la Transition écologique',
  siret: '11000001000013',
}

export const DEMO_ORGANISME_AGENT = {
  uuid: 'a0000000-0000-4000-8000-000000000002',
  nom: 'Commune de Briançon',
}

export const DEMO_RECRUTEMENT_UUID = 'b0000000-0000-4000-8000-000000000001'

export const DEMO_RECRUTEMENT_INTITULE = 'Gestionnaire des ressources humaines'

export const DEMO_CANDIDATURE = {
  uuid: 'd0000000-0000-4000-8000-000000000003',
  prenom: 'Clara',
  nom: 'Fontaine',
}

export const DEMO_ACTIONS: components['schemas']['AuthorizedActionsEnum'][] = [
  'get_organisme',
  'list_recrutements',
  'get_recrutement',
  'get_candidature',
  'change_etape_candidatures',
  'get_recrutement_etapes',
  'update_recrutement_etapes',
  'list_organisme_agents',
  'list_recrutement_agents',
  'add_recrutement_agent',
  'update_recrutement_agent',
  'set_recrutements_responsable',
  'get_motifs_refus',
  'read_document',
  'list_documents',
  'list_notes',
  'create_note',
  'update_note',
  'delete_note',
  'list_conversations',
  'read_conversation',
  'create_conversation',
  'reply_conversation',
  'list_tags',
]

export const DEMO_UTILISATEUR: Utilisateur = {
  email: 'camille.bernard@example.gouv.fr',
  prenom: 'Camille',
  nom: 'Bernard',
  is_staff: false,
  organisme_roles: [
    { organisme_uuid: DEMO_ORGANISME.uuid, nom: DEMO_ORGANISME.nom, role: 'superviseur' },
    { organisme_uuid: DEMO_ORGANISME_AGENT.uuid, nom: DEMO_ORGANISME_AGENT.nom, role: 'agent' },
  ],
  authorized_actions: DEMO_ACTIONS,
  organismes: [{ uuid: DEMO_ORGANISME.uuid, nom: DEMO_ORGANISME.nom, authorized_actions: DEMO_ACTIONS }],
}

export function demoDate(daysAgo: number, hours = 9, minutes = 0): string {
  const date = new Date()
  date.setDate(date.getDate() - daysAgo)
  date.setHours(hours, minutes, 0, 0)
  return date.toISOString()
}

export function paginated<T>(results: T[]) {
  return { count: results.length, next: null, previous: null, results }
}
