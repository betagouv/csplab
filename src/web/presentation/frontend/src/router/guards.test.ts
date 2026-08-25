import type { Utilisateur } from '@/api/utilisateur'
import { createPinia } from 'pinia'
import { beforeEach, describe, expect, it, vi } from 'vitest'
import { createMemoryHistory, createRouter } from 'vue-router'
import { getMe } from '@/api/utilisateur'
import { routes } from '@/router'
import { registerNavigationGuards } from './guards'

vi.mock('@/api/utilisateur', () => ({
  getMe: vi.fn(),
}))

const ORGANISME_UUID = '11111111-1111-1111-1111-111111111111'

function makeUser(organismeRoles: Utilisateur['organisme_roles']): Utilisateur {
  return {
    email: 'marie.dupont@example.gouv.fr',
    prenom: 'Marie',
    nom: 'Dupont',
    organisme_roles: organismeRoles,
  }
}

function makeGuardedRouter() {
  const router = createRouter({ history: createMemoryHistory(), routes })
  registerNavigationGuards(router, createPinia())
  return router
}

describe('registerNavigationGuards', () => {
  beforeEach(() => {
    vi.mocked(getMe).mockReset()
  })

  it('lets a user with an organisme reach mon-organisme', async () => {
    vi.mocked(getMe).mockResolvedValue(
      makeUser([{ organisme_uuid: ORGANISME_UUID, nom: 'MTE', role: 'membre' }]),
    )
    const router = makeGuardedRouter()

    await router.push({ name: 'mon-organisme' })

    expect(router.currentRoute.value.name).toBe('mon-organisme')
  })

  it('redirects a user without organisme to home', async () => {
    vi.mocked(getMe).mockResolvedValue(makeUser([]))
    const router = makeGuardedRouter()

    await router.push({ name: 'mon-organisme' })

    expect(router.currentRoute.value.name).toBe('home')
  })

  it('does not fetch the user for unguarded routes', async () => {
    const router = makeGuardedRouter()

    await router.push({ name: 'organismes' })

    expect(getMe).not.toHaveBeenCalled()
  })
})
