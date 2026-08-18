export const VERSANTS = ['FPE', 'FPT', 'FPH'] as const

export type Versant = typeof VERSANTS[number]

export interface OrganismeGestionnaire {
  prenom: string
  nom: string
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
