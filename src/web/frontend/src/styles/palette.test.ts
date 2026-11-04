import type { LinearRgb } from './color'
import type { Theme } from './palette-rule'
import { readFileSync } from 'node:fs'
import { dirname, join } from 'node:path'
import { fileURLToPath } from 'node:url'
import { describe, expect, it } from 'vitest'
import { contrastRatio, deltaEOk, hexToLinearRgb, isInSrgb } from './color'
import { PALETTE_COLORS, PALETTE_ROLES } from './palette'
import { paletteCss, paletteRgb, THEMES } from './palette-rule'

const STYLES = dirname(fileURLToPath(import.meta.url))

function tokens(file: string): [Map<string, string>, Map<string, string>] {
  const css = readFileSync(join(STYLES, file), 'utf8')
  const [light = '', dark = ''] = css.split(':root[data-fr-theme=\'dark\']')
  const read = (block: string) => new Map([...block.matchAll(/--([\w-]+)\s*:([^;]+);/g)].map(([, name, value]) => [name!, value!.trim()]))
  return [read(light), read(dark)]
}

const [optionsLight, optionsDark] = tokens('dsfr-tokens-options.css')
const [decisions] = tokens('dsfr-tokens-decisions.css')

function dsfrColor(name: string, theme: Theme): LinearRgb {
  const values = new Map([...optionsLight, ...(theme === 'dark' ? optionsDark : []), ...decisions])
  let value = values.get(name)
  while (value?.startsWith('var(')) {
    value = values.get(value.slice('var(--'.length, -1))
  }
  if (!value) {
    throw new Error(`--${name} has no value`)
  }
  return hexToLinearRgb(value)
}

// The surfaces under a label: card and table row, note and kanban column, side panel
const SURFACES = ['background-default-grey', 'background-alt-grey', 'background-overlap-grey']
// Backgrounds of the status badges and of the filter tag
const NEIGHBOURS = ['background-contrast-info', 'background-contrast-success', 'background-contrast-warning', 'background-contrast-error', 'background-contrast-grey', 'background-action-low-blue-france']

const pairs = PALETTE_COLORS.flatMap((first, index) => PALETTE_COLORS.slice(index + 1).map(second => [first, second] as const))

describe('palette', () => {
  it('writes palette.css from the rule', async () => {
    await expect(paletteCss()).toMatchFileSnapshot('./palette.css')
  })

  describe.each(THEMES)('%s theme', (theme) => {
    it.each([...PALETTE_COLORS])('%s stays inside sRGB', (color) => {
      PALETTE_ROLES.forEach(role => expect(isInSrgb(paletteRgb(color, role, theme))).toBe(true))
    })

    it.each([...PALETTE_COLORS])('%s text reaches 4.5:1 and dot 3:1 on the label background', (color) => {
      const background = paletteRgb(color, 'background', theme)
      expect(contrastRatio(paletteRgb(color, 'text', theme), background)).toBeGreaterThanOrEqual(4.5)
      expect(contrastRatio(paletteRgb(color, 'dot', theme), background)).toBeGreaterThanOrEqual(3)
    })

    it.each(SURFACES)('every dot reaches 3:1 on %s', (surface) => {
      PALETTE_COLORS.forEach(color => expect(contrastRatio(paletteRgb(color, 'dot', theme), dsfrColor(surface, theme)), color).toBeGreaterThanOrEqual(3))
    })

    it.each([...PALETTE_ROLES])('two colors differ by 0.02 in OKLab on the %s role', (role) => {
      pairs.forEach(([first, second]) => expect(deltaEOk(paletteRgb(first, role, theme), paletteRgb(second, role, theme)), `${first} ${second}`).toBeGreaterThanOrEqual(0.02))
    })

    it.each(NEIGHBOURS)('every background differs from %s by 0.02 in OKLab', (neighbour) => {
      PALETTE_COLORS.forEach(color => expect(deltaEOk(paletteRgb(color, 'background', theme), dsfrColor(neighbour, theme)), color).toBeGreaterThanOrEqual(0.02))
    })
  })
})
