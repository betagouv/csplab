import type { Role, Versant } from '../types'
import type { CspRadioGroupOption } from '@/components/base/CspRadioGroup/CspRadioGroup.vue'

export const VERSANT_LABELS: Record<Versant, string> = {
  FPE: 'Fonction Publique d\'État',
  FPT: 'Fonction Publique Territoriale',
  FPH: 'Fonction Publique Hospitalière',
}

export const SIRET_LENGTH = 14

export const ESPACE_ADMINISTRATEUR_LABEL = 'Espace administrateur'
export const ORGANISME_LABEL = 'Organisme'

export const ROLE_LABELS: Record<Role, string> = {
  superviseur: 'Superviseur',
  agent: 'Membre',
}

export const ROLE_OPTIONS: (CspRadioGroupOption & { value: Role })[] = [
  {
    value: 'superviseur',
    label: ROLE_LABELS.superviseur,
    hint: 'Administre son organisme, invite des utilisateurs et attribue les responsables des recrutements.',
  },
  {
    value: 'agent',
    label: ROLE_LABELS.agent,
    hint: 'Accède à l\'espace de l\'organisme et participe aux recrutements auxquels il est rattaché.',
  },
]

export const ORGANISME_TAB_LABELS = {
  membres: 'Membres',
  etapes: 'Étapes de recrutement',
  tags: 'Étiquettes',
} as const

export const ORGANISME_TAB_ICONS = {
  membres: 'ri:group-line',
  etapes: 'ri:route-line',
  tags: 'ri:price-tag-3-line',
} as const

export type OrganismeTabKey = keyof typeof ORGANISME_TAB_LABELS
