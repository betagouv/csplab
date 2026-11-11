import type { MembreEquipe } from '@/features/equipe-recrutement/types'
import { AGENT_UUID, NOUVEL_AGENT } from './agents'

export const RECRUTEMENT_UUID = 'aaaaaaaa-0001-0001-0001-000000000001'

export const MEMBRE_EQUIPE: MembreEquipe = {
  uuid: AGENT_UUID,
  nom: 'Dupont',
  prenom: 'Jeanne',
  poste: 'Responsable recrutement',
  email: 'jeanne.dupont@example.gouv.fr',
  recrutement_role: 'recruteur',
}

export const SECOND_MEMBRE_EQUIPE: MembreEquipe = {
  uuid: NOUVEL_AGENT.uuid,
  nom: NOUVEL_AGENT.nom,
  prenom: NOUVEL_AGENT.prenom,
  poste: NOUVEL_AGENT.intitule_poste,
  email: NOUVEL_AGENT.email,
  recrutement_role: 'recruteur',
}

export const EQUIPE: MembreEquipe[] = [MEMBRE_EQUIPE]
