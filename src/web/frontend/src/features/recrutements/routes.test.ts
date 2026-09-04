import { describe, expect, it } from 'vitest'
import { recrutementsListLocation } from './routes'

const ORGANISME_UUID = '00000000-0000-0000-0000-000000000000'

describe('recrutementsListLocation', () => {
  it('points to the archives tab for an archived recrutement', () => {
    expect(recrutementsListLocation(ORGANISME_UUID, true)).toEqual({
      name: 'recrutements-archives',
      params: { organismeUuid: ORGANISME_UUID },
    })
  })

  it('points to the actifs tab for a live recrutement', () => {
    expect(recrutementsListLocation(ORGANISME_UUID, false)).toEqual({
      name: 'recrutements',
      params: { organismeUuid: ORGANISME_UUID },
    })
  })

  it('points to the default tab while the detail is loading', () => {
    expect(recrutementsListLocation(ORGANISME_UUID, undefined)).toEqual({
      name: 'recrutements',
      params: { organismeUuid: ORGANISME_UUID },
    })
  })
})
