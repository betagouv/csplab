import type { components } from '@/types/api'

export type OrganismesList = components['schemas']['OrganismesList']

export type OrganismeDetail = components['schemas']['OrganismeDetail']

export type CreateOrganismePayload = components['schemas']['CreateOrganisme']

export type UpdateOrganismePayload = components['schemas']['UpdateOrganisme']

export type Versant = components['schemas']['VersantEnum']

export type AgentOrganisme = components['schemas']['AgentOrganisme']

export type Role = components['schemas']['RoleEnum']

export type RattacherAgentPayload = components['schemas']['SetAgentRoleOnOrganisme']

export type ModifierAgentPayload = components['schemas']['PatchedUpdateAgentOrganisme']
