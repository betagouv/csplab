import type { LinearRgb, Oklch } from '../color'
import type { PaletteColor, PaletteRole } from '../palette'
import { deltaEOk, DICHROMACIES, fitChroma, oklchToLinearRgb, simulateDichromacy } from '../color'
import { DEFAULT_PALETTE_COLOR, PALETTE_COLORS, PALETTE_ROLES } from '../palette'

export type Theme = 'light' | 'dark'

export const THEMES: readonly Theme[] = ['light', 'dark']

// OKLCH hue of each key, near the DSFR illustrative color of the same family; grey has none
const HUES: Record<PaletteColor, number | null> = {
  grey: null,
  // blue-cumulus is at 254 and blue France, the color of the filter tag, at 264
  blue: 245,
  teal: 200,
  green: 150,
  yellow: 92,
  // terre-battue, at 43, is too close to red
  orange: 58,
  red: 25,
  pink: 352,
  // glycine, at 330, is too close to pink
  purple: 316,
  brown: 60,
}

// Lightness and chroma of each role; outside sRGB, a color keeps its lightness and hue and loses chroma
const ROLES: Record<Theme, Record<PaletteRole, { lightness: number, chroma: number }>> = {
  light: {
    background: { lightness: 0.92, chroma: 0.045 },
    text: { lightness: 0.42, chroma: 0.1 },
    dot: { lightness: 0.57, chroma: 0.15 },
  },
  dark: {
    background: { lightness: 0.32, chroma: 0.045 },
    text: { lightness: 0.84, chroma: 0.08 },
    dot: { lightness: 0.72, chroma: 0.13 },
  },
}

// Shift of lightness and factor of chroma of a key, in every role of a theme. A light yellow turns khaki
// at the lightness of the other backgrounds; red and purple stand one step darker than their neighbours
// orange and pink, whose light backgrounds are close; brown, a greyed orange, stands away from the page,
// two steps in light, below red, from which deuteranopia keeps only the lightness, and one step in dark.
const ADJUSTMENTS: Partial<Record<PaletteColor, Partial<Record<Theme, { lightness: number, chroma: number }>>>> = {
  yellow: { light: { lightness: 0.02, chroma: 1.4 } },
  red: { light: { lightness: -0.03, chroma: 1 } },
  purple: { light: { lightness: -0.03, chroma: 1 } },
  brown: { light: { lightness: -0.06, chroma: 0.6 }, dark: { lightness: 0.03, chroma: 0.5 } },
}

const SELECTOR = ':root[data-csp-etiquettes=\'kit\']'

function round(value: number): number {
  return Math.round(value * 10000) / 10000
}

function kitColor(color: PaletteColor, role: PaletteRole, theme: Theme): Oklch {
  const hue = HUES[color]
  const { lightness, chroma } = ROLES[theme][role]
  const adjustment = ADJUSTMENTS[color]?.[theme]
  const l = round(lightness + (adjustment?.lightness ?? 0))
  if (hue === null) {
    return { l, c: 0, h: 0 }
  }
  return { l, c: fitChroma(l, round(chroma * (adjustment?.chroma ?? 1)), hue), h: hue }
}

export function kitRgb(color: PaletteColor, role: PaletteRole, theme: Theme): LinearRgb {
  return oklchToLinearRgb(kitColor(color, role, theme))
}

function declarations(theme: Theme): string[] {
  return PALETTE_COLORS.flatMap(color => PALETTE_ROLES.map((role) => {
    const { l, c, h } = kitColor(color, role, theme)
    return `  --csp-palette-${color}-${role}: oklch(${l} ${c} ${h});`
  }))
}

export function kitCss(): string {
  return [
    '/* Written by kit.test.ts from the rule in kit.ts: vitest run src/styles/etiquettes/kit.test.ts --update */',
    `${SELECTOR} {`,
    '  --csp-label-dot-display: block;',
    '  --csp-label-dot-size: 0.5em;',
    '  --csp-label-padding-start: 0.5em;',
    ...declarations('light'),
    '}',
    '',
    `${SELECTOR} .csp-label--md {`,
    '  --csp-label-gap: 0.3125rem;',
    '  --csp-label-white-space: normal;',
    '  align-items: flex-start;',
    '}',
    '',
    `${SELECTOR} .color-field__option .csp-radio__label {`,
    '  display: inline-flex;',
    '  align-items: center;',
    '  gap: 0.3125rem;',
    '  padding: 0.1875rem 0.625rem 0.1875rem 0.5em;',
    '  border-radius: 0.25rem;',
    '  background-color: var(--color-field-background);',
    '  color: var(--color-field-text);',
    '  font-weight: var(--csp-font-weight-medium);',
    '}',
    '',
    `${SELECTOR} .color-field__option .csp-radio__label::before {`,
    '  width: 0.5em;',
    '  height: 0.5em;',
    '  margin-inline-end: 0;',
    '}',
    '',
    `${SELECTOR}[data-fr-theme='dark'] {`,
    ...declarations('dark'),
    '}',
    '',
  ].join('\n')
}

// Smallest OKLab distance between two light backgrounds, in typical vision and in the three dichromacies
function backgroundDistance(first: PaletteColor, second: PaletteColor): number {
  const [a, b] = [kitRgb(first, 'background', 'light'), kitRgb(second, 'background', 'light')]
  return Math.min(deltaEOk(a, b), ...DICHROMACIES.map(type => deltaEOk(simulateDichromacy(a, type), simulateDichromacy(b, type))))
}

// From blue, each next color is the farthest from the colors already proposed
function proposalOrder(): PaletteColor[] {
  const order: PaletteColor[] = [DEFAULT_PALETTE_COLOR]
  const remaining = PALETTE_COLORS.filter(color => color !== DEFAULT_PALETTE_COLOR)
  while (remaining.length > 0) {
    const distance = (color: PaletteColor) => Math.min(...order.map(proposed => backgroundDistance(color, proposed)))
    const farthest = remaining.reduce((best, color) => (distance(color) > distance(best) ? color : best))
    order.push(farthest)
    remaining.splice(remaining.indexOf(farthest), 1)
  }
  return order
}

export const KIT_PROPOSAL_ORDER: readonly PaletteColor[] = proposalOrder()

// Color proposed for a new label: the first color of the order among the least used ones
export function proposeColor(used: readonly PaletteColor[]): PaletteColor {
  const count = (color: PaletteColor) => used.filter(item => item === color).length
  return KIT_PROPOSAL_ORDER.reduce((best, color) => (count(color) < count(best) ? color : best))
}
