import { describe, expect, it } from 'vitest'
import { recrutementsListLocation, recrutementsOriginState } from './routes'

describe('recrutementsListLocation', () => {
  it('points back to the tab the detail was opened from', () => {
    expect(recrutementsListLocation(recrutementsOriginState('archives')))
      .toEqual({ name: 'mes-recrutements-archives' })
  })

  it.each([
    ['no state', undefined],
    ['an unrelated state', { position: 3 }],
    ['a malformed tab', { recrutementsTab: 'onglet-inconnu' }],
  ])('falls back to the default tab with %s', (_, state) => {
    expect(recrutementsListLocation(state)).toEqual({ name: 'mes-recrutements' })
  })
})
