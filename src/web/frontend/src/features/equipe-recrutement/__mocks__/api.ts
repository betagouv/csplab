import type * as Api from '@/features/equipe-recrutement/api'
import type { MembreEquipe } from '@/features/equipe-recrutement/types'

const DEMO_EQUIPE: MembreEquipe[] = [
  { uuid: 'e0000000-0000-4000-8000-000000000001', prenom: 'Camille', nom: 'Bernard', poste: 'Responsable du recrutement', email: 'camille.bernard@example.gouv.fr', recrutement_role: 'responsable' },
  { uuid: 'e0000000-0000-4000-8000-000000000002', prenom: 'Julien', nom: 'Moreau', poste: 'Chargé de recrutement', email: 'julien.moreau@example.gouv.fr', recrutement_role: 'recruteur' },
  { uuid: 'e0000000-0000-4000-8000-000000000003', prenom: 'Sophie', nom: 'Lambert', poste: 'Gestionnaire RH', email: 'sophie.lambert@example.gouv.fr', recrutement_role: 'contributeur' },
]

export const getEquipeRecrutement: typeof Api.getEquipeRecrutement = async () => DEMO_EQUIPE

export const addMembreEquipe: typeof Api.addMembreEquipe = async () => DEMO_EQUIPE[0]!

export const updateMembreEquipe: typeof Api.updateMembreEquipe = async () => undefined
