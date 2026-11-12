import type { components } from '@/types/api'

export type OrganismesList = components['schemas']['OrganismesList']

export type PaginatedOrganismesListList = components['schemas']['PaginatedOrganismesListList']

export interface OrganismesPageParams {
  page: number
  filter?: string
}

export type OrganismeRecherche = components['schemas']['OrganismeRecherche']

export type OrganismeDetail = components['schemas']['OrganismeDetail']

export type OrganismeRead = components['schemas']['OrganismeRead']

export type CreateOrganismePayload = components['schemas']['CreateOrganisme']

export type UpdateOrganismePayload = components['schemas']['UpdateOrganisme']

export type Versant = components['schemas']['VersantEnum']

export type AgentOrganisme = components['schemas']['AgentOrganisme']

export type Role = components['schemas']['RoleEnum']

export type SetAgentRolePayload = components['schemas']['SetAgentRoleOnOrganisme']

export type UpdateAgentRolePayload = components['schemas']['UpdateAgentOrganisme']
