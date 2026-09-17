import { screen, waitFor } from '@testing-library/vue'
import { beforeEach, describe, expect, it, vi } from 'vitest'
import { defineComponent, h } from 'vue'
import { getMe } from '@/api/utilisateur'
import { provideSidebar } from '@/composables/ui/useSidebar'
import { BRIANCON_UUID, makeUser, MTE_UUID, ROLE_BRIANCON, ROLE_MTE } from '@/test/fixtures/utilisateur'
import { renderWithApp, setupUser } from '@/test/render'
import CspSidebarOrganisme from './CspSidebarOrganisme.vue'

vi.mock('@/api/utilisateur', () => ({
  getMe: vi.fn(),
}))

const Host = defineComponent({
  setup() {
    provideSidebar({ persistState: false })
    return () => h(CspSidebarOrganisme)
  },
})

function trigger() {
  return screen.queryByRole('button', { name: /Changer d'organisme/ })
}

describe('cspSidebarOrganisme', () => {
  beforeEach(() => {
    vi.mocked(getMe).mockReset()
  })

  it('renders nothing for a staff user without any organisme', async () => {
    vi.mocked(getMe).mockResolvedValue(makeUser([], true))

    await renderWithApp(Host, { route: '/organismes' })
    await waitFor(() => expect(getMe).toHaveBeenCalled())

    expect(trigger()).not.toBeInTheDocument()
  })

  it('shows the organisme carried by the url', async () => {
    vi.mocked(getMe).mockResolvedValue(makeUser([ROLE_MTE, ROLE_BRIANCON]))

    await renderWithApp(Host, { route: `/organismes/${BRIANCON_UUID}/recrutements` })

    expect(await screen.findByRole('button', { name: /Commune de Briançon/ })).toBeInTheDocument()
  })

  it('navigates to the recrutements of the picked organisme', async () => {
    const user = setupUser()
    vi.mocked(getMe).mockResolvedValue(makeUser([ROLE_MTE, ROLE_BRIANCON]))

    const { router } = await renderWithApp(Host, { route: `/organismes/${MTE_UUID}/recrutements` })

    await user.click(await screen.findByRole('button', { name: /Changer d'organisme/ }))
    await user.click(await screen.findByRole('menuitem', { name: 'Commune de Briançon' }))

    await waitFor(() =>
      expect(router.currentRoute.value.path).toBe(`/organismes/${BRIANCON_UUID}/recrutements`),
    )
  })

  it('leaves the route untouched when picking the current organisme', async () => {
    const user = setupUser()
    vi.mocked(getMe).mockResolvedValue(makeUser([ROLE_MTE, ROLE_BRIANCON]))

    const { router } = await renderWithApp(Host, { route: `/organismes/${MTE_UUID}/recrutements/archives` })

    await user.click(await screen.findByRole('button', { name: /Changer d'organisme/ }))
    await user.click(await screen.findByRole('menuitem', { name: 'Ministère de la Transition Écologique' }))

    await waitFor(() => expect(screen.queryAllByRole('menuitem')).toHaveLength(0))
    expect(router.currentRoute.value.path).toBe(`/organismes/${MTE_UUID}/recrutements/archives`)
  })
})
