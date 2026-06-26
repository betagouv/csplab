import { describe, expect, it } from 'vitest'
import { getInitials } from './format'

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
