import type { OrganismesList } from '../../types'
import { screen } from '@testing-library/vue'
import { beforeEach, describe, expect, it, vi } from 'vitest'
import { defineComponent, h } from 'vue'
import { getMe } from '@/api/utilisateur'
import { ORGANISME } from '@/test/fixtures/organismes'
import { makeUser } from '@/test/fixtures/utilisateur'
import { renderWithApp, setupUser } from '@/test/render'
import { provideOrganismeEdition } from '../../composables/useOrganismeEdition'
import OrganismeActionsCell from './OrganismeActionsCell.vue'

function hostFor(row: OrganismesList) {
  return defineComponent({
    setup() {
      provideOrganismeEdition()
      return () => h(OrganismeActionsCell, { row })
    },
  })
}

describe('organismeActionsCell', () => {
  beforeEach(() => {
    vi.mocked(getMe).mockReset().mockResolvedValue(makeUser([], true))
  })

  it('opens the home of the organisme', async () => {
    const user = setupUser()

    const { router } = await renderWithApp(hostFor({ ...ORGANISME, authorized_actions: ['list_recrutements'] }), { route: '/organismes' })
    await user.click(await screen.findByRole('button', { name: `Actions pour ${ORGANISME.nom}` }))
    await user.click(await screen.findByRole('menuitem', { name: 'Se connecter à l’organisme' }))

    await vi.waitFor(() =>
      expect(router.currentRoute.value.path).toBe(`/organismes/${ORGANISME.uuid}/accueil`),
    )
  })

  it('only offers the actions the user is allowed to take', async () => {
    const user = setupUser()

    await renderWithApp(hostFor({ ...ORGANISME, authorized_actions: [] }), { route: '/organismes' })
    await user.click(await screen.findByRole('button', { name: `Actions pour ${ORGANISME.nom}` }))

    expect((await screen.findAllByRole('menuitem')).map(item => item.textContent?.trim())).toEqual(['Modifier l’organisme'])
  })
})
