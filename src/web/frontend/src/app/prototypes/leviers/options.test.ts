import { describe, expect, it } from 'vitest'
import { declaredIn } from '@/test/styles'
import * as leviers from './options'

const kitVariables = declaredIn('csp-variables.css')
const dsfrDecisions = declaredIn('dsfr-tokens-decisions.css')

// The option files of each lever folder, without their stories
const folders = import.meta.glob<Record<string, unknown>>(['./chrome/*.ts', './fonds/*.ts', './rayons/*.ts', './ombres/pistes.ts', './mouvement/*.ts', '!./**/*.stories.ts'], { eager: true })

const levers = Object.entries(Object.assign({ ...leviers }, ...Object.values(folders))).filter((entry): entry is [string, leviers.LevierOption[]] => Array.isArray(entry[1]))

describe.each(levers)('%s', (_, options) => {
  it('sets kit variables and DSFR decision tokens only, like a theme', () => {
    const names = options.flatMap(option => Object.keys({ ...option.valeurs, ...option.sombre }))
    expect(names.filter(name => !kitVariables.has(name) && !dsfrDecisions.has(name))).toEqual([])
  })
})
