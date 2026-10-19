export const PALETTE_COLORS = [
  'grey',
  'blue',
  'teal',
  'green',
  'yellow',
  'orange',
  'red',
  'pink',
  'purple',
  'brown',
] as const

export type PaletteColor = typeof PALETTE_COLORS[number]

export const PALETTE_COLOR_NAMES: Record<PaletteColor, string> = {
  grey: 'Gris',
  blue: 'Bleu',
  teal: 'Turquoise',
  green: 'Vert',
  yellow: 'Jaune',
  orange: 'Orange',
  red: 'Rouge',
  pink: 'Rose',
  purple: 'Violet',
  brown: 'Marron',
}

export const DEFAULT_PALETTE_COLOR: PaletteColor = 'blue'

export const PALETTE_ROLES = ['background', 'text', 'dot'] as const

export type PaletteRole = typeof PALETTE_ROLES[number]

export function paletteVar(color: PaletteColor, role: PaletteRole): string {
  return `var(--csp-palette-${color}-${role})`
}
