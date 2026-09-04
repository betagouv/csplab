import type { Versant } from '../types'

export const VERSANT_LABELS: Record<Versant, string> = {
  FPE: 'Fonction Publique d\'État',
  FPT: 'Fonction Publique Territoriale',
  FPH: 'Fonction Publique Hospitalière',
}

export const SIRET_LENGTH = 14

export const ROLE_LABELS = {
  responsable: 'Responsable',
  membre: 'Membre',
} as const

export const ORGANISME_TAB_LABELS = {
  membres: 'Membres',
  etapes: 'Étapes de recrutement',
} as const

export type OrganismeTabKey = keyof typeof ORGANISME_TAB_LABELS
