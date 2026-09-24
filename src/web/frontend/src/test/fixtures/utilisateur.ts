import type { OrganismeRole, Utilisateur } from '@/api/utilisateur'

export const MTE_UUID = 'a1a1a1a1-a1a1-a1a1-a1a1-a1a1a1a1a1a1'
export const BRIANCON_UUID = 'b2b2b2b2-b2b2-b2b2-b2b2-b2b2b2b2b2b2'
export const ORGANISME_INCONNU_UUID = 'c3c3c3c3-c3c3-c3c3-c3c3-c3c3c3c3c3c3'

export const ROLE_MTE: OrganismeRole = {
  organisme_uuid: MTE_UUID,
  nom: 'Ministère de la Transition Écologique',
  role: 'superviseur',
}

export const ROLE_BRIANCON: OrganismeRole = {
  organisme_uuid: BRIANCON_UUID,
  nom: 'Commune de Briançon',
  role: 'agent',
}

export function makeUser(organismeRoles: OrganismeRole[], isStaff = false): Utilisateur {
  return {
    email: 'marie.dupont@example.gouv.fr',
    prenom: 'Marie',
    nom: 'Dupont',
    is_staff: isStaff,
    organisme_roles: organismeRoles,
  }
}
