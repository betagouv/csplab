import type { LinearRgb } from './color'
import type { PaletteColor, PaletteRole } from './palette'
import { existsSync, readdirSync, readFileSync } from 'node:fs'
import { dirname, join } from 'node:path'
import { fileURLToPath } from 'node:url'
import { describe, expect, it } from 'vitest'
import { contrastRatio, deltaEOk } from './color'
import { SCENARIOS } from './etiquettes/scenarios'
import { PALETTE_COLORS } from './palette'

const STYLES = dirname(fileURLToPath(import.meta.url))

const read = (path: string) => readFileSync(join(STYLES, path), 'utf8').replace(/\/\*[\s\S]*?\*\//g, '')

function declarations(css: string): Map<string, string> {
  return new Map([...css.matchAll(/--([\w-]+)\s*:([^;]+);/g)].map(([, name, value]) => [name!, value!.trim()]))
}

function blocks(css: string): { selector: string, body: string }[] {
  return [...css.matchAll(/([^{}]+)\{([^{}]*)\}/g)].map(([, selector, body]) => ({ selector: selector!.trim(), body: body! }))
}

type Theme = 'light' | 'dark'

const THEMES: Theme[] = ['light', 'dark']

const [optionsLight, optionsDark] = read('./dsfr-tokens-options.css').split(':root[data-fr-theme=\'dark\']') as [string, string]
const decisions = declarations(read('./dsfr-tokens-decisions.css'))
const fallback = declarations(read('./palette.css'))

const scenarioFiles = readdirSync(join(STYLES, 'etiquettes'))
  .filter(file => file.endsWith('.css') && file !== 'index.css')
  .map(file => file.slice(0, -'.css'.length))
const scenarioIds = [...new Set([...scenarioFiles, ...SCENARIOS.map(({ id }) => id)])]

function scenarioAttribute(id: string): RegExp {
  return new RegExp(`\\[data-csp-etiquettes=['"]${id}['"]\\]`)
}

function valuesFor(theme: Theme, scenario?: string): Map<string, string> {
  const values = new Map([...declarations(optionsLight), ...decisions, ...fallback])
  if (theme === 'dark') {
    declarations(optionsDark).forEach((value, name) => values.set(name, value))
  }
  if (scenario) {
    const rules = blocks(read(`./etiquettes/${scenario}.css`)).filter(({ selector }) => scenarioAttribute(scenario).test(selector))
    const isDark = (selector: string) => selector.includes('data-fr-theme')
    for (const { body } of [...rules.filter(({ selector }) => !isDark(selector)), ...(theme === 'dark' ? rules.filter(({ selector }) => isDark(selector)) : [])]) {
      declarations(body).forEach((value, name) => values.set(name, value))
    }
  }
  return values
}

function resolve(values: Map<string, string>, name: string): string {
  let value = values.get(name)
  for (let depth = 0; value?.startsWith('var(') && depth < 10; depth += 1) {
    const [, reference, fallbackValue] = value.match(/^var\(--([\w-]+)\s*(?:,(.+))?\)$/) ?? []
    value = values.get(reference!) ?? fallbackValue?.trim()
  }
  if (!value) {
    throw new Error(`--${name} has no value`)
  }
  return value
}

const toLinear = (channel: number) => (channel <= 0.04045 ? channel / 12.92 : ((channel + 0.055) / 1.055) ** 2.4)

// Linear sRGB channels and alpha of a hex, rgb() or oklch() color
function parseColor(color: string): [number, number, number, number] {
  const hex = color.match(/^#([\da-f]{3,8})$/i)?.[1]
  if (hex) {
    const full = hex.length <= 4 ? [...hex].map(c => c + c).join('') : hex
    const [r, g, b, a = 255] = full.match(/../g)!.map(pair => Number.parseInt(pair, 16))
    return [toLinear(r! / 255), toLinear(g! / 255), toLinear(b! / 255), a / 255]
  }
  const rgb = color.match(/^rgba?\(([^)]+)\)$/i)?.[1]
  if (rgb) {
    const [r, g, b, a = '1'] = rgb.split(/[\s,/]+/).filter(Boolean)
    const alpha = a.endsWith('%') ? Number.parseFloat(a) / 100 : Number.parseFloat(a)
    return [toLinear(Number(r) / 255), toLinear(Number(g) / 255), toLinear(Number(b) / 255), alpha]
  }
  const oklch = color.match(/^oklch\(([^)]+)\)$/i)?.[1]
  if (oklch) {
    const [l, c, h, a = '1'] = oklch.split(/[\s/]+/).filter(Boolean)
    const lightness = l!.endsWith('%') ? Number.parseFloat(l!) / 100 : Number(l)
    const hue = (Number.parseFloat(h!) * Math.PI) / 180
    const [oa, ob] = [Number(c) * Math.cos(hue), Number(c) * Math.sin(hue)]
    const lms = [
      (lightness + 0.3963377774 * oa + 0.2158037573 * ob) ** 3,
      (lightness - 0.1055613458 * oa - 0.0638541728 * ob) ** 3,
      (lightness - 0.0894841775 * oa - 1.291485548 * ob) ** 3,
    ] as const
    const clamp = (value: number) => Math.min(1, Math.max(0, value))
    return [
      clamp(4.0767416621 * lms[0] - 3.3077115913 * lms[1] + 0.2309699292 * lms[2]),
      clamp(-1.2684380046 * lms[0] + 2.6097574011 * lms[1] - 0.3413193965 * lms[2]),
      clamp(-0.0041960863 * lms[0] - 0.7034186147 * lms[1] + 1.707614701 * lms[2]),
      a.endsWith('%') ? Number.parseFloat(a) / 100 : Number.parseFloat(a),
    ]
  }
  throw new Error(`${color}: write the colors of a scenario in hex, rgb() or oklch()`)
}

// A translucent color is composed over the surface, the default background of the theme unless given
function rgbOf(values: Map<string, string>, name: string, surface = 'background-default-grey'): LinearRgb {
  const [r, g, b, alpha] = parseColor(resolve(values, name))
  const [sr, sg, sb] = parseColor(resolve(values, surface))
  return [r * alpha + sr * (1 - alpha), g * alpha + sg * (1 - alpha), b * alpha + sb * (1 - alpha)]
}

function ratio(values: Map<string, string>, foreground: string, background: string): number {
  return contrastRatio(rgbOf(values, foreground), rgbOf(values, background))
}

function contrast(values: Map<string, string>, color: PaletteColor): number {
  return ratio(values, `csp-palette-${color}-text`, `csp-palette-${color}-background`)
}

const PAIRS = PALETTE_COLORS.flatMap((first, index) => PALETTE_COLORS.slice(index + 1).map(second => [first, second] as const))

// Pairs of colors closer than the distance on the role, among the given ones, where they differ most
function closePairs(values: Map<string, string>, roles: PaletteRole[], distance: number): string[] {
  const roleDistance = (first: PaletteColor, second: PaletteColor, role: PaletteRole) =>
    deltaEOk(rgbOf(values, `csp-palette-${first}-${role}`), rgbOf(values, `csp-palette-${second}-${role}`))
  return PAIRS
    .filter(([first, second]) => Math.max(...roles.map(role => roleDistance(first, second, role))) < distance)
    .map(pair => pair.join('/'))
}

// A dot outlined in the text color takes the contrast of the dot or of its outline
function dotContrast(values: Map<string, string>, color: PaletteColor): number {
  const surface = 'background-overlap-grey'
  const outlined = Number.parseFloat(values.get('csp-label-dot-border-width') ?? '0') > 0
  const roles: PaletteRole[] = outlined ? ['dot', 'text'] : ['dot']
  return Math.max(...roles.map(role => contrastRatio(rgbOf(values, `csp-palette-${color}-${role}`, surface), rgbOf(values, surface, surface))))
}

describe('palette fallback', () => {
  describe.each(THEMES)('%s theme', (theme) => {
    it.each([...PALETTE_COLORS])('%s text reaches 4.5:1 on its background', (color) => {
      expect(contrast(valuesFor(theme), color)).toBeGreaterThanOrEqual(4.5)
    })
  })
})

if (scenarioIds.length > 0) {
  describe.each(scenarioIds)('scenario %s', (scenario) => {
    const { backgroundOrTextDistance, lightBackgroundDistance, darkTextDistance, dotContrast: minDotContrast } = SCENARIOS.find(({ id }) => id === scenario)?.checks ?? {}
    const declaresRemoveStates = PALETTE_COLORS.some(color => valuesFor('light', scenario).has(`csp-palette-${color}-background-hover`))

    it('is listed in scenarios.ts, imported by index.css and scoped to its attribute', () => {
      expect(existsSync(join(STYLES, 'etiquettes', `${scenario}.css`))).toBe(true)
      expect(SCENARIOS.map(({ id }) => id)).toContain(scenario)
      expect(read('./etiquettes/index.css')).toContain(`./${scenario}.css`)
      for (const { selector } of blocks(read(`./etiquettes/${scenario}.css`))) {
        selector.split(',').forEach(part => expect(part).toMatch(scenarioAttribute(scenario)))
      }
    })

    describe.each(THEMES)('%s theme', (theme) => {
      it.each([...PALETTE_COLORS])('%s text reaches 4.5:1 on its background', (color) => {
        expect(contrast(valuesFor(theme, scenario), color)).toBeGreaterThanOrEqual(4.5)
      })

      if (declaresRemoveStates) {
        it.each([...PALETTE_COLORS])('%s remove icon reaches 3:1 on the hover and active backgrounds that the palette declares', (color) => {
          const values = valuesFor(theme, scenario)
          const icon = values.has('csp-label-remove-state-color') ? 'csp-label-remove-state-color' : `csp-palette-${color}-text`
          for (const state of ['hover', 'active']) {
            if (values.has(`csp-palette-${color}-background-${state}`)) {
              expect(ratio(values, icon, `csp-palette-${color}-background-${state}`)).toBeGreaterThanOrEqual(3)
            }
          }
        })
      }

      if (minDotContrast !== undefined) {
        it.each([...PALETTE_COLORS])('%s dot, or its outline, reaches the contrast of the scenario on the overlap background', (color) => {
          expect(dotContrast(valuesFor(theme, scenario), color)).toBeGreaterThanOrEqual(minDotContrast)
        })
      }

      if (backgroundOrTextDistance !== undefined) {
        it('separates any two colors by their background or their text', () => {
          expect(closePairs(valuesFor(theme, scenario), ['background', 'text'], backgroundOrTextDistance)).toEqual([])
        })
      }
    })

    if (lightBackgroundDistance !== undefined) {
      it('separates the backgrounds of any two colors in light theme', () => {
        expect(closePairs(valuesFor('light', scenario), ['background'], lightBackgroundDistance)).toEqual([])
      })
    }

    if (darkTextDistance !== undefined) {
      it('separates the texts of any two colors in dark theme', () => {
        expect(closePairs(valuesFor('dark', scenario), ['text'], darkTextDistance)).toEqual([])
      })
    }
  })
}
