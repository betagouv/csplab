import { describe, expect, it, vi } from 'vitest'
import { RouterView } from 'vue-router'
import { getMe } from '@/api/utilisateur'
import { BRIANCON_UUID, makeUser, ORGANISME_BRIANCON, ORGANISME_MTE } from '@/test/fixtures/utilisateur'
import { renderWithApp } from '@/test/render'
import { homeLocationFor } from './home'

describe('homeLocationFor', () => {
  it('sends a member to the home of their first organisme', () => {
    expect(homeLocationFor(makeUser([ORGANISME_BRIANCON, ORGANISME_MTE]))).toEqual({
      name: 'organisme-home',
      params: { organismeUuid: BRIANCON_UUID },
    })
  })

  it('sends a staff member to the home of their first organisme', () => {
    expect(homeLocationFor(makeUser([ORGANISME_BRIANCON], true))).toEqual({
      name: 'organisme-home',
      params: { organismeUuid: BRIANCON_UUID },
    })
  })

  it('sends a staff member without organisme to the list of organismes', () => {
    expect(homeLocationFor(makeUser([], true))).toEqual({ name: 'organismes' })
  })

  it('stays on the root without any organisme', () => {
    expect(homeLocationFor(makeUser([]))).toBe(true)
  })
})

describe('root route', () => {
  it('lands a member on the home of their first organisme', async () => {
    vi.mocked(getMe).mockResolvedValue(makeUser([ORGANISME_BRIANCON, ORGANISME_MTE]))

    const { router } = await renderWithApp(RouterView)

    expect(router.currentRoute.value.path).toBe(`/organismes/${BRIANCON_UUID}/accueil`)
  })

  it('stays on the root when the account cannot be loaded', async () => {
    vi.mocked(getMe).mockRejectedValue(new Error('unavailable'))

    const { router } = await renderWithApp(RouterView)

    expect(router.currentRoute.value.path).toBe('/')
  })
})
