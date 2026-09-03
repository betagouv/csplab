import type { Utilisateur } from '@/api/utilisateur'
import { createPinia } from 'pinia'
import { beforeEach, describe, expect, it, vi } from 'vitest'
import { createMemoryHistory, createRouter } from 'vue-router'
import { getMe } from '@/api/utilisateur'
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
    is_staff: false,
    organisme_roles: organismeRoles,
  }
}

const testRoutes = [
  { path: '/', name: 'home', component: { template: '<div />' } },
  {
    path: '/scope-organisme',
    name: 'scope-organisme',
    component: { template: '<div />' },
    meta: { requiresCurrentOrganisme: true },
  },
  { path: '/libre', name: 'libre', component: { template: '<div />' } },
]

function makeGuardedRouter() {
  const router = createRouter({ history: createMemoryHistory(), routes: testRoutes })
  registerNavigationGuards(router, createPinia())
  return router
}

describe('registerNavigationGuards', () => {
  beforeEach(() => {
    vi.mocked(getMe).mockReset()
  })

  it('lets a user with an organisme reach a scoped route', async () => {
    vi.mocked(getMe).mockResolvedValue(
      makeUser([{ organisme_uuid: ORGANISME_UUID, nom: 'MTE', role: 'membre' }]),
    )
    const router = makeGuardedRouter()

    await router.push({ name: 'scope-organisme' })

    expect(router.currentRoute.value.name).toBe('scope-organisme')
  })

  it('redirects a user without organisme to home', async () => {
    vi.mocked(getMe).mockResolvedValue(makeUser([]))
    const router = makeGuardedRouter()

    await router.push({ name: 'scope-organisme' })

    expect(router.currentRoute.value.name).toBe('home')
  })

  it('does not fetch the user for unguarded routes', async () => {
    const router = makeGuardedRouter()

    await router.push({ name: 'libre' })

    expect(getMe).not.toHaveBeenCalled()
  })
})
