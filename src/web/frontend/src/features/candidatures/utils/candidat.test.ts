import { describe, expect, it } from 'vitest'
import { formatCandidatNom } from './candidat'

describe('formatCandidatNom', () => {
  it('joins prenom and nom', () => {
    expect(formatCandidatNom({
      uuid: 'eeeeeeee-0001-0001-0001-000000000001',
      prenom: 'Alice',
      nom: 'Dupont',
    })).toBe('Alice Dupont')
  })
})
