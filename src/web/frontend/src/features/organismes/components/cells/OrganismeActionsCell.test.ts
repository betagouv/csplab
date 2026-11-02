import { screen } from '@testing-library/vue'
import { describe, expect, it, vi } from 'vitest'
import { defineComponent, h } from 'vue'
import { ORGANISME } from '@/test/fixtures/organismes'
import { renderWithApp, setupUser } from '@/test/render'
import { provideOrganismeEdition } from '../../composables/useOrganismeEdition'
import OrganismeActionsCell from './OrganismeActionsCell.vue'

const Host = defineComponent({
  setup() {
    provideOrganismeEdition()
    return () => h(OrganismeActionsCell, { row: ORGANISME })
  },
})

describe('organismeActionsCell', () => {
  it('opens the recrutements of the organisme', async () => {
    const user = setupUser()

    const { router } = await renderWithApp(Host, { route: '/organismes' })
    await user.click(screen.getByRole('button', { name: `Actions pour ${ORGANISME.nom}` }))
    await user.click(await screen.findByRole('menuitem', { name: 'Se connecter à l’organisme' }))

    await vi.waitFor(() =>
      expect(router.currentRoute.value.path).toBe(`/organismes/${ORGANISME.uuid}/recrutements`),
    )
  })
})
