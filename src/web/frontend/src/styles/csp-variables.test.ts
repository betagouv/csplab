import { readdirSync, readFileSync } from 'node:fs'
import { dirname, join } from 'node:path'
import { fileURLToPath } from 'node:url'
import { describe, expect, it } from 'vitest'
import { UI_AXES } from './uiSettings'

const SRC = join(dirname(fileURLToPath(import.meta.url)), '..')
const OWNER = 'styles/csp-variables.css'
const UI_THEME_SHEETS = { shape: 'styles/shapes.css', density: 'styles/densities.css' } as const satisfies Record<keyof typeof UI_AXES, string>

const sources = readdirSync(SRC, { recursive: true, encoding: 'utf8' })
  .filter(file => /\.(?:vue|ts|css|scss)$/.test(file) && !file.endsWith('.test.ts'))
  .map(file => ({ file, text: readFileSync(join(SRC, file), 'utf8') }))

const withoutComments = (text: string) => text.replace(/\/\*[\s\S]*?\*\//g, '').replace(/^\s*\/\/.*$/gm, '')

const declarations = new Map<string, Set<string>>()
sources.forEach(({ file, text }) => {
  for (const [name] of withoutComments(text).matchAll(/--csp-[\w-]+(?=['"]?\s*:)/g)) {
    declarations.set(name, (declarations.get(name) ?? new Set()).add(file))
  }
})

// A name ending with a hyphen is the prefix of a name built at runtime, such as --csp-palette-${color}
const isDeclared = (name: string) => name.endsWith('-') ? [...declarations.keys()].some(declared => declared.startsWith(name)) : declarations.has(name)

describe('csp variables', () => {
  it('declares every csp variable that a file writes', () => {
    const undeclared = sources.flatMap(({ file, text }) => [...new Set(text.match(/--csp-[\w-]*/g))]
      .filter(name => !isDeclared(name))
      .map(name => `${name} in ${file}: declare it in ${OWNER}, or in the component that owns it`))
    expect(undeclared).toEqual([])
  })

  it('declares the variables of csp-variables.css in the stylesheets of styles/ only', () => {
    const redeclared = [...declarations]
      .filter(([, files]) => files.has(OWNER))
      .flatMap(([name, files]) => [...files].filter(file => !file.startsWith('styles/')).map(file => `${name} in ${file}: ${OWNER} owns this variable`))
    expect(redeclared).toEqual([])
  })
})

interface CssBlock { prelude: string, body: string, open: number, close: number }

function topLevelBlocks(text: string): CssBlock[] {
  const blocks: CssBlock[] = []
  let depth = 0
  let start = 0
  let open = 0
  for (let index = 0; index < text.length; index++) {
    if (text[index] === '{') {
      if (depth === 0) {
        open = index
      }
      depth++
    }
    else if (text[index] === '}') {
      depth--
      if (depth === 0) {
        blocks.push({ prelude: text.slice(start, open).split(';').pop()!.trim(), body: text.slice(open + 1, index), open, close: index })
        start = index + 1
      }
    }
  }
  return blocks
}

function declaredNames(text: string) {
  return [...text.matchAll(/(--[\w-]+)\s*:/g)].map(([, name]) => name!)
}

function ownDeclarations(body: string) {
  const { own, rest } = topLevelBlocks(body).reduce(
    (cut, block) => ({ own: cut.own + body.slice(cut.rest, block.open), rest: block.close + 1 }),
    { own: '', rest: 0 },
  )
  return declaredNames(own + body.slice(rest))
}

const ownerText = withoutComments(readFileSync(join(SRC, OWNER), 'utf8'))
const ownerBlocks = topLevelBlocks(ownerText)
const ownerVariables = new Set(declaredNames(ownerText))
const ownerXxlVariables = new Set(ownerBlocks
  .flatMap(rule => topLevelBlocks(rule.body))
  .filter(block => block.prelude === '@variant xxl')
  .flatMap(block => ownDeclarations(block.body)))
// The dark color mode and the motion media query match with the specificity of a theme selector or below it,
// so a theme sheet imported after csp-variables.css would override them
const ownerContextVariables = new Set(ownerBlocks
  .filter(block => block.prelude !== ':root')
  .flatMap(block => declaredNames(block.body)))

describe.each(Object.entries(UI_THEME_SHEETS))('ui theme sheet of the %s axis', (axis, sheet) => {
  const rules = topLevelBlocks(withoutComments(readFileSync(join(SRC, sheet), 'utf8')))
  const selector = new RegExp(`^:root\\[data-csp-${axis}='[\\w-]+'\\]$`)

  it('applies only under a theme attribute of its axis', () => {
    const misplaced = rules
      .flatMap(rule => [rule.prelude, ...topLevelBlocks(rule.body).map(block => block.prelude).filter(prelude => prelude !== '@variant xxl')])
      .filter(prelude => !selector.test(prelude))
      .map(prelude => `${prelude} in ${sheet}: write the rules of a theme under :root[data-csp-${axis}='…']`)
    expect(misplaced).toEqual([])
  })

  it('has a rule for each value of its axis but the default, and for no other value', () => {
    const [, ...themed] = UI_AXES[axis as keyof typeof UI_AXES].values
    const valued = rules.map(rule => rule.prelude.match(/='([\w-]+)'/)?.[1])
    expect([...valued].sort()).toEqual([...themed].sort())
  })

  it('nests no block inside @variant xxl', () => {
    const nested = rules
      .flatMap(rule => topLevelBlocks(rule.body))
      .flatMap(block => topLevelBlocks(block.body).map(inner => `${inner.prelude} in ${block.prelude} of ${sheet}: write it at the level of @variant xxl`))
    expect(nested).toEqual([])
  })

  it('sets only variables that csp-variables.css declares', () => {
    const unowned = rules
      .flatMap(rule => declaredNames(rule.body))
      .filter(name => !ownerVariables.has(name))
      .map(name => `${name} in ${sheet}: declare it in ${OWNER} first`)
    expect(unowned).toEqual([])
  })

  it('sets at the xxl breakpoint every variable that csp-variables.css sets there', () => {
    const missing = rules.flatMap((rule) => {
      const xxl = new Set(topLevelBlocks(rule.body).filter(block => block.prelude === '@variant xxl').flatMap(block => ownDeclarations(block.body)))
      return ownDeclarations(rule.body)
        .filter(name => ownerXxlVariables.has(name) && !xxl.has(name))
        .map(name => `${name} in ${rule.prelude} of ${sheet}: ${OWNER} sets it again at xxl, so set it in @variant xxl too`)
    })
    expect(missing).toEqual([])
  })

  it('sets no variable that csp-variables.css sets for the dark color mode or a media query', () => {
    const overriding = rules
      .flatMap(rule => declaredNames(rule.body))
      .filter(name => ownerContextVariables.has(name))
      .map(name => `${name} in ${sheet}: ${OWNER} sets it for the dark color mode or a media query, which the theme would override`)
    expect(overriding).toEqual([])
  })
})
