import { describe, expect, it } from 'vitest'
import { getInitials, pluralize } from './format'

describe('pluralize', () => {
  it('returns singular form for 0 and 1', () => {
    expect(pluralize(0, 'candidature')).toBe('candidature')
    expect(pluralize(1, 'candidature')).toBe('candidature')
  })

  it('appends "s" by default for counts greater than 1', () => {
    expect(pluralize(2, 'candidature')).toBe('candidatures')
    expect(pluralize(10, 'candidature')).toBe('candidatures')
  })

  it('uses custom plural form when provided', () => {
    expect(pluralize(1, 'sera', 'seront')).toBe('sera')
    expect(pluralize(2, 'sera', 'seront')).toBe('seront')
    expect(pluralize(1, 'sa', 'leur')).toBe('sa')
    expect(pluralize(3, 'sa', 'leur')).toBe('leur')
  })
})

describe('getInitials', () => {
  it('returns null for empty or whitespace input', () => {
    expect(getInitials(null)).toBeNull()
    expect(getInitials(undefined)).toBeNull()
    expect(getInitials('')).toBeNull()
    expect(getInitials('   ')).toBeNull()
  })

  it('returns null when input is only separators', () => {
    expect(getInitials('---')).toBeNull()
    expect(getInitials(' - - ')).toBeNull()
  })

  it('returns first two chars for single word', () => {
    expect(getInitials('Alice')).toBe('AL')
    expect(getInitials('Jo')).toBe('JO')
  })

  it('returns first and last initials for multiple words', () => {
    expect(getInitials('Jean Dupont')).toBe('JD')
    expect(getInitials('Marie-Claire Martin')).toBe('MM')
    expect(getInitials('Jean Pierre Dupont')).toBe('JD')
  })
})
