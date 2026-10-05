import { describe, expect, it } from 'vitest'
import { findCandidaturePosition } from './position'

const SEQUENCE = ['b', 'c', 'd']

describe('findCandidaturePosition', () => {
  it('locates a candidature in the sequence', () => {
    expect(findCandidaturePosition(SEQUENCE, 'c')).toEqual({ index: 1, total: 3, previousUuid: 'b', nextUuid: 'd' })
  })

  it('has no neighbour before the first nor after the last of the sequence', () => {
    expect(findCandidaturePosition(SEQUENCE, 'b')).toMatchObject({ previousUuid: null, nextUuid: 'c' })
    expect(findCandidaturePosition(SEQUENCE, 'd')).toMatchObject({ previousUuid: 'c', nextUuid: null })
  })

  it('returns an unknown position for a candidature absent from the sequence', () => {
    expect(findCandidaturePosition(SEQUENCE, 'masquee')).toBeNull()
  })
})
