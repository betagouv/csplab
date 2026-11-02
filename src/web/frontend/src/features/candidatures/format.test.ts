import { describe, expect, it } from 'vitest'
import { formatCandidatName } from './format'

describe('formatCandidatName', () => {
  it('joins prenom and nom', () => {
    expect(formatCandidatName({
      uuid: 'eeeeeeee-0001-0001-0001-000000000001',
      prenom: 'Alice',
      nom: 'Dupont',
    })).toBe('Alice Dupont')
  })
})
