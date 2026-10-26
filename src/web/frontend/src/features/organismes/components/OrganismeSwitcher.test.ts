import { screen } from '@testing-library/vue'
import { beforeEach, describe, expect, it, vi } from 'vitest'
import { defineComponent, h } from 'vue'
import { getMe } from '@/api/utilisateur'
import { provideSidebar } from '@/composables/ui/useSidebar'
import { createLocalStorageMock } from '@/test/browser'
import { ORGANISME } from '@/test/fixtures/organismes'
import { BRIANCON_UUID, makeUser, MTE_UUID, ROLE_BRIANCON, ROLE_MTE } from '@/test/fixtures/utilisateur'
import { renderWithApp, setupUser } from '@/test/render'
import { getOrganismesList } from '../api'
import OrganismeSwitcher from './OrganismeSwitcher.vue'

vi.mock('@/api/utilisateur', () => ({
  getMe: vi.fn(),
}))

vi.mock('../api', () => ({
  getOrganismesList: vi.fn(),
}))

const Host = defineComponent({
  setup() {
    provideSidebar({ persistState: false })
    return () => h(OrganismeSwitcher)
  },
})

function organismeTrigger(nom: string) {
  return screen.findByRole('button', { name: `Organisme : ${nom}. Changer d'organisme` })
}

function espaceTrigger(nom: string) {
  return screen.findByRole('button', { name: `${nom}. Changer d'espace` })
}

describe('organismeSwitcher', () => {
  beforeEach(() => {
    vi.mocked(getMe).mockReset()
    vi.mocked(getOrganismesList).mockReset().mockResolvedValue([ORGANISME])
    vi.stubGlobal('localStorage', createLocalStorageMock())
  })

  describe('for a superviseur or an agent', () => {
    it('shows the name of a single organisme without any menu', async () => {
      vi.mocked(getMe).mockResolvedValue(makeUser([ROLE_MTE]))

      await renderWithApp(Host, { route: `/organismes/${MTE_UUID}/recrutements` })

      expect(await screen.findByText(ROLE_MTE.nom)).toBeInTheDocument()
      expect(screen.queryByRole('button')).not.toBeInTheDocument()
    })

    it('shows the organisme carried by the url', async () => {
      vi.mocked(getMe).mockResolvedValue(makeUser([ROLE_MTE, ROLE_BRIANCON]))

      await renderWithApp(Host, { route: `/organismes/${BRIANCON_UUID}/recrutements` })

      expect(await organismeTrigger(ROLE_BRIANCON.nom)).toHaveTextContent(ROLE_BRIANCON.nom)
    })

    it('lists their organismes, without the administrator space nor the search', async () => {
      vi.mocked(getMe).mockResolvedValue(makeUser([ROLE_MTE, ROLE_BRIANCON]))
      const user = setupUser()

      await renderWithApp(Host, { route: `/organismes/${MTE_UUID}/recrutements` })
      await user.click(await organismeTrigger(ROLE_MTE.nom))

      expect(screen.getAllByRole('option').map(option => option.textContent)).toEqual([ROLE_MTE.nom, ROLE_BRIANCON.nom])
      expect(screen.queryByRole('searchbox')).not.toBeInTheDocument()
      expect(getOrganismesList).not.toHaveBeenCalled()
    })

    it('navigates to the recrutements of the picked organisme', async () => {
      vi.mocked(getMe).mockResolvedValue(makeUser([ROLE_MTE, ROLE_BRIANCON]))
      const user = setupUser()

      const { router } = await renderWithApp(Host, { route: `/organismes/${MTE_UUID}/recrutements` })

      await user.click(await organismeTrigger(ROLE_MTE.nom))
      await user.click(await screen.findByRole('option', { name: ROLE_BRIANCON.nom }))

      await vi.waitFor(() =>
        expect(router.currentRoute.value.path).toBe(`/organismes/${BRIANCON_UUID}/recrutements`),
      )
    })

    it('leaves the route untouched when picking the current organisme', async () => {
      vi.mocked(getMe).mockResolvedValue(makeUser([ROLE_MTE, ROLE_BRIANCON]))
      const user = setupUser()

      const { router } = await renderWithApp(Host, { route: `/organismes/${MTE_UUID}/recrutements/archives` })

      await user.click(await organismeTrigger(ROLE_MTE.nom))
      await user.click(await screen.findByRole('option', { name: ROLE_MTE.nom }))

      await vi.waitFor(() => expect(screen.queryByRole('option')).not.toBeInTheDocument())
      expect(router.currentRoute.value.path).toBe(`/organismes/${MTE_UUID}/recrutements/archives`)
    })
  })

  describe('for a staff user', () => {
    it('shows the administrator space outside any organisme, with the organismes they belong to', async () => {
      vi.mocked(getMe).mockResolvedValue(makeUser([ROLE_MTE], true))
      const user = setupUser()

      await renderWithApp(Host, { route: '/organismes' })
      await user.click(await espaceTrigger('Espace administrateur'))

      expect(screen.getByRole('option', { name: 'Espace administrateur' })).toHaveAttribute('aria-selected', 'true')
      expect(screen.getByRole('group', { name: 'Membre de' })).toHaveTextContent(ROLE_MTE.nom)
    })

    it('names an organisme they do not belong to', async () => {
      vi.mocked(getMe).mockResolvedValue(makeUser([], true))

      await renderWithApp(Host, { route: `/organismes/${ORGANISME.uuid}/recrutements` })

      expect(await espaceTrigger(ORGANISME.nom)).toBeInTheDocument()
    })

    it('keeps the switcher while the name of an organisme they do not belong to is unknown', async () => {
      vi.mocked(getMe).mockResolvedValue(makeUser([], true))
      vi.mocked(getOrganismesList).mockReturnValue(new Promise(() => {}))

      await renderWithApp(Host, { route: `/organismes/${ORGANISME.uuid}/recrutements` })

      expect(await espaceTrigger('Organisme')).toBeInTheDocument()
    })

    it('clears the search when the menu closes', async () => {
      vi.mocked(getMe).mockResolvedValue(makeUser([ROLE_MTE], true))
      const user = setupUser()

      await renderWithApp(Host, { route: '/organismes' })
      await user.click(await espaceTrigger('Espace administrateur'))
      await user.type(screen.getByRole('searchbox', { name: 'Accéder à un organisme' }), 'introuvable')
      await user.keyboard('{Escape}')
      await user.click(await espaceTrigger('Espace administrateur'))

      expect(screen.getByRole('searchbox', { name: 'Accéder à un organisme' })).toHaveValue('')
    })

    it('enters an organisme found by its SIRET with the Enter key', async () => {
      vi.mocked(getMe).mockResolvedValue(makeUser([ROLE_MTE], true))
      const user = setupUser()

      const { router } = await renderWithApp(Host, { route: '/organismes' })
      await user.click(await espaceTrigger('Espace administrateur'))
      await user.type(screen.getByRole('searchbox', { name: 'Accéder à un organisme' }), `${ORGANISME.siret.slice(0, 6)}{Enter}`)

      await vi.waitFor(() =>
        expect(router.currentRoute.value.path).toBe(`/organismes/${ORGANISME.uuid}/recrutements`),
      )
    })

    it('says when no organisme matches the search', async () => {
      vi.mocked(getMe).mockResolvedValue(makeUser([], true))
      const user = setupUser()

      await renderWithApp(Host, { route: '/organismes' })
      await user.click(await espaceTrigger('Espace administrateur'))
      await user.type(screen.getByRole('searchbox', { name: 'Accéder à un organisme' }), 'introuvable')

      await vi.waitFor(() => expect(screen.getByRole('status')).toHaveTextContent('Aucun organisme trouvé'))
    })

    it('goes back to the administrator space from an organisme', async () => {
      vi.mocked(getMe).mockResolvedValue(makeUser([ROLE_MTE], true))
      const user = setupUser()

      const { router } = await renderWithApp(Host, { route: `/organismes/${MTE_UUID}/recrutements` })
      await user.click(await espaceTrigger(ROLE_MTE.nom))
      await user.click(screen.getByRole('option', { name: 'Espace administrateur' }))

      await vi.waitFor(() => expect(router.currentRoute.value.path).toBe('/organismes'))
    })
  })
})
