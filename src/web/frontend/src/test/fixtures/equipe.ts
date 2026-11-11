import type { MembreEquipe } from '@/features/equipe-recrutement/types'
import { AGENT_UUID } from './agents'

export const RECRUTEMENT_UUID = 'aaaaaaaa-0001-0001-0001-000000000001'

export const MEMBRE_EQUIPE: MembreEquipe = {
  uuid: AGENT_UUID,
  nom: 'Dupont',
  prenom: 'Jeanne',
  poste: 'Responsable recrutement',
  email: 'jeanne.dupont@example.gouv.fr',
  recrutement_role: 'recruteur',
}

export const EQUIPE: MembreEquipe[] = [MEMBRE_EQUIPE]
