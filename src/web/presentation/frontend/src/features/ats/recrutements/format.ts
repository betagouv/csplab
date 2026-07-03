import type { TypeContrat } from './types'

export const TYPE_CONTRAT_LABELS = {
  TITULAIRE_CONTRACTUEL: 'Titulaire et contractuel',
  CONTRACTUELS: 'Contractuels',
  TERRITORIAL: 'Territorial',
} satisfies Record<TypeContrat, string>
