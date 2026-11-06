import type { Utilisateur } from '@/api/utilisateur'

export type UserOrganisme = Utilisateur['organismes'][number]

export const MTE_UUID = 'a1a1a1a1-a1a1-a1a1-a1a1-a1a1a1a1a1a1'
export const BRIANCON_UUID = 'b2b2b2b2-b2b2-b2b2-b2b2-b2b2b2b2b2b2'
export const ORGANISME_INCONNU_UUID = 'c3c3c3c3-c3c3-c3c3-c3c3-c3c3c3c3c3c3'

export const ORGANISME_MTE: UserOrganisme = {
  uuid: MTE_UUID,
  nom: 'Ministère de la Transition Écologique',
  authorized_actions: [],
}

export const ORGANISME_BRIANCON: UserOrganisme = {
  uuid: BRIANCON_UUID,
  nom: 'Commune de Briançon',
  authorized_actions: [],
}

export function makeUser(organismes: UserOrganisme[], isStaff = false): Utilisateur {
  return {
    email: 'marie.dupont@example.gouv.fr',
    prenom: 'Marie',
    nom: 'Dupont',
    is_staff: isStaff,
    authorized_actions: isStaff ? ['create_organisme', 'list_organismes', 'update_organisme'] : [],
    organismes,
    organisme_roles: [],
  }
}
