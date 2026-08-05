import { describe, expect, it } from 'vitest'
import { recrutementsListLocation } from './routes'

describe('recrutementsListLocation', () => {
  it('points to the archives tab for an archived recrutement', () => {
    expect(recrutementsListLocation(true)).toEqual({ name: 'mes-recrutements-archives' })
  })

  it('points to the actifs tab for a live recrutement', () => {
    expect(recrutementsListLocation(false)).toEqual({ name: 'mes-recrutements' })
  })

  it('points to the default tab while the detail is loading', () => {
    expect(recrutementsListLocation(undefined)).toEqual({ name: 'mes-recrutements' })
  })
})
