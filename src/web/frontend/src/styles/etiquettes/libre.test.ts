import { readFileSync } from 'node:fs'
import { dirname, join } from 'node:path'
import { fileURLToPath } from 'node:url'
import { describe, expect, it } from 'vitest'
import { PALETTE_COLORS } from '../palette'

const STYLES = dirname(dirname(fileURLToPath(import.meta.url)))

const read = (path: string) => readFileSync(join(STYLES, path), 'utf8')

const css = read('etiquettes/libre.css')

type Oklab = [number, number, number]

function themeBlock(selector: string): string {
  const start = css.indexOf(`${selector} {`)
  return css.slice(start, css.indexOf('}', start))
}

function oklab(block: string, name: string): Oklab {
  const [, l, c, h] = block.match(new RegExp(`--${name}: oklch\\(([\\d.]+) ([\\d.]+) ([\\d.]+)\\);`)) ?? []
  if (!l || !c || !h) {
    throw new Error(`--${name} is not written in oklch()`)
  }
  const hue = (Number(h) * Math.PI) / 180
  return [Number(l), Number(c) * Math.cos(hue), Number(c) * Math.sin(hue)]
}

const distance = (a: Oklab, b: Oklab) => Math.hypot(a[0] - b[0], a[1] - b[1], a[2] - b[2])

function token(source: string, name: string): string {
  const value = source.match(new RegExp(`--${name}:\\s*([^;]+);`))?.[1]?.trim()
  if (!value) {
    throw new Error(`--${name} has no value`)
  }
  return value
}

const toLinear = (channel: number) => (channel <= 0.04045 ? channel / 12.92 : ((channel + 0.055) / 1.055) ** 2.4)

function luminance(hex: string): number {
  const full = hex.length === 4 ? [...hex.slice(1)].map(c => c + c).join('') : hex.slice(1)
  const [r, g, b] = full.match(/../g)!.map(pair => toLinear(Number.parseInt(pair, 16) / 255))
  return 0.2126 * r! + 0.7152 * g! + 0.0722 * b!
}

function contrast(a: string, b: string) {
  const [high, low] = [luminance(a), luminance(b)].sort((x, y) => y - x)
  return (high! + 0.05) / (low! + 0.05)
}

const [optionsLight, optionsDark] = read('dsfr-tokens-options.css').split(':root[data-fr-theme=\'dark\']') as [string, string]
const decisions = read('dsfr-tokens-decisions.css')
const focusRing = token(read('csp-variables.css'), 'csp-focus-ring-color')

function surface(theme: 'light' | 'dark', name: string): string {
  const option = token(decisions, name).match(/^var\(--([\w-]+)\)$/)![1]!
  return token(theme === 'dark' ? optionsDark : optionsLight, option)
}

const THEMES = {
  light: themeBlock(':root[data-csp-etiquettes=\'libre\']'),
  dark: themeBlock(':root[data-csp-etiquettes=\'libre\'][data-fr-theme=\'dark\']'),
}

// 0.02 is the just noticeable difference of CSS Color 4 in OKLab
const MIN_DISTANCE = { background: 0.035, text: 0.03, dot: 0.1 }

describe.each(Object.entries(THEMES))('libre scenario, %s theme', (theme, block) => {
  it.each(Object.entries(MIN_DISTANCE))('keeps every pair of %s colours apart', (role, min) => {
    const colors = PALETTE_COLORS.map(color => oklab(block, `csp-palette-${color}-${role}`))
    const closest = Math.min(...colors.flatMap((a, i) => colors.slice(i + 1).map(b => distance(a, b))))
    expect(closest).toBeGreaterThanOrEqual(min)
  })

  it('draws a pale fill in light and a deep fill in dark, under the lightest surfaces of the screen', () => {
    const lightness = PALETTE_COLORS.map(color => oklab(block, `csp-palette-${color}-background`)[0])
    if (theme === 'dark') {
      expect(Math.max(...lightness)).toBeLessThanOrEqual(0.4)
    }
    else {
      expect(Math.min(...lightness)).toBeGreaterThanOrEqual(0.86)
    }
  })

  it.each(['background-default-grey', 'background-alt-grey', 'background-overlap-grey'])('draws focus rings that reach 3:1 on %s', (name) => {
    expect(contrast(focusRing, surface(theme as 'light' | 'dark', name))).toBeGreaterThanOrEqual(3)
  })
})
