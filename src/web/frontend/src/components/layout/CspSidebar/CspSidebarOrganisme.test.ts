import type { Utilisateur } from '@/api/utilisateur'
import { PiniaColada } from '@pinia/colada'
import { mount } from '@vue/test-utils'
import { createPinia } from 'pinia'
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest'
import { defineComponent, h } from 'vue'
import { createMemoryHistory, createRouter } from 'vue-router'
import { getMe } from '@/api/utilisateur'
import { provideSidebar } from '@/composables/ui/useSidebar'
import { routes } from '@/router'
import CspSidebarOrganisme from './CspSidebarOrganisme.vue'

vi.mock('@/api/utilisateur', () => ({
  getMe: vi.fn(),
}))

function createLocalStorageMock() {
  const storage = new Map<string, string>()

  return {
    getItem: (key: string) => storage.get(key) ?? null,
    setItem: (key: string, value: string) => storage.set(key, value),
    removeItem: (key: string) => storage.delete(key),
    clear: () => storage.clear(),
  }
}

const MTE = 'a1a1a1a1-a1a1-a1a1-a1a1-a1a1a1a1a1a1'
const BRIANCON = 'b2b2b2b2-b2b2-b2b2-b2b2-b2b2b2b2b2b2'

const ROLE_MTE = { organisme_uuid: MTE, nom: 'Ministère de la Transition Écologique', role: 'responsable' }
const ROLE_BRIANCON = { organisme_uuid: BRIANCON, nom: 'Commune de Briançon', role: 'membre' }

function makeUser(organismeRoles: Utilisateur['organisme_roles'], isStaff = false): Utilisateur {
  return {
    email: 'marie.dupont@example.gouv.fr',
    prenom: 'Marie',
    nom: 'Dupont',
    is_staff: isStaff,
    organisme_roles: organismeRoles,
  }
}

async function mountAt(path: string) {
  const router = createRouter({ history: createMemoryHistory(), routes })
  await router.push(path)

  const Wrapper = defineComponent({
    setup() {
      provideSidebar({ persistState: false })
      return () => h(CspSidebarOrganisme)
    },
  })

  mount(Wrapper, {
    attachTo: document.body,
    global: {
      plugins: [createPinia(), PiniaColada, router],
    },
  })

  return router
}

function trigger() {
  return document.querySelector<HTMLButtonElement>('.csp-sidebar-organisme')
}

function menuItems() {
  return [...document.querySelectorAll<HTMLElement>('.csp-dropdown__item')]
}

describe('cspSidebarOrganisme', () => {
  beforeEach(() => {
    vi.mocked(getMe).mockReset()
    vi.stubGlobal('localStorage', createLocalStorageMock())
  })

  afterEach(() => {
    vi.unstubAllGlobals()
    document.body.innerHTML = ''
  })

  it('renders nothing for a staff user without any organisme', async () => {
    vi.mocked(getMe).mockResolvedValue(makeUser([], true))

    await mountAt('/organismes')
    await vi.waitFor(() => expect(getMe).toHaveBeenCalled())

    expect(trigger()).toBeNull()
  })

  it('shows the organisme carried by the url', async () => {
    vi.mocked(getMe).mockResolvedValue(makeUser([ROLE_MTE, ROLE_BRIANCON]))

    await mountAt(`/organismes/${BRIANCON}/recrutements`)

    await vi.waitFor(() =>
      expect(trigger()?.textContent).toContain('Commune de Briançon'),
    )
  })

  it('navigates to the recrutements of the picked organisme', async () => {
    vi.mocked(getMe).mockResolvedValue(makeUser([ROLE_MTE, ROLE_BRIANCON]))

    const router = await mountAt(`/organismes/${MTE}/recrutements`)
    await vi.waitFor(() => expect(trigger()).not.toBeNull())

    trigger()!.click()
    await vi.waitFor(() => expect(menuItems()).toHaveLength(2))

    menuItems()[1]!.click()

    await vi.waitFor(() =>
      expect(router.currentRoute.value.path).toBe(`/organismes/${BRIANCON}/recrutements`),
    )
  })

  it('leaves the route untouched when picking the current organisme', async () => {
    vi.mocked(getMe).mockResolvedValue(makeUser([ROLE_MTE, ROLE_BRIANCON]))

    const router = await mountAt(`/organismes/${MTE}/recrutements/archives`)
    await vi.waitFor(() => expect(trigger()).not.toBeNull())

    trigger()!.click()
    await vi.waitFor(() => expect(menuItems()).toHaveLength(2))

    menuItems()[0]!.click()
    await vi.waitFor(() => expect(menuItems()).toHaveLength(0))

    expect(router.currentRoute.value.path).toBe(`/organismes/${MTE}/recrutements/archives`)
  })
})
