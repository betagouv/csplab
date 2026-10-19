import { existsSync, readdirSync, readFileSync } from 'node:fs'
import { dirname, join } from 'node:path'
import { fileURLToPath } from 'node:url'
import { describe, expect, it } from 'vitest'
import { DEFAULT_THEME, THEMES } from './scenarios'

const THEMES_FOLDER = dirname(fileURLToPath(import.meta.url))

// Keyframes keep their own selectors (from, to, percentages): a theme names them, the animation variables scope them
function read(file: string): string {
  return readFileSync(join(THEMES_FOLDER, file), 'utf8')
    .replace(/\/\*[\s\S]*?\*\//g, '')
    .replace(/@keyframes[^{]+\{(?:[^{}]*\{[^{}]*\})*[^{}]*\}/g, '')
}

function selectors(css: string): string[] {
  return [...css.matchAll(/([^{}]+)\{[^{}]*\}/g)].flatMap(([, selector]) => selector!.split(',').map(part => part.trim()))
}

const themeFiles = readdirSync(THEMES_FOLDER)
  .filter(file => file.endsWith('.css') && file !== 'index.css')
  .map(file => file.slice(0, -'.css'.length))
const themeIds = [...new Set([...themeFiles, ...THEMES.map(({ id }) => id)])]

it('applies a listed theme by default, or none', () => {
  expect(DEFAULT_THEME === null || THEMES.some(({ id }) => id === DEFAULT_THEME)).toBe(true)
})

if (themeIds.length > 0) {
  describe.each(themeIds)('theme %s', (theme) => {
    it('is listed in scenarios.ts, imported by index.css and scoped to its attribute', () => {
      expect(existsSync(join(THEMES_FOLDER, `${theme}.css`))).toBe(true)
      expect(THEMES.map(({ id }) => id)).toContain(theme)
      expect(read('index.css')).toContain(`./${theme}.css`)
      const attribute = new RegExp(`\\[data-csp-theme=['"]${theme}['"]\\]`)
      selectors(read(`${theme}.css`)).forEach(selector => expect(selector).toMatch(attribute))
    })
  })
}
