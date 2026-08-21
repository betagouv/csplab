import { describe, expect, it } from 'vitest'
import { isSiretValid } from './siret'

describe('isSiretValid', () => {
  it('accepts a siret with a valid checksum', () => {
    expect(isSiretValid('11004601800021')).toBe(true)
  })

  it('accepts a La Poste siret despite its invalid checksum', () => {
    expect(isSiretValid('35600000012345')).toBe(true)
  })

  it('rejects a siret with an invalid checksum', () => {
    expect(isSiretValid('12345671234567')).toBe(false)
  })

  it('rejects a siret with a wrong length or non-digit characters', () => {
    expect(isSiretValid('123456712')).toBe(false)
    expect(isSiretValid('1100460180001a')).toBe(false)
  })
})
