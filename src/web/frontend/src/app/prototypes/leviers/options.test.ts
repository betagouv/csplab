import { describe, expect, it } from 'vitest'
import { declaredIn } from '@/test/styles'
import * as leviers from './options'

const kitVariables = declaredIn('csp-variables.css')
const dsfrDecisions = declaredIn('dsfr-tokens-decisions.css')

const levers = Object.entries(leviers).filter((entry): entry is [string, leviers.LevierOption[]] => Array.isArray(entry[1]))

describe.each(levers)('%s', (_, options) => {
  it('sets kit variables and DSFR decision tokens only, like a theme', () => {
    const names = options.flatMap(option => Object.keys({ ...option.valeurs, ...option.sombre }))
    expect(names.filter(name => !kitVariables.has(name) && !dsfrDecisions.has(name))).toEqual([])
  })
})
