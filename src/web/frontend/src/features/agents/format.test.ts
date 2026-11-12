import { describe, expect, it } from 'vitest'
import { agentSearchKeys } from './format'

describe('agentSearchKeys', () => {
  it('finds an agent by first name then last name, last name then first name, or email', () => {
    expect(agentSearchKeys({
      prenom: 'Jeanne',
      nom: 'Dupont',
      email: 'jeanne.dupont@example.gouv.fr',
    })).toEqual(['Jeanne Dupont', 'Dupont Jeanne', 'jeanne.dupont@example.gouv.fr'])
  })
})
