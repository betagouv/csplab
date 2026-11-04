import type { RecrutementDetail } from './types'
import { describe, expect, it } from 'vitest'
import { formatLocalisationLabel } from './format'

function makeDetail(labels: string[]): RecrutementDetail {
  return {
    localisations: labels.map(localisation_label => ({ localisation_label })),
  } as unknown as RecrutementDetail
}

describe('formatLocalisationLabel', () => {
  it.each([
    [[], '-'],
    [['Paris'], 'Paris'],
    [['Caen', 'Saint-Lô', 'Alençon'], 'Caen + 2'],
  ])('formats %j as %s', (labels, expected) => {
    expect(formatLocalisationLabel(makeDetail(labels))).toBe(expected)
  })
})
