import { readdirSync, readFileSync } from 'node:fs'
import { dirname, join } from 'node:path'
import { fileURLToPath } from 'node:url'
import { describe, expect, it } from 'vitest'

const SRC = join(dirname(fileURLToPath(import.meta.url)), '..')
const OWNER = 'styles/csp-variables.css'

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
