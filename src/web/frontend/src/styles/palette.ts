export const PALETTE_COLORS = [
  'grey',
  'blue',
  'mint',
  'green',
  'yellow',
  'red',
  'orange',
  'beige',
  'pink',
  'purple',
] as const

export type PaletteColor = typeof PALETTE_COLORS[number]

export const PALETTE_ROLES = ['background', 'text', 'dot'] as const

export type PaletteRole = typeof PALETTE_ROLES[number]

export function paletteVar(color: PaletteColor, role: PaletteRole): string {
  return `var(--csp-palette-${color}-${role})`
}
