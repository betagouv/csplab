import type { CspLabelItem } from '@/components/base/CspLabel/types'
import type { PaletteColor } from '@/styles/palette'

// Prototype field: the API serves no labels yet, the Storybook demo data adds them.
export interface Etiquette {
  libelle: string
  couleur: PaletteColor
}

export interface WithEtiquettes {
  etiquettes?: Etiquette[]
}

export function etiquettesOf(item: object): CspLabelItem[] {
  const { etiquettes = [] } = item as WithEtiquettes
  return etiquettes.map(({ libelle, couleur }) => ({ label: libelle, color: couleur }))
}
