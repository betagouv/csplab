import type { LinearRgb, Oklch } from './color'
import type { PaletteColor, PaletteRole } from './palette'
import { fitChroma, oklchToLinearRgb } from './color'
import { PALETTE_COLORS, PALETTE_ROLES } from './palette'

export type Theme = 'light' | 'dark'

export const THEMES: readonly Theme[] = ['light', 'dark']

const HUES: Record<PaletteColor, number | null> = {
  grey: null,
  // blue France, the color of the filter tag, is at 264
  blue: 245,
  mint: 182,
  green: 150,
  yellow: 92,
  red: 25,
  orange: 58,
  beige: 75,
  pink: 352,
  purple: 316,
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

// Shift of lightness and factor of chroma of a color in every role of a theme. At the lightness of the other
// backgrounds, a light yellow turns khaki. Red and purple are 0.03 darker than orange and pink, whose light
// backgrounds are close. Beige has half the chroma of the other colors and is 0.03 darker in light theme,
// 0.03 lighter in dark theme.
const ADJUSTMENTS: Partial<Record<PaletteColor, Partial<Record<Theme, { lightness: number, chroma: number }>>>> = {
  yellow: { light: { lightness: 0.02, chroma: 1.4 } },
  red: { light: { lightness: -0.03, chroma: 1 } },
  purple: { light: { lightness: -0.03, chroma: 1 } },
  beige: { light: { lightness: -0.03, chroma: 0.5 }, dark: { lightness: 0.03, chroma: 0.5 } },
}

function round(value: number): number {
  return Math.round(value * 10000) / 10000
}

function paletteColor(color: PaletteColor, role: PaletteRole, theme: Theme): Oklch {
  const hue = HUES[color]
  const { lightness, chroma } = ROLES[theme][role]
  const adjustment = ADJUSTMENTS[color]?.[theme]
  const l = round(lightness + (adjustment?.lightness ?? 0))
  if (hue === null) {
    return { l, c: 0, h: 0 }
  }
  return { l, c: fitChroma(l, round(chroma * (adjustment?.chroma ?? 1)), hue), h: hue }
}

export function paletteRgb(color: PaletteColor, role: PaletteRole, theme: Theme): LinearRgb {
  return oklchToLinearRgb(paletteColor(color, role, theme))
}

function declarations(theme: Theme): string[] {
  return PALETTE_COLORS.flatMap(color => PALETTE_ROLES.map((role) => {
    const { l, c, h } = paletteColor(color, role, theme)
    return `  --csp-palette-${color}-${role}: oklch(${l} ${c} ${h});`
  }))
}

export function paletteCss(): string {
  return [
    '/* Written by palette.test.ts from the rule in palette-rule.ts: vitest run src/styles/palette.test.ts --update */',
    ':root {',
    ...declarations('light'),
    '}',
    '',
    ':root[data-fr-theme=\'dark\'] {',
    ...declarations('dark'),
    '}',
    '',
  ].join('\n')
}
