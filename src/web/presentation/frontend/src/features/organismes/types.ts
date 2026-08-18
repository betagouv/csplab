export const VERSANTS = ['FPE', 'FPT', 'FPH'] as const

export type Versant = typeof VERSANTS[number]

export interface OrganismeGestionnaire {
  prenom: string
  nom: string
  invitation_en_attente?: boolean
}

export interface UtilisateurRecherche {
  uuid: string
  prenom: string
  nom: string
  email: string
}

export type CompteUtilisateurType = 'gestionnaire' | 'agent'

export interface CreateCompteUtilisateurPayload {
  email: string
  nom: string
  prenom: string
  poste: string
  type: CompteUtilisateurType
}

export interface OrganismeAdmin {
  uuid: string
  nom: string
  siret: string
  versant: Versant
  gestion_candidatures: boolean
  gestionnaire: OrganismeGestionnaire | null
}

export interface CreateOrganismePayload {
  nom: string
  siret: string
  versant: Versant
  gestion_candidatures: boolean
}

export interface UpdateOrganismePayload {
  nom: string
  versant: Versant
  gestion_candidatures: boolean
}
