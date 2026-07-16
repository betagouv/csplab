import { describe, expect, it } from 'vitest'
import { normalizeSearchText } from './search'

describe('normalizeSearchText', () => {
  it('lowercases and strips diacritics', () => {
    expect(normalizeSearchText('Chargé de MISSION')).toBe('charge de mission')
    expect(normalizeSearchText('Élise Lefèvre')).toBe('elise lefevre')
  })

  it('keeps plain text untouched', () => {
    expect(normalizeSearchText('dupont')).toBe('dupont')
  })
})
