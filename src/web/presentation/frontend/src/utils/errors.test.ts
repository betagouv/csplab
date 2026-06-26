import { describe, expect, it } from 'vitest'
import { parseFieldErrors } from './errors'

describe('parseFieldErrors', () => {
  it('returns {} for invalid inputs and skips DRF meta keys', () => {
    expect(parseFieldErrors(null)).toEqual({})
    expect(parseFieldErrors(undefined)).toEqual({})
    expect(parseFieldErrors('error')).toEqual({})
    expect(parseFieldErrors([1, 2])).toEqual({})
    expect(parseFieldErrors({
      detail: 'global',
      message: 'ignored',
      status: 'error',
      type: 'X',
      email: ['Invalid'],
    })).toEqual({ email: ['Invalid'] })
  })

  it('parses string field values', () => {
    expect(parseFieldErrors({ email: 'Invalid email' })).toEqual({
      email: ['Invalid email'],
    })
  })

  it('reads errors from custom handler details payload', () => {
    expect(parseFieldErrors({
      status: 'error',
      details: {
        email: ['Invalid'],
        name: 'Required',
      },
    })).toEqual({ email: ['Invalid'], name: ['Required'] })
  })
})
