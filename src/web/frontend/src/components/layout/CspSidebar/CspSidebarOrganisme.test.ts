import { screen } from '@testing-library/vue'
import { beforeEach, describe, expect, it, vi } from 'vitest'
import { defineComponent, h } from 'vue'
import { getMe } from '@/api/utilisateur'
import { provideSidebar } from '@/composables/ui/useSidebar'
import { createLocalStorageMock } from '@/test/browser'
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

function trigger(nom: string) {
  return screen.findByRole('button', { name: `Organisme : ${nom}. Changer d'organisme` })
}

describe('cspSidebarOrganisme', () => {
  beforeEach(() => {
    vi.mocked(getMe).mockReset()
    vi.stubGlobal('localStorage', createLocalStorageMock())
  })

  it('renders nothing for a staff user without any organisme', async () => {
    vi.mocked(getMe).mockResolvedValue(makeUser([], true))

    renderWithApp(Host, { route: '/organismes' })
    await vi.waitFor(() => expect(getMe).toHaveBeenCalled())

    expect(screen.queryByRole('button', { name: /Changer d'organisme/ })).not.toBeInTheDocument()
  })

  it('shows the organisme carried by the url', async () => {
    vi.mocked(getMe).mockResolvedValue(makeUser([ROLE_MTE, ROLE_BRIANCON]))

    await renderWithApp(Host, { route: `/organismes/${BRIANCON_UUID}/recrutements` })

    expect(await trigger(ROLE_BRIANCON.nom)).toHaveTextContent(ROLE_BRIANCON.nom)
  })

  it('navigates to the recrutements of the picked organisme', async () => {
    vi.mocked(getMe).mockResolvedValue(makeUser([ROLE_MTE, ROLE_BRIANCON]))
    const user = setupUser()

    const { router } = await renderWithApp(Host, { route: `/organismes/${MTE_UUID}/recrutements` })

    await user.click(await trigger(ROLE_MTE.nom))
    await user.click(await screen.findByRole('menuitem', { name: ROLE_BRIANCON.nom }))

    await vi.waitFor(() =>
      expect(router.currentRoute.value.path).toBe(`/organismes/${BRIANCON_UUID}/recrutements`),
    )
  })

  it('leaves the route untouched when picking the current organisme', async () => {
    vi.mocked(getMe).mockResolvedValue(makeUser([ROLE_MTE, ROLE_BRIANCON]))
    const user = setupUser()

    const { router } = await renderWithApp(Host, { route: `/organismes/${MTE_UUID}/recrutements/archives` })

    await user.click(await trigger(ROLE_MTE.nom))
    await user.click(await screen.findByRole('menuitem', { name: ROLE_MTE.nom }))

    await vi.waitFor(() => expect(screen.queryByRole('menuitem')).not.toBeInTheDocument())
    expect(router.currentRoute.value.path).toBe(`/organismes/${MTE_UUID}/recrutements/archives`)
  })
})
