import { describe, expect, it } from 'vitest'
import { CANDIDAT_ALICE, CANDIDAT_BRUNO } from '@/test/fixtures/candidatures'
import { etapeOptions, formatCandidatName, formatEtapeChangeTitle } from './format'

describe('formatCandidatName', () => {
  it('joins prenom and nom', () => {
    expect(formatCandidatName({
      uuid: 'eeeeeeee-0001-0001-0001-000000000001',
      prenom: 'Alice',
      nom: 'Dupont',
    })).toBe('Alice Dupont')
  })
})

describe('formatEtapeChangeTitle', () => {
  it('names the candidat when a single candidature moves', () => {
    expect(formatEtapeChangeTitle([CANDIDAT_ALICE], 'Entretien')).toBe('La candidature d\'Alice Dupont est passée à l\'étape Entretien')
    expect(formatEtapeChangeTitle([{ ...CANDIDAT_ALICE, prenom: 'Hélène' }], 'Entretien')).toBe('La candidature d\'Hélène Dupont est passée à l\'étape Entretien')
    expect(formatEtapeChangeTitle([CANDIDAT_BRUNO], 'Entretien')).toBe('La candidature de Bruno Martin est passée à l\'étape Entretien')
  })

  it('counts the candidatures when several move', () => {
    expect(formatEtapeChangeTitle([CANDIDAT_ALICE, CANDIDAT_BRUNO], 'Entretien')).toBe('2 candidatures sont passées à l\'étape Entretien')
  })
})

describe('etapeOptions', () => {
  it('marks the current stage as disabled with a hint', () => {
    expect(etapeOptions([
      { uuid: 'reception', nom: 'Réception des candidatures', categorie: 'ENTREE' },
      { uuid: 'entretien', nom: 'Entretien', categorie: 'EN_COURS' },
    ], 'reception')).toEqual([
      { value: 'reception', label: 'Réception des candidatures', hint: 'Étape actuelle', disabled: true },
      { value: 'entretien', label: 'Entretien', hint: undefined, disabled: false },
    ])
  })
})
