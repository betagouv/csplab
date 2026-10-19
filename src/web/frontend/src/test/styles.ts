import { readFileSync } from 'node:fs'
import { dirname, join } from 'node:path'
import { fileURLToPath } from 'node:url'

const STYLES = join(dirname(fileURLToPath(import.meta.url)), '../styles')

// A stylesheet of src/styles without its comments
export function readStyle(file: string): string {
  return readFileSync(join(STYLES, file), 'utf8').replace(/\/\*[\s\S]*?\*\//g, '')
}

export function declaredIn(file: string): Set<string> {
  return new Set([...readStyle(file).matchAll(/(--[\w-]+)\s*:/g)].map(([, name]) => name!))
}
