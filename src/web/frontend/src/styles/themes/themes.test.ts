import { readFileSync } from 'node:fs'
import { dirname, join } from 'node:path'
import { fileURLToPath } from 'node:url'
import { describe, expect, it } from 'vitest'
import { UI_THEMES } from '@/composables/ui/useUiTheme'

const STYLES = join(dirname(fileURLToPath(import.meta.url)), '..')

function read(file: string): string {
  return readFileSync(join(STYLES, file), 'utf8').replace(/\/\*[\s\S]*?\*\//g, '')
}

function declaredIn(file: string): Set<string> {
  return new Set([...read(file).matchAll(/(--[\w-]+)\s*:/g)].map(([, name]) => name!))
}

const kitVariables = declaredIn('csp-variables.css')
const dsfrDecisions = declaredIn('dsfr-tokens-decisions.css')
const themeIds = UI_THEMES.map(({ id }) => id).filter(id => id !== 'kit')

describe.each(themeIds)('theme %s', (id) => {
  const css = read(`themes/${id}.css`)

  it('is imported by themes/index.css', () => {
    expect(read('themes/index.css')).toContain(`./${id}.css`)
  })

  it('applies to the root of the page only', () => {
    const selectors = [...css.matchAll(/([^{};]+)\{/g)].map(([, selector]) => selector!.trim()).filter(selector => !selector.startsWith('@media'))
    selectors.forEach(selector => expect(selector).toMatch(new RegExp(`^:root\\[data-csp-theme='${id}'\\]`)))
  })

  it('redefines kit variables, DSFR decision tokens and its own values only', () => {
    const redefined = [...css.matchAll(/(--[\w-]+)\s*:/g)].map(([, name]) => name!)
    const others = redefined.filter(name => !kitVariables.has(name) && !dsfrDecisions.has(name) && !name.startsWith(`--${id}-`))
    expect(others).toEqual([])
  })
})
