import type { Utilisateur } from '@/api/utilisateur'

export const DEMO_ORGANISME = {
  uuid: 'a0000000-0000-4000-8000-000000000001',
  nom: 'Ministère de la Transition écologique',
  siret: '11000001000013',
}

export const DEMO_RECRUTEMENT_UUID = 'b0000000-0000-4000-8000-000000000001'

export const DEMO_RECRUTEMENT_INTITULE = 'Gestionnaire des ressources humaines'

export const DEMO_CANDIDATURE = {
  uuid: 'd0000000-0000-4000-8000-000000000003',
  prenom: 'Clara',
  nom: 'Fontaine',
}

export const DEMO_UTILISATEUR: Utilisateur = {
  email: 'camille.bernard@example.gouv.fr',
  prenom: 'Camille',
  nom: 'Bernard',
  is_staff: false,
  organisme_roles: [{ organisme_uuid: DEMO_ORGANISME.uuid, nom: DEMO_ORGANISME.nom, role: 'superviseur' }],
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
